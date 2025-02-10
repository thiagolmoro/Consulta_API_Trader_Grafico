# CÓDIGO QUE PERCORRE UM INTERVALO DE DATA E GERA 1 ÚNICO ARQUIVO COM A MÁXIMA E MÍNIMA DE CADA DIA, JÁ PULANDO OS SÁBADOS E DOMINGOS DO MÊS NO X1

# pip install requests timedelta datetime pandas

import requests
import pandas as pd
import json
import base64
from datetime import datetime, timedelta
import time

# Registre o tempo inicial
tempo_inicial = time.time()

# Credenciais de acesso, o Token já deve estar ativo para poder usar 
token = "SEU_TOKEN_AQUI"
email = "SEU_EMAIL_AQUI"

# Número da Carteira
carteira = "S155446297"  # Código da carteira S que deseja consultar Ex.: S1000 ou S328252097

# Intervalo de datas
data_inicial = datetime(2023, 1, 1)  # Data no formato AAAA, Mês, Dia
data_final = datetime(2024, 8, 26)   # Data no formato AAAA, Mês, Dia

# Lista para armazenar os resultados
resultados = []

# Acessando a API para cada data no intervalo
data_atual = data_inicial

while data_atual <= data_final:
    # Verificar se a data atual não é sábado (5) ou domingo (6)
    if data_atual.weekday() not in [5, 6]:
        # Construir o URL da API para a data atual
        data_intraday = int(data_atual.strftime('%Y%m%d'))
        link = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira}&intraday={data_intraday}"
        
        # Acessando a API
        credenciais = email + ":" + token
        credenciais_codificadas = base64.b64encode(credenciais.encode())
        auth = "Basic " + credenciais_codificadas.decode()
        headers = {"accept": "application/json", "Authorization": auth}
        requisicao = requests.get(link, headers=headers)
        
        if requisicao.status_code == 200:
            dic_requisicao = requisicao.json()
            
            # Carregar o JSON em um DataFrame
            data = json.loads(requisicao.text)

            # Separar o DataFrame em 2 partes
            bars_df = pd.DataFrame(data["bars"])
            
            if not bars_df.empty:
                # Calcular o maior valor da coluna "high" e o menor valor da coluna "low"
                max_high = bars_df["high"].max()
                min_low = bars_df["low"].min()
                
                # Armazenar os resultados na lista
                resultados.append({"Data": data_intraday, "Máxima do Dia": max_high, "Mínima do Dia": min_low})
        else:
            print(f"Erro na solicitação para a data {data_intraday}: Status {requisicao.status_code}")

    print(data_atual)
    
    # Avançar para o próximo dia
    data_atual += timedelta(days=1)

# Criar um DataFrame a partir da lista de resultados
resultados_df = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo CSV e Excel
resultados_df.to_csv(f'Relatorios/Resultados_Max_Min_{carteira}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_CSV.csv', index=False)
resultados_df.to_excel(f'Relatorios/Resultados_Max_Min_{carteira}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_Excel.xlsx', index=False)

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