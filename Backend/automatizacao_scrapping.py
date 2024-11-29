import requests
from datetime import datetime

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
