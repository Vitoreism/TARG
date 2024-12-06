from selenium import webdriver
from fastapi import HTTPException
from typing import Dict, List
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException
)
from bs4 import BeautifulSoup
import time
from time import sleep
import pymongo
from pymongo import MongoClient, errors
from urllib.parse import unquote


# Configurações do MongoDB
MONGO_URI = "mongodb://localhost:27017/"  # Substitua pela sua string de conexão, se estiver usando o Atlas
DATABASE_NAME = "news_database"            # Nome do banco de dados
COLLECTION_NAME = "news_collection"        # Nome da coleção

def get_db_collection():
    """
    Estabelece a conexão com o MongoDB e retorna a coleção desejada.
    Cria um índice único no campo 'link' para evitar duplicatas.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        # Cria um índice único no campo 'link' para evitar duplicatas
        collection.create_index("link", unique=True)
        print(f"Conectado ao MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
        return collection
    except errors.ConnectionFailure as e:
        print(f"Falha na conexão com o MongoDB: {e}")
        exit(1)
    except errors.PyMongoError as e:
        print(f"Erro ao configurar a coleção: {e}")
        exit(1)

def scrape_news(url, collection):
    """
    Realiza o scraping das notícias da URL fornecida e as armazena no MongoDB.
    Apenas adiciona notícias que ainda não existem na coleção com base no 'link'.
    """
    # Configuração do Selenium para o Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--headless")  # Descomente para executar em modo headless

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Lista para armazenar as novas notícias coletadas
    new_news = []

    try:
        # Acesse a URL
        print(f"Acessando a página principal: {url}")
        driver.get(url)

        
        # Aguarda o carregamento do iframe do anúncio
        try:
            out_of_page_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "OutOfPage"))
            )
            iframe = out_of_page_div.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)  # Entrando no iframe do anúncio

            try:
                fechar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "fechar"))
                )
                fechar.click()
                print("Anúncio fechado com sucesso.")
                driver.switch_to.default_content()  # Volta para o conteúdo principal
            except Exception as e:
                print(f'Não foi possível fechar o anúncio: {e}')
                driver.switch_to.default_content()  # Assegura que sai do iframe mesmo se falhar
        except TimeoutException:
            print("Iframe do anúncio não encontrado ou tempo de espera esgotado.")
            # Prossegue mesmo se o anúncio não for encontrado

        # Aguarda até que os itens de notícia estejam presentes no DOM
        wait = WebDriverWait(driver, 30)  # Aguarda até 30 segundos
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card__headline')))
        sleep(5)  # Reduzi o tempo de espera para 5 segundos, ajuste conforme necessário

        # Procura pelas notícias
        news_items = driver.find_elements(By.CLASS_NAME, 'article-card__headline')

        if not news_items:
            print("Nenhuma notícia encontrada.")
            return new_news
        else:
            print(f"{len(news_items)} notícias encontradas!")

        # Coleta os títulos e links primeiro para evitar referências obsoletas
        news_links = []
        for item in news_items:
            try:
                title = item.text.strip() if item.text else 'Sem Título'
                link_element = item.find_element(By.XPATH, './ancestor::a')
                link = link_element.get_attribute('href').strip() if link_element else 'Sem Link'
                if link.startswith('http'):
                    news_links.append({'title': title, 'link': link})
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(f"Erro ao coletar título/link: {e}")
                continue

        print(f"{len(news_links)} links coletados com sucesso.")

        # Processa cada notícia individualmente
        for idx, news in enumerate(news_links, start=1):
            title = news['title']
            link = news['link']
            print(f"\nAcessando notícia {idx}: {title}")
            print(f"Link: {link}")

            try:
                # Verifica se a notícia já está presente no MongoDB com base no 'link'
                if collection.find_one({"link": link}):
                    print("Notícia já existente no banco de dados. Pulando...")
                    break

                # Acessa o link da notícia
                driver.get(link)

                # Aguarda até que o conteúdo do artigo esteja presente
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'im-article')))
                except TimeoutException:
                    print(f"Tempo de espera esgotado para carregar a notícia {link}.")
                    continue

                # Extrai o conteúdo da notícia com BeautifulSoup
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # Localiza o <article> com a classe definida
                article_tag = soup.find('article', class_='im-article clear-fix')
                if not article_tag:
                    print(f"Elemento <article> não encontrado na notícia {link}.")
                    continue

                # Coleta os parágrafos do artigo
                paragraphs = article_tag.find_all('p')
                content = "\n".join([p.get_text(strip=True) for p in paragraphs]) if paragraphs else "Sem conteúdo"

                # Coleta a data de publicação
                date_tag = soup.find('time')
                date = date_tag.get_text(strip=True) if date_tag else "Sem data"

                # Cria o documento da notícia
                news_data = {
                    'title': title,
                    'link': link,
                    'content': content,
                    'date': date
                }

                # Insere a notícia no MongoDB
                try:
                    collection.insert_one(news_data)
                    new_news.append(news_data)
                    print(f"Notícia '{title}' inserida com sucesso no banco de dados.")
                except errors.DuplicateKeyError:
                    print(f"Duplicata encontrada para o link '{link}'. Notícia já existe.")
                except errors.PyMongoError as e:
                    print(f"Erro ao inserir a notícia '{title}': {e}")

            except Exception as e:
                print(f"Erro ao processar a notícia '{title}': {e}")
                continue

        return new_news

    except Exception as e:
        print(f"Erro geral durante o scraping: {e}")
        return new_news

    finally:
        driver.quit()




def get_news_by_title(title: str):
    """
    Recupera uma notícia específica do MongoDB com base no título.

    Parâmetros:
        title (str): O título da notícia a ser recuperada.

    Retorna:
        dict: Um dicionário contendo 'title', 'content', 'date' e 'analysis'.
              Retorna um dicionário de erro se a notícia não for encontrada.
    """
    if not title:
        return {"error": "Título não fornecido."}

    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        projection = {
            'title': 1,
            'content': 1,
            'date': 1,
            'analysis': 1,
            '_id': 0  # Não precisa do '_id' no retorno
        }
        
        # Busca a notícia pelo título exato
        news = collection.find_one({"title": title}, projection)
        
        if news:
            return news
        else:
            return {"error": "Notícia não encontrada."}

    except errors.ConnectionFailure as e:
        print(f"Falha na conexão com o MongoDB: {e}")
        return {"error": f"Falha na conexão com o MongoDB: {e}"}
    except errors.PyMongoError as e:
        print(f"Erro ao recuperar a notícia: {e}")
        return {"error": f"Erro ao recuperar a notícia: {e}"}



def get_titles_dict() -> Dict[str, List[str]]:
    """
    Recupera todas as notícias e retorna um dicionário onde as chaves são os títulos
    e os valores são listas de links correspondentes.
    
    Retorna:
        dict: Dicionário com 'title' como chave e lista de links como valor.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Define os campos a serem retornados (título e link)
        projection = {
            'title': 1,
            'link': 1,  # Presume-se que as notícias tenham um campo 'link'
            '_id': 0  # Não precisamos do _id
        }
        
        cursor = collection.find({}, projection)
        
        titles_dict: Dict[str, List[str]] = {}
        for doc in cursor:
            title = doc.get('title')
            link = doc.get('link')  # Presume-se que cada notícia tenha um campo 'link'
            if title and link:
                if title in titles_dict:
                    titles_dict[title].append(link)
                else:
                    titles_dict[title] = [link]
        
        print(f"Total de {len(titles_dict)} títulos recuperados.")
        return titles_dict
        
    except errors.ConnectionFailure as e:
        print(f"Falha na conexão com o MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados.")
    except errors.PyMongoError as e:
        print(f"Erro ao recuperar os documentos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao recuperar os dados.")




def main():
    # Obtém a coleção do MongoDB
    collection = get_db_collection()

    # URL da página principal
    url = 'https://www.infomoney.com.br/tudo-sobre/banco-do-brasil/'  # Substitua pela URL real

    # Executando a função para pegar as notícias
    new_news = scrape_news(url, collection)

    if new_news:
        print(f"\n{len(new_news)} novas notícias foram adicionadas ao banco de dados.")
    else:
        print("\nNenhuma nova notícia foi adicionada.")

    # Exibindo as notícias armazenadas (opcional)
    print("\nTodas as notícias armazenadas no banco de dados:")
    try:
        for news_item in collection.find().sort("date", pymongo.DESCENDING):
            print(f"Título: {news_item['title']}")
            print(f"Link: {news_item['link']}")
            print(f"Conteúdo: {news_item['content'][:100]}...")  # Exibe os primeiros 100 caracteres
            print(f"Data: {news_item['date']}\n")
    except errors.PyMongoError as e:
        print(f"Erro ao recuperar as notícias do banco de dados: {e}")

if __name__ == "__main__":
    main()
