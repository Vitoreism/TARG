import openai
from dotenv import load_dotenv
import os
from pymongo import MongoClient, errors


load_dotenv()
gpt_key = os.environ.get("OPENAI_KEY")

class GPT():
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.prompt = """"
        Ola, somos a TARG, empresa que está trabalhando com o mercado de ações!/ 
        a mensagem que irei lhe mandar é uma notícia sobre o mercado financeiro, quero que você faça uma análise sentimental!/
        sobre o texto contido na notícia/
        ESSAS ANÁLISES DEVEM SER VOLTADAS APENAS PARA A REALIDADE DA AÇÃO DO BANCO DO BRASIL(BBAS3)!/
        AS ANÁLISES DEVEM SER FEITAS LEVANDO EM CONSIDERAÇÃO UM CURTO PRAZO, E NÃO MÉDIO / LONGO PRAZO!/
        A noticia pode ser: Positiva, que representa uma tendencia de alta para a ação do BANCO DO BRASIL (BBAS3)/
        Neutra, que não vai apresentar tanto impacto para a empresa do BANCO DO BRASIL (BBAS3), mantendo-se sua estabilidade"/ 
        Negativa, que representa algo ruim / com tendencia de queda para ação do BANCO DO BRASIL (BBAS3)/

        Além da análise sentimental, quero que você justifique o porque que foi considerado negativo, positivo ou neutro determinada
        notícia para a realidade da ação do BANCO DO BRASIL (BBAS3)/

        SAIBA QUE ALGUMAS NOTÍCIAS NÃO VÃO SER DIRETAMENTE SOBRE O BANCO DO BRASIL (BBAS3), MAS QUE PODEM INTERFERIR E IMPACTAR INDIRETAMENTE./

        CASO VOCÊ RECEBA UMA NOTÍCIA QUE NÃO POSSUI NENHUM TIPO DE CONEXÃO COM A AÇÃO BBAS3, NEM DIRETA NEM INDIRETAMENTE, DEVE-SE ANALISÁ-LA COMO INVÁLIDA./
        
        """

    def call_gpt(self, prompt: str, question: str) -> str:

        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.3,
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
    
    
        response_content = response.choices[0].message.content
        response_content = response_content.replace('```', '').replace('python', '')

        return response_content
    
    def analyze_news_article(self, news_text: str, title: str) -> str:
        try:
            analysis = self.call_gpt(self.prompt, f"Título: {title}\nCorpo: {news_text}".strip())
            return analysis
        except Exception as e:
            raise Exception(f"Erro ao chamar o GPT: {e}")
        
def get_db_collection():
    """
    Estabelece a conexão com o MongoDB e retorna a coleção desejada.
    Cria um índice único no campo 'link' para evitar duplicatas.
    """
    try:
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
        db = client["news_database"]  # Substitua pelo nome do seu banco de dados
        collection = db["news_collection"]  # Substitua pelo nome da sua coleção
        # Cria um índice único no campo 'link' para evitar duplicatas
        collection.create_index("link", unique=True)
        print(f"Conectado ao MongoDB: {db.name}.{collection.name}")
        return collection
    except errors.ConnectionFailure as e:
        print(f"Falha na conexão com o MongoDB: {e}")
        exit(1)
    except errors.PyMongoError as e:
        print(f"Erro ao configurar a coleção: {e}")
        exit(1)    
    

def process_and_analyze_news():
    # Instanciar a classe GPT
    gpt_instance = GPT(api_key=gpt_key)

    # Obter a coleção do MongoDB
    collection = get_db_collection()

    # Recuperar todas as notícias que ainda não foram analisadas
    # Assumindo que há um campo 'analysis' que armazena o resultado da análise
    query = {"analysis": {"$exists": False}}  # Filtra documentos sem análise
    try:
        news_cursor = collection.find(query)
        for news in news_cursor:
            title = news.get("title", "Sem Título")
            content = news.get("content", "Sem Conteúdo")
            link = news.get("link", "Sem Link")

            print(f"Analisando notícia: {title}")

            # Realizar a análise sentimental
            analysis = gpt_instance.analyze_news_article(content, title)

            # Atualizar o documento com a análise
            try:
                collection.update_one(
                    {"_id": news["_id"]},
                    {"$set": {"analysis": analysis}}
                )
                print(f"Análise concluída e armazenada para: {title}\n")
            except errors.PyMongoError as e:
                print(f"Erro ao atualizar a análise no MongoDB para '{title}': {e}\n")
    except errors.PyMongoError as e:
        print(f"Erro ao recuperar notícias do MongoDB: {e}")

if __name__ == "__main__":
    process_and_analyze_news()

gpt_instance = GPT(api_key=gpt_key)

resposta = gpt_instance.call_gpt(gpt_instance.prompt, """A Polícia Civil do Rio de Janeiro e o Ministério Público do estado (MPRJ) deflagraram, na manhã desta quinta-feira (21/11), uma operação contra fraudes noBanco do Brasil. Estima-se que o prejuízo ao banco foi de mais de R$ 40 milhões.


Entre os alvos da Operação Chave Mestra estão funcionários e terceirizados investigados por participação em organização criminosa e invasão de dispositivo de informática.


Segundo o MPRJ, as investigações tiveram início a partir de informações apuradas pela Unidade de Segurança Institucional do Banco do Brasil e revelaram que o grupo utiliza dispositivos eletrônicos como modens e roteadores clandestinos para acessar sistemas internos de agências bancárias e obter dados sigilosos de clientes, manipulando essas informações para cometerfraudes financeiras.


A organização atuava desde dezembro de 2023 e, em apenas oito meses, conseguiu invadir o sistema de segurança de agências do Banco do Brasil localizadas no Recreio dos Bandeirantes, Barra da Tijuca, Vila Isabel, Centro do Rio, além de unidades localizadas nos municípios deNiterói.


Ainda de acordo com oMinistério Público, o grupo criminoso atuava com divisão de tarefas específicas entre aliciadores, aliciados, instaladores, operadores financeiros e líderes.


Ao todo são cumpridos 16 mandados de busca e apreensão contra 11 investigados em São Gonçalo, Taquara, Barra da Tijuca, Praça Seca, Magé, Recreio dos Bandeirantes, Pechincha, Cidade de Deus, Magalhães Bastos e Irajá. Cerca de 25 equipes policiais da Delegacia de Roubos e Furtos (DRF) e do Grupo de Atuação Especial de Combate ao Crime Organizado (Gaeco/MPRJ) participam da operação. O objetivo é apreender dispositivos eletrônicos ilegais, coletar provas e identificar outros integrantes do esquema criminoso.


AoMetrópoles, o Banco do Brasil informou que esse é um desdobramento da operação que se iniciou em julho deste ano, e que está em sua quarta fase. As investigações iniciaram a partir de apuração interna, que detectou irregularidades, as quais foram comunicadas às autoridades policiais.


“O BB possui processos estabelecidos para monitoramento e apuração de fraudes contra a instituição, adotou todas as providências no seu âmbito de atuação e colabora com as investigações do caso”, afirma a instituição em nota.


...

Receba notícias do Metrópoles no seuTelegrame fique por dentro de tudo! Basta acessar o canal:https://t.me/metropolesurgente.""")