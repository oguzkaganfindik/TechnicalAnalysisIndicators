# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings

def ehlers_fisher_transform(data, length=10,repaint=False):
    # Calculate the highest and lowest values for the given length
    df = data.copy()

    df['maxSrc'] = df['close'].rolling(window=length).max()
    df['minSrc'] = df['close'].rolling(window=length).min()

    # Calculate the stochastic oscillator
    df['sto'] = np.where(df['maxSrc'] - df['minSrc'] != 0,
                         (df['close'] - df['minSrc']) / (df['maxSrc'] - df['minSrc']), 0)

    # Initialize v1 and fish columns
    df['v1'] = 0.0
    df['fish'] = 0.0

    # Calculate v1 and fish values
    for i in range(length, len(df)):
        v1_prev = df.at[i-1, 'v1']
        v1_new = max(min((0.33 * 2 * (df.at[i, 'sto'] - 0.5)) + (0.67 * v1_prev), 0.999), -0.999)
        df.at[i, 'v1'] = v1_new

        fish_prev = df.at[i-1, 'fish']
        fish_new = (0.5 * np.log((1 + v1_new) / (1 - v1_new))) + (0.5 * fish_prev)
        df.at[i, 'fish'] = fish_new
    if repaint == False:
        df['fish'] = df['fish'].shift(1)

    # Generate signals
    df['Entry'] = df['fish'] > df['fish'].shift(1)
    df['Exit'] = df['fish'] < df['fish'].shift(1)
    return df



tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat', 'Giriş Sinyali', 'Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for hisse in Hisseler:
    try:
        data = tv.get_hist(symbol=hisse, exchange='BIST', interval=Interval.in_weekly, n_bars=500)
        data = data.reset_index()
        FisherSignal = ehlers_fisher_transform(data,9, True)
        FisherSignal.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        FisherSignal.set_index('datetime', inplace=True)

        Buy=False
        Sell=False
        Signals = FisherSignal.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] ==True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [hisse,Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True)