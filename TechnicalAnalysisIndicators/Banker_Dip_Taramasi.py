﻿# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings

warnings.simplefilter(action='ignore')

#Standart Moving Average
def sma(series, length):
    """
    Calculate the Simple Moving Average (SMA) for a given series.
    """
    return series.rolling(window=length).mean()

#Exponential Moving Average
def ema(series, length):
    """
    Calculate the Exponential Moving Average (EMA) for a given series.
    """
    return series.ewm(span=length, adjust=False).mean()


def Bankery(data):
    df=data.copy()
    close_minus_rolling_min = data['close'] - pd.Series(data['low']).rolling(window=27).min()
    percentage_change = close_minus_rolling_min / (pd.Series(data['high']).rolling(window=27).max() - pd.Series(data['low']).rolling(window=27).min()) * 100

    sma1 = sma(percentage_change, 5)
    sma2 = sma(sma1, 3)

    fundtrend = (3 * sma1 - 2 * sma2 - 50) * 1.032 + 50

    typ = (2 * data['close'] + data['high'] + data['low'] + data['open']) / 5
    lol = pd.Series(data['low']).rolling(window=34).min()
    hoh = pd.Series(data['high']).rolling(window=34).max()
    bullbearline = ema((typ - lol) / (hoh - lol) * 100, 13)
    bankerentry = (fundtrend > bullbearline) & (bullbearline < 25)
    df['Entry'] = (bankerentry==True)
    return df


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)


#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Dip Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for hisse in Hisseler:
    try:
        data = tv.get_hist(symbol=hisse, exchange='BIST', interval=Interval.in_1_hour, n_bars=100)
        data = data.reset_index()
        Banker = Bankery(data)
        Banker.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        Banker.set_index('datetime', inplace=True)
        Buy = False
        Signals = Banker.tail(2)
        Signals = Signals.reset_index()

        Entry = (Signals.loc[0, 'Entry'] == False) & (Signals.loc[1, 'Entry'] == True)
        Last_Price = Signals.loc[1, 'Close']
        L1 = [hisse, Last_Price,Entry]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Dip Sinyali'] == True)]
print(df_True)