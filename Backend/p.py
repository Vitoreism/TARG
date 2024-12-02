from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time
from time import sleep

def scrape_news(url):
    # Configuração do Selenium para o Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--headless")  # Descomente para executar em modo headless

    driver = webdriver.chrome(service=Service(ChromeDriverManager().install(), options=chrome_options))

    # Lista para armazenar as notícias coletadas
    news_data = []

    try:
        # Acesse a URL
        print(f"Acessando a página principal: {url}")
        driver.get(url)
        
        out_of_page_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "OutOfPage"))
        )
    
        iframe = out_of_page_div.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe) # Entrando no iframe do anuncio
    
        try:
            fechar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "fechar"))
            )
            fechar.click()
            print("Anúncio fechado com sucesso.")
            driver.switch_to.default_content() # Volta pro iframe principal
        except Exception as e:
            print(f'Não foi possível fechar o anúncio: {e}')

        # Aguarda até que os itens de notícia estejam presentes no DOM
        wait = WebDriverWait(driver, 30)  # Aguarda até 30 segundos
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card__headline')))
        sleep(30)
        # Procura pelas notícias
        news_items = driver.find_elements(By.CLASS_NAME, 'article-card__headline')

        if not news_items:
            print("Nenhuma notícia encontrada.")
            return news_data
        else:
            print(f"{len(news_items)} notícias encontradas!")

        # Coleta os títulos e links primeiro para evitar referências obsoletas
        news_links = []
        for item in news_items:
            try:
                title = item.text.strip() if item.text else 'No title'
                link_element = item.find_element(By.XPATH, './ancestor::a')
                link = link_element.get_attribute('href').strip() if link_element else 'No link'
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
                content = "\n".join([p.get_text(strip=True) for p in paragraphs]) if paragraphs else "No content"

                # Coleta a data de publicação
                date_tag = soup.find('time')
                date = date_tag.get_text(strip=True) if date_tag else "No date"

                # Armazena os dados da notícia
                news_data.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'date': date
                })

                print(f"Notícia '{title}' processada com sucesso.")

            except Exception as e:
                print(f"Erro ao processar a notícia '{title}': {e}")
                continue

        return news_data

    except Exception as e:
        print(f"Erro geral durante o scraping: {e}")
        return news_data

    finally:
        # Fechar o driver do Selenium
        driver.quit()

# URL da página principal
url = 'https://www.infomoney.com.br/tudo-sobre/banco-do-brasil/'  # Substitua pela URL real

# Executando a função para pegar as notícias
news = scrape_news(url)

# Exibindo as notícias coletadas
print("\nTodas as notícias coletadas:")
for news_item in news:
    print(f"Título: {news_item['title']}")
    print(f"Link: {news_item['link']}")
    print(f"Conteúdo: {news_item['content']}")
    print(f"Data: {news_item['date']}\n")
