# CÓDIGO QUE PERCORRE UM INTERVALO DE DATA E GERA 1 ARQUIVO PARA CADA DIA DENTRO DO INTERVALO JÁ PULANDO OS SÁBADOS E DOMINGOS DO MÊS E CONSIDERANDO O MULTIPLICADOR

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
carteira = "S324572197"  # Código da carteira S que deseja consultar Ex.: S1000 ou S328252097

# Defina o multiplicador da carteira
multiplicador_carteira = 17  # Defina o valor do multiplicador aqui

# Intervalo de datas
data_inicial = datetime(2023, 9, 1)  # Data no formato AAAA, Mês, Dia
data_final = datetime(2023, 9, 10)    # Data no formato AAAA, Mês, Dia

# Acessando a API para cada data no intervalo
data_atual = data_inicial

while data_atual <= data_final:
    # Verificar se a data atual é válida e não é sábado (6) ou domingo (7)
    if data_atual.month == 9 and data_atual.weekday() not in [5, 6]:  # Verifica se o mês é setembro e não é sábado ou domingo
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
            stops_df = pd.DataFrame(data["stops"])
            bars_df = pd.DataFrame(data["bars"])

            # Multiplicar o valor da carteira pelo multiplicador
            bars_df["open"] = bars_df["open"] * multiplicador_carteira
            bars_df["high"] = bars_df["high"] * multiplicador_carteira
            bars_df["low"] = bars_df["low"] * multiplicador_carteira
            bars_df["close"] = bars_df["close"] * multiplicador_carteira

            # Salvar o JSON em arquivos CSV e Excel dentro da pasta Relatorios
            bars_df.to_csv(f'Relatorios/Carteira_{carteira}x{multiplicador_carteira}_{data_intraday}_CSV.csv')
            bars_df.to_excel(f'Relatorios/Carteira_{carteira}x{multiplicador_carteira}_{data_intraday}_Excel.xlsx')
                    
        else:
            print(f"Erro na solicitação para a data {data_intraday}: Status {requisicao.status_code}")

    print(data_atual)
    
    # Avançar para o próximo dia
    data_atual += timedelta(days=1)

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