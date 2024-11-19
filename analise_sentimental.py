from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Caminho para o diretório onde o modelo está salvo
model_path = "./sentiment-analysis-model"

# Carregar o modelo
#model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Carregar o tokenizador (necessário para tokenizar texto de entrada)
tokenizer = AutoTokenizer.from_pretrained(model_path)

sentiment_pipeline = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
# Exemplo de novas notícias para inferência

teste1 = 'Banco do Brasil vê melhora no campo e espera emprestar R$ 260 bilhões ao setor\nDepois de um início de safra mais fraco, em função de fatores relacionados ao clima e ao mercado que pesaram na margem dos produtores na temporada 2023/24, o Banco do Brasil alcançou R$ 100 bilhões em desembolsos de crédito rural, emissões de títulos para o setor e outros financiamentos vinculados à cadeia do agronegócio entre julho e a primeira quinzena de novembro.\nAté junho de 2025, a instituição espera aplicar R$ 260 bilhões em empréstimos ao setor e segue, com folga, na liderança desse mercado. O número é 13% maior do que liberado até o mesmo mês de 2024. A expectativa é que a partir de agora haja um ponto de virada no desempenho dos empréstimos ao setor agropecuário, com um cenário de reacomodação do mercado e de conjuntura mais promissora pela frente, já em 2025, disse Luiz Gustavo Braz Lage, vice-presidente de Agronegócios e Agricultura Familiar do BB, em entrevista exclusiva ao Valor. O BB admite que o ambiente no campo foi mais desafiador neste ano, com o aumento da inadimplência a níveis quase históricos (1,97%) e a elevação do risco associado ao setor, mas prevê melhora à frente. O otimismo é baseado nas estimativas de safra recorde — apesar do atraso inicial no plantio da soja —, na recuperação de margem em algumas cadeias afetadas pela seca deste ano, como soja e milho, e no fortalecimento de outras, como a pecuária, que detém 40% da carteira de agronegócios do banco, e vive um momento de valorização da arroba do boi. Segundo Lage, a diversificação do público atendido, em termos de cadeia produtiva e localização, permite pulverizar o risco e ampliar a presença no setor. A carteira de agronegócios do BB cresceu 13,7% até setembro deste ano, para R$ 386,6 bilhões, e pode terminar 2024 próxima dos R$ 400 bilhões. Para isso, o banco tem avaliado o risco e reconquistado clientes em um momento de “baixa” no mercado financeiro, em que “aventureiros” saem da atividade e mesmo instituições fortes pisam no freio e não expandem carteira. A gestão da base de dados e a proximidade com o campo têm feito a diferença. “É um crédito mais assertivo, temos uma carteira resiliente e diversificada, e uma gestão prudencial”, destacou o executivo. Felipe Guimarães Geissler Prince, vice-presidente de Controles Internos e Gestão de Riscos do banco, disse, na entrevista, que a saída de alguns agentes financeiros do mercado abre novas possibilidades para o banco. “Não tem como dizer que não existe oportunidade num setor cujo PIB tem projeção de crescer 5% em 2025 e onde culturas têm cenário bastante promissor”, afirmou. O BB reconhece que o desembolso de crédito rural pelas linhas tradicionais do Plano Safra está mais lento, mas diz que o movimento é compensado, em parte, pelas emissões de Cédulas de Produto Rural (CPR), que evoluíram 33% no primeiro trimestre deste ciclo. O saldo desses títulos no banco ultrapassou R$ 30 bilhões em setembro. Segundo dados do Banco Central, a queda nas liberações pelo Banco do Brasil é de 15%, de R$ 79,2 bilhões para R$ 67,1 bilhões entre julho e outubro na comparação com o mesmo período da safra passada. O recuo é menos intenso que a média geral. Por outro lado, o movimento beneficiou o BB, que expandiu a fatia no segmento, de 39% para 44% no quadrimestre. “O banco teve uma queda, mas bem menor do que o sistema como um todo. Houve atraso no lançamento do plano, os produtores estão mais cautelosos em relação à tomada de crédito. Antes havia postura do produtor de assegurar a contratação antes da safra, de forma antecipada, e agora esperou. A chuva demorou e tem menor demanda para investimentos”, relatou Lage. Ele disse, porém, que o ritmo já melhorou nas primeiras semanas de novembro, com desempenho 9% acima do mesmo mês do ciclo 2023/24, focado em crédito para pequenos e médios produtores. A expansão da participação do BB na aplicação dos recursos equalizáveis, que recebem subvenção do Tesouro Nacional, também ajudou a recuperar posições. Com o movimento de alta da Selic, já em 11,25% ao ano, o cenário pode ser ainda mais interessante. Dos R$ 60 bilhões que a instituição recebeu de limite do governo para emprestar recursos com juros subsidiados entre 3% e 11,5% no Plano Safra 2024/25, cerca de 48% ainda estão disponíveis e serão um diferencial nos próximos meses, apontaram os executivos do BB. “Voltamos a ter uma fatia justa nesses recursos equalizados. Na negociação, as projeções eram de queda de juros e agora vemos a curva se elevando, o que traz oportunidade. Hoje temos condição de oferecer custo mais atrativo, uma das alavancas que temos utilizado para resgatar clientes”, afirmou Prince.'

input=tokenizer(teste1, return_tensors="pt", truncation=True, padding=True, max_length=512)
input=tokenizer.decode(input['input_ids'][0], skip_special_tokens=True)

# Obter as previsões de sentimento para cada notícia
resultados = sentiment_pipeline(input)

label_map = {
    "LABEL_0": "negativo",
    "LABEL_1": "neutro",
    "LABEL_2": "positivo"
}

# Exibir os resultados com o mapeamento dos rótulos e pontuação de confiança
for noticia, resultado in zip(input, resultados):
    sentimento = label_map.get(resultado['label'], "desconhecido")  # Mapeia o rótulo para o texto interpretável
    print("Notícia:", noticia)
    print("Sentimento:", sentimento)
    print("Pontuação:", resultado['score'])
    print("="*50)

#inputs = tokenizer(teste1, max_length=512, padding=True, truncation=True, return_tensors="pt")

#outputs = model(**inputs)

#logits = outputs.logits
#pred = logits.argmax(dim=-1)

#print(f'Predição: {pred.item()}')
#print(outputs)
