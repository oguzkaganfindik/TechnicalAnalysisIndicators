# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import pandas as pd
import pandas_ta as ta
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def Optimized_Trend_Tracker(data, prt, prc):
    df = data.copy()
    pds = prt
    percent = prc
    alpha = 2 / (pds + 1)

    df['ud1'] = np.where(df['Close'] > df['Close'].shift(1), (df['Close'] - df['Close'].shift()), 0)
    df['dd1'] = np.where(df['Close'] < df['Close'].shift(1), (df['Close'].shift() - df['Close']), 0)
    df['UD'] = df['ud1'].rolling(9).sum()
    df['DD'] = df['dd1'].rolling(9).sum()
    df['CMO'] = ((df['UD'] - df['DD']) / (df['UD'] + df['DD'])).fillna(0).abs()

    df['Var'] = 0.0
    for i in range(pds, len(df)):
        df['Var'].iat[i] = (alpha * df['CMO'].iat[i] * df['Close'].iat[i]) + (1 - alpha * df['CMO'].iat[i]) * df['Var'].iat[i - 1]

    df['fark'] = df['Var'] * percent * 0.01
    df['newlongstop'] = df['Var'] - df['fark']
    df['newshortstop'] = df['Var'] + df['fark']
    df['longstop'] = 0.0
    df['shortstop'] = 999999999999999999

    for i in df['UD']:
        def maxlongstop():
            df.loc[(df['newlongstop'] > df['longstop'].shift(1)), 'longstop'] = df['newlongstop']
            df.loc[(df['longstop'].shift(1) > df['newlongstop']), 'longstop'] = df['longstop'].shift(1)
            return df['longstop']

        def minshortstop():
            df.loc[(df['newshortstop'] < df['shortstop'].shift(1)), 'shortstop'] = df['newshortstop']
            df.loc[(df['shortstop'].shift(1) < df['newshortstop']), 'shortstop'] = df['shortstop'].shift(1)
            return df['shortstop']

        df['longstop'] = np.where(((df['Var'] > df['longstop'].shift(1))), maxlongstop(), df['newlongstop'])
        df['shortstop'] = np.where(((df['Var'] < df['shortstop'].shift(1))), minshortstop(), df['newshortstop'])

    df['xlongstop'] = np.where(((df['Var'].shift(1) > df['longstop'].shift(1)) & (df['Var'] < df['longstop'].shift(1))), 1, 0)
    df['xshortstop'] = np.where(((df['Var'].shift(1) < df['shortstop'].shift(1)) & (df['Var'] > df['shortstop'].shift(1))), 1, 0)

    df['trend'] = 0
    df['dir'] = 0

    for i in df['UD']:
        df['trend'] = np.where(((df['xshortstop'] == 1)), 1, (np.where((df['xlongstop'] == 1), -1, df['trend'].shift(1))))
        df['dir'] = np.where(((df['xshortstop'] == 1)), 1, (np.where((df['xlongstop'] == 1), -1, df['dir'].shift(1).fillna(1))))

    df['MT'] = np.where(df['dir'] == 1, df['longstop'], df['shortstop'])
    df['OTT'] = np.where(df['Var'] > df['MT'], (df['MT'] * (200 + percent) / 200), (df['MT'] * (200 - percent) / 200))

    df = df.round(2)
    df['OTT2'] = df['OTT'].shift(2)
    df['OTT3'] = df['OTT'].shift(3)
    df['Entry'] = df['Var'] > df['OTT2']
    df['Exit'] = df['Var'] < df['OTT2']
    return df


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Giriş Sinyali', 'Çıkış Sinyali']

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
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=100)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        OTT = Optimized_Trend_Tracker(data,2,1.4)
        OTT['datetime'] = pd.to_datetime(OTT['datetime'])  # Assuming 'Date' is the name of your datetime column
        OTT.set_index('datetime', inplace=True)
        Buy = False
        Sell = False
        Signals = OTT.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] == True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i] ,Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True)