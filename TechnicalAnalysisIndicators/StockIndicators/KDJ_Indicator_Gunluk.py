﻿import os
import requests
import pandas as pd

# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

# StockIndicators.py dosyasını indir ve kaydet
url = "https://raw.githubusercontent.com/oguzkaganfindik/TechnicalAnalysisIndicators/master/TechnicalAnalysisIndicators/StockIndicators/StockIndicators.py"
response = requests.get(url)

with open("StockIndicators.py", "wb") as file:
    file.write(response.content)

print("Dosya indirildi ve kaydedildi.")

# StockIndicators modülünü içe aktar
import StockIndicators as SI

exchange = 'BIST'           #Kripto için 'BINANCE' yazın
periyot = '1D'              #Diğer zaman dilimleri için
                            #Dakikalık                  : 1m, 3m, 5m, 30m, 45m
                            #Saatlik                    : 1h, 2h, 3h, 4h
                            #Günlük / Haftalık / Aylık  : 1D, 1W, 1M

datas = SI.Stocks(exchange)
print(datas)


Titles = ['Hisse Adı', 'Son Fiyat','Cross']
df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(datas)):
    try:
        data = SI.TVGet(datas[i],exchange,periyot,100)
        data['KDJ'] = SI.kdj_indicator(data['high'],data['low'],data['close'])
        Buy = False
        Signals = data.tail(2)
        Signals = Signals.reset_index()
        KDJ1 = Signals.loc[0,'KDJ']
        KDJ2 = Signals.loc[1,'KDJ']
        Buy = (KDJ2 > 0) and (KDJ1 < 0)
        Last_Price = Signals.loc[1, 'close']
        L1 = [datas[i] ,Last_Price,str(Buy)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Cross'] == 'True')]
print(df_True.to_string())