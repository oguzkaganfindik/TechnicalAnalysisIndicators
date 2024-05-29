# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def Ichimoku_Cloud(data, n1=9, n2=26, n3=52, n4=26, n5=26):
    df = data.copy()

    # Conversion Line (Tenkan-sen)
    high1 = df['High'].rolling(window=n1).max()
    low1 = df['Low'].rolling(window=n1).min()
    df['tenkansen'] = (high1 + low1) / 2

    # Base Line (Kijun-sen)
    high2 = df['High'].rolling(window=n2).max()
    low2 = df['Low'].rolling(window=n2).min()
    df['kijunsen'] = (high2 + low2) / 2

    # Leading Span A (Senkou Span A)
    df['senkou_A'] = ((df['tenkansen'] + df['kijunsen']) / 2).shift(n2)

    # Leading Span B (Senkou Span B)
    high3 = df['High'].rolling(window=n3).max()
    low3 = df['Low'].rolling(window=n3).min()
    df['senkou_B'] = ((high3 + low3) / 2).shift(n4)

    # Lagging Span (Chikou Span)
    df['chikou'] = df['Close'].shift(-n5)

    # Kumo Breakout Entry Condition
    df['Entry'] = (df['Close'] > df['senkou_A']) & (df['Close'] > df['senkou_B']) & (df['Close'] > df['kijunsen'])

    # Tenkan-sen/Kijun-sen Cross Entry Condition
    df['Exit'] = (df['Close'] < df['kijunsen'])

    return df

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Giriş Sinyali', 'Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(Hisseler)):
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=500)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        Ichimoku_cloud = Ichimoku_Cloud(data,9,26,52,26,26)
        Ichimoku_cloud['datetime'] = pd.to_datetime(Ichimoku_cloud['datetime'])
        Ichimoku_cloud.set_index('datetime', inplace=True)
        Buy = False
        Sell = False
        Signals = Ichimoku_cloud.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] == True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i],Last_Price,  str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True)