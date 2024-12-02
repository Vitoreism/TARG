import openai
from dotenv import load_dotenv
import os

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
    
    def analyze_news_article(news_text: str, title: str) -> str:
        try:
            analysis = gpt_instance.call_gpt(gpt_instance.prompt, f"titulo: {title}\ncorpo:{news_text}")
            return analysis
        except Exception as e:
            raise Exception(f"Erro ao chamar o GPT: {e}")
    
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


