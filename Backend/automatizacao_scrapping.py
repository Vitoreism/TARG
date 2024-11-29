import requests
from datetime import datetime
import pandas as pd

# URL da News API
url = "https://newsapi.org/v2/everything"

start_date = '2010-01-01'
end_date = '2010-04-01'

params = {
    'q': '"BBAS3"  "agronegócio" "Ações" "Bolsa de valores" "B3" "Imposto" "Selic" "Taxa selic" "Juros" "Taxa de juros" "Banco do Brasil" "Carteira de credito"',
    'language': 'pt', 
    'pageSize': 100,  
    'apiKey': 'edd160e0d4bd42148f33d34b91275158', 
    'from': start_date,  # Data inicial para as notícias (formato YYYY-MM-DD)
    'to': end_date,
}


def pull_news():
    try:
        # Fazendo a requisição à News API
        response = requests.get(url, params=params)

        # Verificando se a requisição foi bem-sucedida
        response.raise_for_status()

        # Transformando a resposta em formato JSON
        data = response.json()

        if data['status'] == 'ok' and 'articles' in data:
            for article in data['articles']:
                title = article['title']
                description = article['description']
                content = article['content'] 

                print(f'Título: {title}')
                print(f'Descrição: {description}')
                print(f'Conteúdo: {content}\n')
        else:
            print("Nenhuma notícia encontrada ou erro na resposta.")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

pull_news()


# Função para salvar as notícias em um arquivo CSV
def salvar_noticias_csv(noticias):
    # Criar um DataFrame a partir das notícias
    df = pd.DataFrame(noticias)

    # Verificar se o arquivo já existe para não sobrescrever
    try:
        df_existente = pd.read_csv('noticias_bbas3.csv')
        df = pd.concat([df_existente, df], ignore_index=True)
    except FileNotFoundError:
        pass  # Se o arquivo não existe, cria um novo DataFrame

    # Salvar as notícias no arquivo CSV
    df.to_csv('noticias_bbas3.csv', index=False)

# Função para puxar as notícias da News API e evitar duplicatas
def pull_news():
    noticias = []  # Lista para armazenar as notícias
    urls_vistas = set()  # Conjunto para armazenar as URLs já vistas e evitar duplicatas
    page = 1  # Começar pela primeira página

    while True:
        params['page'] = page  # Atualizar o parâmetro de página
        
        try:
            # Fazendo a requisição à News API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

            data = response.json()

            if data['status'] == 'ok' and 'articles' in data:
                new_articles = False  # Flag para verificar se encontrou novos artigos

                # Processando as notícias
                for article in data['articles']:
                    url_noticia = article['url']
                    if url_noticia not in urls_vistas:  # Verificar se a notícia já foi processada
                        urls_vistas.add(url_noticia)  # Adicionar a URL ao conjunto
                        
                        # Criar um dicionário para a notícia
                        noticia = {
                            'Título': article['title'],
                            'Descrição': article.get('description', 'Descrição não disponível'),
                            'Conteúdo': article.get('content', 'Conteúdo não disponível'),
                            'URL': url_noticia,
                            'Data': article['publishedAt']
                        }
                        noticias.append(noticia)  # Adicionar a notícia à lista
                        new_articles = True  # Marcar que encontrou novos artigos

                # Se não encontrar novos artigos, sair do loop
                if not new_articles:
                    print("Nenhuma notícia nova encontrada. Finalizando.")
                    break

                # Incrementar a página para buscar mais notícias
                page += 1
            else:
                print("Nenhuma notícia encontrada ou erro na resposta.")
                break
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            break

    # Salvar as notícias no CSV
    if noticias:
        salvar_noticias_csv(noticias)