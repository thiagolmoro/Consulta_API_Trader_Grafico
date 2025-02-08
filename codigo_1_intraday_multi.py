# CÓDIGO SIMPLES PARA CONSULTAR 1 DIA DE CADA VEZ DA CARTEIRA E RETORNAR OS DADOS INTRADAY JÁ CONSIDERANDO O MULTIPLICADOR

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

# Número da Carteira e Data do Intraday
carteira = "S328252097"  # Código da carteira S que deseja consultar Ex.: S1000 ou S328252097
data_intraday = 20231004 # Data no formato AAAAMMDD (Ano, Mês, Dia)

# Defina o multiplicador da carteira
multiplicador_carteira = 12  # Defina o valor do multiplicador aqui

# Acessando a API
credenciais = email + ":" + token
credenciais_codificadas = base64.b64encode(credenciais.encode())
auth = "Basic " + credenciais_codificadas.decode()
headers = {"accept": "application/json", "Authorization": auth}
link = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira}&intraday={data_intraday}"
requisicao = requests.get(link, headers=headers)
dic_requisicao = requisicao.json()

# Carregue o JSON em um DataFrame
data = json.loads(requisicao.text)

# Separa o DataFrame em 2 partes
stops_df = pd.DataFrame(data["stops"])
bars_df = pd.DataFrame(data["bars"])

# Multiplicar o valor da carteira pelo multiplicador
bars_df["open"] = bars_df["open"] * multiplicador_carteira
bars_df["high"] = bars_df["high"] * multiplicador_carteira
bars_df["low"] = bars_df["low"] * multiplicador_carteira
bars_df["close"] = bars_df["close"] * multiplicador_carteira

# Salvar o JSON em arquivos CSV e Excel dentro da pasta Relatorios
bars_df.to_csv('Relatorios/Carteira_'+carteira+'x'+str(multiplicador_carteira)+'_'+str(data_intraday)+'_CSV.csv')
bars_df.to_excel('Relatorios/Carteira_'+carteira+'x'+str(multiplicador_carteira)+'_'+str(data_intraday)+'_Excel.xlsx')

# Imprimir os DataFrames como tabelas
print("Tabela de Stops:")
print(stops_df)

print("\nTabela de Barras:")
print(bars_df)

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