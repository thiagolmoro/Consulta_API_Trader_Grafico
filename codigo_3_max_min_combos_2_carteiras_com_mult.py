# CÓDIGO QUE PERCORRE UM INTERVALO DE DATA E GERA 1 ÚNICO ARQUIVO COM A MÁXIMA E MÍNIMA DE CADA DIA DE UMA COMBINAÇÃO
# DE CARTEIRAS JÁ MULTIPLICANDO CADA UMA DELAS PELO MULTIPLICADR ESCOLHIDO, JÁ PULANDO OS SÁBADOS E DOMINGOS DO MÊS.

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

# Números das Carteiras
carteira1 = "S326462297"  # Código da primeira carteira S que deseja consultar
carteira2 = "S488313297"  # Código da segunda carteira S que deseja consultar

# Multiplicadores para cada carteira
multiplicador_carteira1 = 12  # Substitua pelo multiplicador desejado para a carteira 1
multiplicador_carteira2 = 12  # Substitua pelo multiplicador desejado para a carteira 2

# Intervalo de datas
data_inicial = datetime(2023, 11, 1)  # Data inicial no formato AAAA, Mês, Dia
data_final = datetime(2024, 7, 10)    # Data final no formato AAAA, Mês, Dia

# Função para somar os valores de máxima e mínima
def somar_maxima_minima(df1, df2):
    # Somar os valores de máxima e mínima para as carteiras após multiplicá-los
    # soma_maxima = (bars_df_carteira1["high"] * multiplicador_carteira1) + (bars_df_carteira2["high"] * multiplicador_carteira2)
    # soma_minima = (bars_df_carteira1["low"] * multiplicador_carteira1) + (bars_df_carteira2["low"] * multiplicador_carteira2)
    # soma_maxima = (df1["high"] * multiplicador_carteira1) + (df2["high"] * multiplicador_carteira2)
    # soma_minima = (df1["low"]  * multiplicador_carteira1) + (df2["low"] * multiplicador_carteira2)
    soma_maxima = (df1["high"] * multiplicador_carteira1) + (df2["high"] * multiplicador_carteira2)
    soma_minima = (df1["low"]  * multiplicador_carteira1) + (df2["low"] * multiplicador_carteira2)
    return soma_maxima, soma_minima

# Lista para armazenar os resultados
resultados = []

# Acessando a API para cada dia no intervalo
data_atual = data_inicial

while data_atual <= data_final:
    # Verificar se a data atual não é sábado (5) ou domingo (6)
    if data_atual.weekday() not in [5, 6]:
        # Construir o URL da API para a data atual
        data_intraday = int(data_atual.strftime('%Y%m%d'))
        
        credenciais = email + ":" + token
        credenciais_codificadas = base64.b64encode(credenciais.encode())
        auth = "Basic " + credenciais_codificadas.decode()
        
        # Acessando a API para a primeira carteira
        link_carteira1 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira1}&intraday={data_intraday}"
        requisicao_carteira1 = requests.get(link_carteira1, headers={"accept": "application/json", "Authorization": auth})
        dic_requisicao_carteira1 = requisicao_carteira1.json()
        
        # Carregar o JSON em um DataFrame para a primeira carteira
        data_carteira1 = json.loads(requisicao_carteira1.text)
        bars_df_carteira1 = pd.DataFrame(data_carteira1["bars"])
        
        # Acessando a API para a segunda carteira
        link_carteira2 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira2}&intraday={data_intraday}"
        requisicao_carteira2 = requests.get(link_carteira2, headers={"accept": "application/json", "Authorization": auth})
        dic_requisicao_carteira2 = requisicao_carteira2.json()
        
        # Carregar o JSON em um DataFrame para a segunda carteira
        data_carteira2 = json.loads(requisicao_carteira2.text)
        bars_df_carteira2 = pd.DataFrame(data_carteira2["bars"])
        
        
        # Somar os valores de máxima e mínima para as carteiras
        soma_maxima, soma_minima = somar_maxima_minima(bars_df_carteira1, bars_df_carteira2)
        
        # Calcular a maior máxima e a menor mínima do dia
        maxima_do_dia = soma_maxima.max()
        minima_do_dia = soma_minima.min()
        
        # Armazenar os resultados na lista
        resultados.append({"Data": data_intraday, "Maior Máxima do Dia": maxima_do_dia, "Menor Mínima do Dia": minima_do_dia})
    
    print(data_atual)
    
    # Avançar para o próximo dia
    data_atual += timedelta(days=1)

# Criar um DataFrame a partir da lista de resultados
resultados_df = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo CSV e Excel dentro da pasta Relatorios
# resultados_df.to_csv(f'Relatorios/Max_Min_Carteiras_{carteira1}x{multiplicador_carteira1}_{carteira2}x{multiplicador_carteira2}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_CSV.csv', index=False)
# resultados_df.to_excel(f'Relatorios/Max_Min_Carteiras_{carteira1}x{multiplicador_carteira1}_{carteira2}x{multiplicador_carteira2}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_Excel.xlsx', index=False)
resultados_df.to_csv(f'Relatorios/Max_Min_Carteiras_{carteira1}x{multiplicador_carteira1}_{carteira2}x{multiplicador_carteira2}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_CSV.csv', index=False)
resultados_df.to_excel(f'Relatorios/Max_Min_Carteiras_{carteira1}x{multiplicador_carteira1}_{carteira2}x{multiplicador_carteira2}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_Excel.xlsx', index=False)

# Imprimir o DataFrame com as maiores máximas e menores mínimas
print("\nTabela de Maiores Máximas e Menores Mínimas:")
print(resultados_df)

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