# CÓDIGO QUE PERCORRE UM INTERVALO DE DATA E GERA 1 ÚNICO ARQUIVO COM A MÁXIMA, MÍNIMA E O FECHAMENTO DE CADA DIA DE UMA COMBINAÇÃO
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
carteira1 = "S221015197"  # Código da primeira carteira S que deseja consultar
carteira2 = "S321015197"  # Código da segunda carteira S que deseja consultar
carteira3 = "S521015197"  # Código da terceira carteira S que deseja consultar
carteira4 = "S925754197"  # Código da terceira carteira S que deseja consultar

# Multiplicadores para cada carteira
multiplicador_carteira1 = 1  # Substitua pelo multiplicador desejado para a carteira 1
multiplicador_carteira2 = 1  # Substitua pelo multiplicador desejado para a carteira 2
multiplicador_carteira3 = 1  # Substitua pelo multiplicador desejado para a carteira 3
multiplicador_carteira4 = 1  # Substitua pelo multiplicador desejado para a carteira 4

# Intervalo de datas
data_inicial = datetime(2023, 1, 2)  # Data inicial no formato AAAA, Mês, Dia
data_final = datetime(2023, 12, 13)    # Data final no formato AAAA, Mês, Dia

# Função para somar os valores de máxima, mínima e fechamento
def somar_maxima_minima_fechamento(df1, df2, df3, df4):
    # Somar os valores de máxima, mínima e fechamento para as carteiras após multiplicá-los
    soma_maxima = (df1["high"] * multiplicador_carteira1) + (df2["high"] * multiplicador_carteira2) + (df3["high"] * multiplicador_carteira3) + (df4["high"] * multiplicador_carteira4)
    soma_minima = (df1["low"]  * multiplicador_carteira1) + (df2["low"] * multiplicador_carteira2) + (df3["low"] * multiplicador_carteira3) + (df4["low"] * multiplicador_carteira4)
    soma_fechamento = (df1["close"]  * multiplicador_carteira1) + (df2["close"] * multiplicador_carteira2) + (df3["close"] * multiplicador_carteira3) + (df4["close"] * multiplicador_carteira4)
    return soma_maxima, soma_minima, soma_fechamento

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

        # Acessando a API para a terceira carteira
        link_carteira3 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira3}&intraday={data_intraday}"
        requisicao_carteira3 = requests.get(link_carteira3, headers={"accept": "application/json", "Authorization": auth})
        dic_requisicao_carteira3 = requisicao_carteira3.json()
        
        # Carregar o JSON em um DataFrame para a terceira carteira
        data_carteira3 = json.loads(requisicao_carteira3.text)
        bars_df_carteira3 = pd.DataFrame(data_carteira3["bars"])

        # Acessando a API para a quarta carteira
        link_carteira4 = f"https://api.tradergrafico.com.br/intraday_chart?codigo_cart={carteira4}&intraday={data_intraday}"
        requisicao_carteira4 = requests.get(link_carteira4, headers={"accept": "application/json", "Authorization": auth})
        dic_requisicao_carteira4 = requisicao_carteira4.json()
        
        # Carregar o JSON em um DataFrame para a quarta carteira
        data_carteira4 = json.loads(requisicao_carteira4.text)
        bars_df_carteira4 = pd.DataFrame(data_carteira4["bars"])
       
        # Somar os valores de máxima, mínima e fechamento para as carteiras
        soma_maxima, soma_minima, soma_fechamento = somar_maxima_minima_fechamento(bars_df_carteira1, bars_df_carteira2, bars_df_carteira3, bars_df_carteira4)
        
        # Calcular a maior máxima, a menor mínima e o fechamento do dia
        maxima_do_dia = soma_maxima.max()
        minima_do_dia = soma_minima.min()
        fechamento_do_dia = soma_fechamento.iloc[-1]

        # Armazenar os resultados na lista
        resultados.append({"Data": data_intraday, "Maior Máxima do Dia": maxima_do_dia, "Menor Mínima do Dia": minima_do_dia, "Fechamento do Dia": fechamento_do_dia})
    
    print(data_atual)
    
    # Avançar para o próximo dia
    data_atual += timedelta(days=1)

# Criar um DataFrame a partir da lista de resultados
resultados_df = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo CSV e Excel dentro da pasta Relatorios
resultados_df.to_csv(f'Relatorios/Max_Min_Fech_Carteiras_{carteira1}x{multiplicador_carteira1}_{carteira2}x{multiplicador_carteira2}_{carteira3}x{multiplicador_carteira3}_{carteira4}x{multiplicador_carteira4}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_CSV.csv', index=False)
resultados_df.to_excel(f'Relatorios/Max_Min_Fech_Carteiras_{carteira1}x{multiplicador_carteira1}_{carteira2}x{multiplicador_carteira2}_{carteira3}x{multiplicador_carteira3}_{carteira4}x{multiplicador_carteira4}_{data_inicial.strftime("%Y%m%d")}_{data_final.strftime("%Y%m%d")}_Excel.xlsx', index=False)

# Imprimir o DataFrame com as maiores máximas, menores mínimas e fechamentos
print("\nTabela de Maiores Máximas, Menores Mínimas e Fechamentos:")
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