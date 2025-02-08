# CÓDIGO QUE ANALISA 1 DIA DA COMBINAÇÃO DE 2 OU MAIS CARTEIRAS E SOMA OS VALORES DE MÁXIMA E MINIMA DE CADA MINUTO NO X1 E COLOCA TODOS OS VALORES EM UMA ÚNICA TABELA

# pip install requests timedelta datetime pandas

import requests
import pandas as pd
import json
import base64
import time

# Registre o tempo inicial
tempo_inicial = time.time()

# Credenciais de acesso, o Token já deve estar ativo para poder usar 
token = "a518b45263e38a3664fde4c7a1cd518f"
email = "testeapitg@gmail.com"

# Números das Carteiras e Data do Intraday
carteira1 = "S004931097"  # Código da primeira carteira S que deseja consultar
carteira2 = "S328252097"  # Código da segunda carteira S que deseja consultar
carteira3 = "S609623197"  # Código da terceira carteira S que deseja consultar
data_intraday = 20231004 # Data no formato AAAAMMDD (Ano, Mês, Dia)

# Lista para armazenar os resultados
resultados = []

# Função para somar os valores de máxima e mínima
def somar_maxima_minima(df1, df2, df3):
    soma_maxima = df1["high"] + df2["high"] + df3["high"]
    soma_minima = df1["low"] + df2["low"] + df3["low"]
    return soma_maxima, soma_minima

# Acessando a API para a primeira carteira
credenciais = email + ":" + token
credenciais_codificadas = base64.b64encode(credenciais.encode())
auth = "Basic " + credenciais_codificadas.decode()
link_carteira1 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira1}&intraday={data_intraday}"
requisicao_carteira1 = requests.get(link_carteira1, headers={"accept": "application/json", "Authorization": auth})
dic_requisicao_carteira1 = requisicao_carteira1.json()

# Carregue o JSON em um DataFrame para a primeira carteira
data_carteira1 = json.loads(requisicao_carteira1.text)
bars_df_carteira1 = pd.DataFrame(data_carteira1["bars"])

# Acessando a API para a segunda carteira
link_carteira2 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira2}&intraday={data_intraday}"
requisicao_carteira2 = requests.get(link_carteira2, headers={"accept": "application/json", "Authorization": auth})
dic_requisicao_carteira2 = requisicao_carteira2.json()

# Carregue o JSON em um DataFrame para a segunda carteira
data_carteira2 = json.loads(requisicao_carteira2.text)
bars_df_carteira2 = pd.DataFrame(data_carteira2["bars"])

# Acessando a API para a terceira carteira
link_carteira3 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira3}&intraday={data_intraday}"
requisicao_carteira3 = requests.get(link_carteira3, headers={"accept": "application/json", "Authorization": auth})
dic_requisicao_carteira3 = requisicao_carteira3.json()

# Carregue o JSON em um DataFrame para a terceira carteira
data_carteira3 = json.loads(requisicao_carteira3.text)
bars_df_carteira3 = pd.DataFrame(data_carteira3["bars"])

# Somar os valores de máxima e mínima para as duas carteiras
soma_maxima, soma_minima = somar_maxima_minima(bars_df_carteira1, bars_df_carteira2, bars_df_carteira3)

# Cria as tabelas que irão receber a soma das máximas e das mínimas de cada minuto
maximas = {'Soma das Máximas': soma_maxima}
minimas = {'Soma das Mínimas': soma_minima}

bars_df_maxima = pd.DataFrame(maximas)
bars_df_minima = pd.DataFrame(minimas)

# Junta as duas carteiras e a somas das máximas e mínimas em uma única variável
resultados = pd.concat([bars_df_carteira1, bars_df_carteira2, bars_df_carteira3, bars_df_maxima, bars_df_minima], axis=1)

# Criar um DataFrame a partir da lista de resultados
resultados_df = pd.DataFrame(resultados)

# Salvar o DataFrame com as somas em um arquivo CSV e Excel dentro da pasta Relatorios
resultados_df.to_csv(f'Relatorios/Soma_Max_Min_Carteiras_{carteira1}_{carteira2}_{carteira3}_{data_intraday}_CSV.csv', index=False)
resultados_df.to_excel(f'Relatorios/Soma_Max_Min_Carteiras_{carteira1}_{carteira2}_{carteira3}_{data_intraday}_Excel.xlsx', index=False)

# Imprimir o DataFrame com as somas
print("\nTabela de Barras com Somas:")
print(resultados)

# Registre o tempo final
tempo_final = time.time()

# Calcule o tempo decorrido em segundos
tempo_decorrido_segundos = tempo_final - tempo_inicial

# Converta o tempo decorrido em horas, minutos e segundos
horas = int(tempo_decorrido_segundos // 3600)
tempo_decorrido_segundos %= 3600
minutos = int(tempo_decorrido_segundos // 60)
segundos = int(tempo_decorrido_segundos % 60)

# Imprima o tempo decorrido no formato HH:MM:SS
print(tempo_inicial)
print(tempo_final)
print(f"Tempo decorrido: {tempo_decorrido_segundos} segundos")
print(f"Tempo decorrido: {horas:02d}:{minutos:02d}:{segundos:02d}")