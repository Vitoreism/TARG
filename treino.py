import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, pipeline
import wandb

# Inicializar o WandB para monitoramento do treinamento
wandb.login()

# Carregar o dataset
data = pd.read_csv('Dataset/financial_phrase_bank_pt_br.csv')

# Selecionar apenas as colunas de sentimento e texto em português
data = data[['y', 'text_pt']]

# Mapear rótulos para 0 (negativo), 1 (neutro) e 2 (positivo)
data['y'] = data['y'].map({'positive': 2, 'neutral': 1, 'negative': 0})

# Dividir o dataset em treino e validação
train_texts, val_texts, train_labels, val_labels = train_test_split(
    data['text_pt'].values, data['y'].values, test_size=1, random_state=42
)

# Carregar o tokenizador BERT em português
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')

# Tokenizar os textos de treino e validação
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True, max_length=128)

# Definir o Dataset personalizado para o PyTorch
class FinancialDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Criar os datasets de treino e validação
train_dataset = FinancialDataset(train_encodings, train_labels)
val_dataset = FinancialDataset(val_encodings, val_labels)

# Carregar o modelo BERT com classificação para 3 classes
model = BertForSequenceClassification.from_pretrained('neuralmind/bert-base-portuguese-cased', num_labels=3)

# Iniciar o WandB para monitoramento
wandb.init(project="sentiment_analysis_project_improved", name="sentiment_analysis_experiment_improved")

# Configurar os parâmetros de treinamento
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,              
    per_device_train_batch_size=4,    
    per_device_eval_batch_size=4,     
    warmup_steps=500,                 
    weight_decay=0.01,                
    learning_rate=5e-5,               
    logging_dir='./logs',             
    save_strategy="epoch",
    evaluation_strategy="epoch",      
    run_name="sentiment_analysis_experiment_improved",  
    load_best_model_at_end=True,      
    lr_scheduler_type="cosine",       
    metric_for_best_model="eval_loss",
    gradient_accumulation_steps=2
    report_to=["wandb"]
)

# Definir métricas personalizadas para precisão, revocação e F1-score
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

# Inicializar o Trainer
trainer = Trainer(
    model=model,                         
    args=training_args,                  
    train_dataset=train_dataset,         
    eval_dataset=val_dataset,            
    compute_metrics=compute_metrics      
)


# Iniciar o treinamento
trainer.train()

# Avaliação do modelo
eval_results = trainer.evaluate()
print(eval_results)

# Finalizar o WandB após o treinamento
wandb.finish()

# Salvar o modelo e o tokenizador treinados
model.save_pretrained('./sentiment-analysis-model')
tokenizer.save_pretrained('./sentiment-analysis-model')

# Definir o mapeamento dos rótulos de saída do modelo para os rótulos de sentimento interpretáveis
label_map = {
    "LABEL_0": "negativo",
    "LABEL_1": "neutro",
    "LABEL_2": "positivo"
}

# Carregar o pipeline de análise de sentimento usando o modelo e o tokenizador salvos
sentiment_pipeline = pipeline("sentiment-analysis", model='./sentiment-analysis-model', tokenizer='./sentiment-analysis-model')

# Exemplo de novas notícias para inferência
noticias_novas = [
    "A empresa X apresentou uma grande alta nos lucros do último trimestre.",
    "Problemas regulatórios podem comprometer os planos de expansão da empresa Y."
]

# Obter as previsões de sentimento para cada notícia
resultados = sentiment_pipeline(noticias_novas)

# Exibir os resultados com o mapeamento dos rótulos e pontuação de confiança
for noticia, resultado in zip(noticias_novas, resultados):
    sentimento = label_map.get(resultado['label'], "desconhecido")  # Mapeia o rótulo para o texto interpretável
    print("Notícia:", noticia)
    print("Sentimento:", sentimento)
    print("Pontuação:", resultado['score'])
    print("="*50)

