from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Caminho para o diretório onde o modelo está salvo
model_path = "./sentiment-analysis-model"

# Carregar o tokenizador (necessário para tokenizar texto de entrada)
tokenizer = AutoTokenizer.from_pretrained(model_path)

sentiment_pipeline = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
# Exemplo de novas notícias para inferência

noticias = ['''BC aumenta Selic em 0,25% e juros passam para 10,75% ao ano
A Confederação Nacional da Indústria criticou a medida
O Banco Central elevou, nesta quarta-feira, a taxa de juros básicos da economia em 0,25 ponto percentual, passando de 10,5% para 10,75% ao ano. Foi o primeiro aumento da taxa Selic, pelo Copom, o Comitê de Política Monetária, desde agosto de 2022.

Nas reuniões de junho e julho, a decisão foi pela manutenção da taxa em 10,5% ao ano.

Entre as justificativas para medida, tomada por unanimidade pelos diretores do Banco Central, estão as estimativas de aumento dos preços ao consumidor e pressões no mercado de trabalho.

Em agosto, a inflação medida pelo IPCA ficou negativa em 0,02%. O índice de desemprego analisado pelo IBGE foi de 6,8% em julho, o menor desde 2014.

O aumento da taxa Selic ajuda a conter a inflação. Isso porque juros mais altos encarecem o crédito e desestimulam a produção e o consumo.

Logo após o anúncio do Copom, a Confederação Nacional da Indústria afirmou que aumentar os juros é medida excessiva para controlar a inflação e prejudicial ao crescimento econômico.
''', '''
Banco do Brasil (BBAS3) atualiza valor de dividendos e JCP
Proventos foram atualizados pela taxa Selic até a data-base de 21 de agosto
O Banco do Brasil (BBAS3) informou que o valor dos dividendos referente ao 2º trimestre de 2024 passou de R$ 0,15186078881 para R$ 0,15414348799.

Já o valor aprovado em juros sobre capital próprio (JCP) saiu de R$ 0,31448148860 R$ 0,31920862483.

O aumento nos proventos foi motivado pela atualização da taxa Selic até a data-base de ontem (21).''']

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

