from pymongo import MongoClient
from urllib.parse import unquote

# Configurações do MongoDB
MONGO_URI = "mongodb://localhost:27017"  # URL do MongoDB
DATABASE_NAME = "news_database"  # Nome do banco de dados
COLLECTION_NAME = "news_collection"  # Nome da coleção

# Conexão com o MongoDB
def connect_to_mongo():
    """
    Conecta ao MongoDB e retorna a coleção.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print(f"Conectado ao MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
        return collection
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None

# Função para buscar um link no MongoDB
def find_news_by_link(collection, link: str):
    """
    Busca uma notícia no MongoDB pelo link exato.
    
    Parâmetros:
        collection: A coleção do MongoDB onde buscar.
        link (str): O link da notícia a ser buscado.

    Retorna:
        dict: O documento encontrado ou None se não existir.
    """
    try:
        result = collection.find_one({"link": link})
        if result:
            print(f"Notícia encontrada: {result}")
        else:
            print("Notícia não encontrada.")
        return result
    except Exception as e:
        print(f"Erro ao buscar notícia: {e}")
        return None

# Função para decodificar e imprimir URLs
def print_decoded_url(encoded_url: str):
    """
    Recebe uma URL codificada, decodifica-a e imprime o resultado.
    
    Parâmetros:
        encoded_url (str): A URL codificada que precisa ser decodificada.
    """
    try:
        # Decodifica a URL
        decoded_url = unquote(encoded_url)
        
        # Imprime a URL decodificada
        print(f"URL codificada: {encoded_url}")
        print(f"URL decodificada: {decoded_url}")
        return decoded_url
    except Exception as e:
        print(f"Erro ao decodificar a URL: {e}")
        return None

# Main Script
if __name__ == "__main__":
    # Conectar ao MongoDB
    collection = connect_to_mongo()
    if collection is None:
        print("Falha ao conectar ao MongoDB. Saindo...")
        exit(1)

    # URL para busca no banco de dados
    original_link = "https://www.infomoney.com.br/business/justica-de-goias-permite-que-banco-do-brasil-retenha-recebiveis-da-agrogalaxy/"
    print("\n--- Buscando a notícia pelo link original ---")
    result = find_news_by_link(collection, original_link)

    if result is not None:
        # Teste de URLs codificadas
        test_encoded_urls = [
            "https%3A//www.infomoney.com.br/business/justica-de-goias-permite-que-banco-do-brasil-retenha-recebiveis-da-agrogalaxy/",
            "https%3a//www.infomoney.com.br/business/justica-de-goias-permite-que-banco-do-brasil-retenha-recebiveis-da-agrogalaxy/",  # Teste com letras minúsculas no esquema
            "https://www.infomoney.com.br/business/justica-de-goias-permite-que-banco-do-brasil-retenha-recebiveis-da-agrogalaxy/"  # Sem codificação
        ]

        for url in test_encoded_urls:
            decoded_url = print_decoded_url(url)
            if decoded_url.strip() == result['link'].strip():
                print(f"As URLs correspondem para: {url}")
            else:
                print(f"As URLs NÃO correspondem para: {url}")
