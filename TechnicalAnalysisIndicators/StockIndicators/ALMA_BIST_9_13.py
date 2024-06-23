import os
if os.path.exists('StockIndicators.py'):
    os.remove('StockIndicators.py')

pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener
wget https://raw.githubusercontent.com/oguzkaganfindik/TechnicalAnalysisIndicators/tree/master/TechnicalAnalysisIndicators/StockIndicators/StockIndicators.py

import pandas as pd
import StockIndicators as SI

""" Stocks Komutu Coin için 'BINANCE' Borsa için 'BIST' dir"""
""" TVGet Komutu COIN / HISSE ADI,  BIST / BINANCE , periyotlar ve Periyot Uzunluğu ile çalışır.
            1 - Coin yada Hisse Adı        : İlgili Coin yada Hisse Adı SI.Stocks ile otomatik gelir.
            2 - Exchange                   : Borsa için 'BIST' Coin için 'BINANCE'
            3 - Periyotlar
                Dakikalık                  : 1m, 3m, 5m, 30m, 45m
                Saatlik                    : 1h, 2h, 3h, 4h
                Günlük / Haftalık / Aylık  : 1D, 1W, 1M
            4 - Çekilecek Bar uzunluğu     : 100  (Varsayılan Değer)
            """
Coinler = SI.Stocks('BINANCE')
print(Coinler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Giriş Sinyali', 'Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(Coinler)):
    try:
        data = SI.TVGet(Coinler[i],'BIST','1D',100)
        data['ALMA9'] = SI.alma(data['close'],9)
        data['ALMA13'] = SI.alma(data['close'],13)
        data['Entry'] = data['ALMA9'] > data['ALMA13']
        data['Exit'] = data['ALMA9'] < data['ALMA13']

        Buy = False
        Sell = False
        Signals = data.tail(2)
        Signals = Signals.reset_index()
        last_rows = data.iloc[-2:]
        Buy = (Signals.loc[1,'Entry'] ==True ) and (Signals.loc[0,'Entry'] == False)
        Sell = (Signals.loc[1,'Exit'] ==True ) and (Signals.loc[0,'Exit'] == False)
        Last_Price = Signals.loc[1, 'close']
        L1 = [Coinler[i] ,Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True.to_string())
