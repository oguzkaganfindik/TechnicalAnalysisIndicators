# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import pandas as pd
import pandas_ta as ta
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def Supertrend(data,SENSITIVITY = 3,ATR_PERIOD = 14):
    df=data.copy()
    df['xATR'] = ta.atr(data['High'], data['Low'], data['Close'], timeperiod=ATR_PERIOD)
    df['nLoss'] = SENSITIVITY * df['xATR']
    # Filling ATRTrailing Variable
    df['ATRTrailing'] = [0.0] + [np.nan for i in range(len(df) - 1)]

    for i in range(1, len(df)):
        if (df.loc[i, 'Close'] > df.loc[i - 1, 'ATRTrailing']) and (df.loc[i - 1, 'Close'] > df.loc[i - 1, 'ATRTrailing']):
            df.loc[i, 'ATRTrailing'] = max(df.loc[i - 1, 'ATRTrailing'],df.loc[i, 'Close']-df.loc[i,'nLoss'])

        elif (df.loc[i, 'Close'] < df.loc[i - 1, 'ATRTrailing']) and (df.loc[i - 1, 'Close'] < df.loc[i - 1, 'ATRTrailing']):
            df.loc[i, 'ATRTrailing'] = min(df.loc[i - 1, 'ATRTrailing'],df.loc[i, 'Close']+df.loc[i,'nLoss'])

        elif df.loc[i, 'Close'] > df.loc[i - 1, 'ATRTrailing']:
            df.loc[i, 'ATRTrailing']=df.loc[i, 'Close']-df.loc[i,'nLoss']
        else:
            df.loc[i, 'ATRTrailing']=df.loc[i, 'Close']+df.loc[i,'nLoss']

    # Calculating signals
    ema = ta.ema(df['Close'], 1)
    df['Above'] = ema > (df['ATRTrailing'])
    df['Below'] = ema < (df['ATRTrailing'])
    df['Entry'] = (df['Close'] > df['ATRTrailing']) & (df['Above']==True)
    df['Exit'] = (df['Close'] < df['ATRTrailing']) & (df['Below']==True)
    return df


#Backtest için gerekli class yapısı
class Strategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.data['Entry'] == True and not self.position:
            self.buy()

        elif self.data['Exit'] == True:
            self.position.close()

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Kazanma Oranı','Giriş Sinyali', 'Çıkış Sinyali']

df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        S=3
        ATR=14
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=500)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        Supert = Supertrend(data,S,ATR)
        Supert['datetime'] = pd.to_datetime(Supert['datetime'])
        Supert.set_index('datetime', inplace=True)
        bt = Backtest(Supert, Strategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy = False
        Sell = False
        Signals = Supert.tail(2)
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