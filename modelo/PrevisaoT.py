from modelo1 import ModeloPrevisao

window_size = 60
modelo = "TARG2.keras"

modelo = ModeloPrevisao(modelo, window_size)

inicio = "2024-07-01"
fim = "2024-11-27"

modelo.prever_precos(inicio, fim)
teste = modelo.prever_futuro(5)
print(teste)
