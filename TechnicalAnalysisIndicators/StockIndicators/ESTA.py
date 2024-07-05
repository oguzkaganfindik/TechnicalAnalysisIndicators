import os
import requests
import pandas as pd

# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

# StockIndicators.py dosyasını indir ve kaydet
url = "https://raw.githubusercontent.com/oguzkaganfindik/TechnicalAnalysisIndicators/master/TechnicalAnalysisIndicators/StockIndicators/StockIndicators.py"
response = requests.get(url)

with open("StockIndicators.py", "wb") as file:
    file.write(response.content)

print("Dosya indirildi ve kaydedildi.")

# StockIndicators modülünü içe aktar
import StockIndicators as SI
from backtesting import Backtest, Strategy
exchange = 'BIST'
periyot = '1D'

datas = SI.Stocks(exchange)
print(datas)

Titles = ['Hisse Adı', 'Son Fiyat', 'Başarı Oranı','Son Durum']
df_signals = pd.DataFrame(columns=Titles)

#Backtest için gerekli class yapısı
class Strategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.data['Entry'] == True and not self.position:
            self.buy()

        elif self.data['Exit'] == True:
            self.position.close()

for i in range(0, len(datas)):
     #print(datas[i])
     try:
        # Input parameters
        k_period = 34
        fast_period = 3
        slow_period = 5
        signal_period = 2
        atr_multiplier = 2.2
        atr_period = 17
        tp1 = 10 / 100
        tp2 = 20 / 100

        data = SI.TVGet(datas[i], exchange, periyot, 1000)
        ESTA = SI.ESTA(data,k_period,fast_period,slow_period,signal_period,atr_multiplier,atr_period,tp1,tp2)
        ESTA.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        ESTA['datetime'] = pd.to_datetime(ESTA['datetime'])
        ESTA.set_index('datetime', inplace=True)
        bt = Backtest(ESTA, Strategy, cash=100000, commission=0.001)
        Stats = bt.run()
        Signals = ESTA.tail(1)
        Last_Price = Signals.iloc[0]['Close']
        Status = Signals.iloc[0]['Trade']
        L1 = [datas[i], Last_Price,round(Stats.loc['Win Rate [%]'], 2), Status]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
     except Exception as e:
        print(f"An error occurred for stock {datas[i]}: {e}")

df_True = df_signals[df_signals['Son Durum'] == 'AL']

print(df_True.to_string())