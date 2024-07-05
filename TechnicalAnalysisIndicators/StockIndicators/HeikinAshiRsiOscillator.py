import os
import requests
import pandas as pd
import numpy as np

# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

# StockIndicators.py dosyasını indir ve kaydet
url = "https://raw.githubusercontent.com/oguzkaganfindik/TechnicalAnalysisIndicators/master/TechnicalAnalysisIndicators/StockIndicators/StockIndicators.py"
response = requests.get(url)

with open("StockIndicators.py", "wb") as file:
    file.write(response.content)

print("Dosya indirildi ve kaydedildi.")

# StockIndicators modülünü içe aktar
import StockIndicators as SI

"""exchange Kripto için 'BIST' yerine 'BINANCE' yazın"""

"""Diğer zaman periyotları için
#Dakikalık                  : 1m, 3m, 5m, 30m, 45m
#Saatlik                    : 1h, 2h, 3h, 4h
#Günlük / Haftalık / Aylık  : 1D, 1W, 1M  """

exchange = 'BIST'
periyot = '1D'

datas = SI.Stocks(exchange)
print(datas)

Titles = ['Hisse Adı', 'Son Fiyat', 'Giriş Sinyali', 'Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)


for i in range(len(datas)):
    try:
        data = SI.TVGet(datas[i], exchange, periyot, 200)
        O,H,L,C = SI.HARSI(data,14,1)
        data['Entry'] = C > O
        data['Exit'] = O > C
        Buy = False
        Sell = False
        Signals = data.tail(2).reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] == True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'close']
        L1 = [datas[i], Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except Exception as e:
        print(f"Error processing {datas[i]}: {e}")

df_True = df_signals[df_signals['Giriş Sinyali'] == 'True']
print(df_True.to_string())