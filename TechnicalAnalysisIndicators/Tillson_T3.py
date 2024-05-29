# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import pandas as pd
import pandas_ta as ta
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Tillson onay için sinyal 2 bar gecikmeli
def TillsonT3(data, Length=14, vf=0.7,app=2):
    df = data.copy()

    ema_first_input = (df['High'] + df['Low'] + 2 * df['Close']) / 4
    e1 = ta.ema(ema_first_input, Length)
    e2 = ta.ema(e1, Length)
    e3 = ta.ema(e2, Length)
    e4 = ta.ema(e3, Length)
    e5 = ta.ema(e4, Length)
    e6 = ta.ema(e5, Length)

    c1 = -1 * vf * vf * vf
    c2 = 3 * vf * vf + 3 * vf * vf * vf
    c3 = -6 * vf * vf - 3 * vf - 3 * vf * vf * vf
    c4 = 1 + 3 * vf + vf * vf * vf + 3 * vf * vf
    df['T3'] = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3
    df['Entry'] = False
    df['Exit'] = False
    df['Entry']=df['T3'] > df['T3'].shift(1)
    df['Exit']=df['T3'] < df['T3'].shift(1)

    df['Entry']=(df['Entry'] & df['Entry'].shift(app))
    df['Exit']=(df['Exit'] & df['Exit'].shift(app))
    return df


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Kazanma Oranı','Giriş Sinyali', 'Çıkış Sinyali']

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

for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=500)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        Tillson=TillsonT3(data,2,14,2)    #Sondaki 2 Gecikmeli sinyal sayısı Tillson Onayı için önemli
        Tillson['datetime'] = pd.to_datetime(Tillson['datetime'])
        Tillson.set_index('datetime', inplace=True)
        bt = Backtest(Tillson, Strategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy = False
        Sell = False
        Signals = Tillson.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] ==True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i],Last_Price, round(Stats.loc['Win Rate [%]'], 2), str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True)