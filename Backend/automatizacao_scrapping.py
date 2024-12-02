from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

def scrape_news(url):
    # Configuração do Selenium para o Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Lista para armazenar as notícias coletadas
    news_data = []

    try:
        # Acesse a URL
        driver.get(url)

        # Aguarda até que os itens de notícia estejam presentes no DOM
        wait = WebDriverWait(driver, 30)  # Aguarda até 30 segundos
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card__headline')))

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
                title = item.text if item.text else 'No title'
                link_element = item.find_element(By.XPATH, './ancestor::a')
                link = link_element.get_attribute('href') if link_element else 'No link'

                print(f'LINK ELEMENT: {link_element}')
                print(f'LINK: {link}')
                news_links.append({'title': title, 'link': link})
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(f"Erro ao coletar título/link: {e}")
                continue

        # Itera sobre os links coletados
        for idx, news in enumerate(news_links, start=1):
            title = news['title']
            link = news['link']
            print(f"Processando notícia {idx}: {title}")

            if link == 'No link':
                print("Link inválido, pulando...")
                continue

            try:
                # Navega para a página da notícia
                driver.get(link)

                # Aguarda até que o conteúdo da notícia esteja presente
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))  # Ajuste conforme necessário
                except TimeoutException:
                    print("Tempo de espera esgotado para carregar o conteúdo da notícia.")
                
                # Coleta o HTML da página da notícia
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # Coletar conteúdo da notícia (ajuste a classe conforme necessário)
                content_tag = soup.find('div', {'class': 'content'})
                content = content_tag.get_text(separator='\n').strip() if content_tag else 'No content'

                # Coletar data de publicação (ajuste o seletor conforme necessário)
                date_tag = soup.find('span', class_='data')
                date = date_tag.get_text().strip() if date_tag else 'No date'

                # Armazenar os dados
                news_data.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'date': date
                })

            except Exception as e:
                print(f"Erro ao processar a notícia '{title}': {e}")
                continue

            finally:
                # Volta para a página inicial para processar a próxima notícia
                driver.back()
                sleep(3)
                # Recria a lista de elementos para evitar referências obsoletas
                try:
                    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'article-card__headline')))
                except TimeoutException:
                    print("Tempo de espera esgotado ao retornar à página principal.")
                    break

        return news_data

    except Exception as e:
        print(f"Erro geral durante o scraping: {e}")
        return news_data

    finally:
        # Fechar o driver do Selenium
        driver.quit()

# URL da página que você deseja fazer scraping
url = 'https://www.infomoney.com.br/tudo-sobre/banco-do-brasil/'  # Substitua pela URL real

# Executando a função para pegar as notícias
news = scrape_news(url)

# Exibindo as notícias coletadas
for news_item in news:
    print(f"Título: {news_item['title']}")
    print(f"Link: {news_item['link']}")
    print(f"Conteúdo: {news_item['content']}")
    print(f"Data: {news_item['date']}\n")
