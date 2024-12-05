from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Caminho para o diretório onde o modelo está salvo
model_path = "./sentiment-analysis-model"

# Carregar o tokenizador (necessário para tokenizar texto de entrada)
tokenizer = AutoTokenizer.from_pretrained(model_path)

sentiment_pipeline = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
# Exemplo de novas notícias para inferência

noticias = ['''Banco do Brasil: polícia investiga fraudes e prejuízos de R$ 40 mi
Agentes da PCRJ e da Gaeco/MPRJ cumprem 16 mandados de busca e apreensão. Entre os alvos estão funcionários e terceirizados
A Polícia Civil do Rio de Janeiro e o Ministério Público do estado (MPRJ) deflagraram, na manhã desta quinta-feira (21/11), uma operação contra fraudes no Banco do Brasil. Estima-se que o prejuízo ao banco foi de mais de R$ 40 milhões.

Entre os alvos da Operação Chave Mestra estão funcionários e terceirizados investigados por participação em organização criminosa e invasão de dispositivo de informática.

Segundo o MPRJ, as investigações tiveram início a partir de informações apuradas pela Unidade de Segurança Institucional do Banco do Brasil e revelaram que o grupo utiliza dispositivos eletrônicos como modens e roteadores clandestinos para acessar sistemas internos de agências bancárias e obter dados sigilosos de clientes, manipulando essas informações para cometer fraudes financeiras.

A organização atuava desde dezembro de 2023 e, em apenas oito meses, conseguiu invadir o sistema de segurança de agências do Banco do Brasil localizadas no Recreio dos Bandeirantes, Barra da Tijuca, Vila Isabel, Centro do Rio, além de unidades localizadas nos municípios de Niterói.
Ainda de acordo com o Ministério Público, o grupo criminoso atuava com divisão de tarefas específicas entre aliciadores, aliciados, instaladores, operadores financeiros e líderes.

Ao todo são cumpridos 16 mandados de busca e apreensão contra 11 investigados em São Gonçalo, Taquara, Barra da Tijuca, Praça Seca, Magé, Recreio dos Bandeirantes, Pechincha, Cidade de Deus, Magalhães Bastos e Irajá. Cerca de 25 equipes policiais da Delegacia de Roubos e Furtos (DRF) e do Grupo de Atuação Especial de Combate ao Crime Organizado (Gaeco/MPRJ) participam da operação. O objetivo é apreender dispositivos eletrônicos ilegais, coletar provas e identificar outros integrantes do esquema criminoso.

Ao Metrópoles, o Banco do Brasil informou que esse é um desdobramento da operação que se iniciou em julho deste ano, e que está em sua quarta fase. As investigações iniciaram a partir de apuração interna, que detectou irregularidades, as quais foram comunicadas às autoridades policiais.

“O BB possui processos estabelecidos para monitoramento e apuração de fraudes contra a instituição, adotou todas as providências no seu âmbito de atuação e colabora com as investigações do caso”, afirma a instituição em nota.''']

input=tokenizer(noticias, return_tensors="pt", truncation=True, padding=True, max_length=512)
input=[tokenizer.decode(input['input_ids'][x], skip_special_tokens=True) for x in range(len(noticias))]


# Obter as previsões de sentimento para cada notícia
resultados = sentiment_pipeline(input)

label_map = {
    "LABEL_0": "negativo",
    "LABEL_1": "neutro",
    "LABEL_2": "positivo"
}

# Exibir os resultados com o mapeamento dos rótulos e pontuação de confiança
for noticia, resultado in zip(noticias, resultados):
    sentimento = label_map.get(resultado['label'], "desconhecido")  # Mapeia o rótulo para o texto interpretável
    print("Notícia:", noticia)
    print("Sentimento:", sentimento)
    print("Pontuação:", resultado['score'])
    print("="*50)

