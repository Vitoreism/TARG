from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep


# Função para fazer scraping das notícias
def scrape_news(url):
    # Configuração do Selenium para o Chrome
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Acesse a URL
    driver.get(url)

    # Aguarda até que o conteúdo necessário esteja carregado
   # WebDriverWait(driver, 30).until(
    #    EC.presence_of_element_located((By.CLASS_NAME, "article-card_headline"))
    #)

    sleep(10)


    while True:
        try:
            # Espera até o botão "Carregar mais" aparecer na página
            load_more_button = locate_with(By.TAG_NAME, "button").below({By.TAG_NAME: "span"}).below({By.ID: "infinite-handle"})
            
            # Clica no botão
            load_more_button.click()
            
            # Aguarda 1 segundo entre os cliques
            sleep(1)
        except Exception as e:
            # Se o botão não estiver mais disponível, interrompe o laço
            print("Não há mais botões 'Carregar mais'. Finalizando.")
            break



    # Pegue o HTML da página carregada
    html = driver.page_source

    # Parse do HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Procura pelas notícias
    news_items = soup.find_all('h3', class_='article-card__headline')

    # Verificando o conteúdo encontrado
    if not news_items:
        print("Nenhuma notícia encontrada.")
    else:
        print("Notícias encontradas!")

    # Lista para armazenar as notícias coletadas
    news_data = []

    # Laço de repetição para percorrer todas as notícias
    for item in news_items:
        # Coletar título
        title = item.get_text() if item else 'No title'
        
        # Coletar URL da notícia
        link_tag = item.find('a', href=True)
        link = link_tag['href'] if link_tag else 'No link'
        
        # Coletar conteúdo da notícia (verifique a estrutura da página para ajustar)
        content_tag = item.find_next('p')
        content = content_tag.get_text() if content_tag else 'No content'
        
        # Coletar data de publicação (ajustar para o seletor correto)
        date_tag = item.find_previous('span', class_='data')  # Ajuste a classe conforme necessário
        date = date_tag.get_text().strip() if date_tag else 'No date'
        
        # Armazenar dados
        news_data.append({
            'title': title,
            'link': link,
            'content': content,
            'date': date
        })
    
    # Fechar o driver do Selenium
    driver.quit()

    return news_data

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
