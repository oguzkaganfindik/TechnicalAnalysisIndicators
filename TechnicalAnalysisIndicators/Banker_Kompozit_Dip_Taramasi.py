# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener  backtesting

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
from backtesting import Backtest, Strategy
import warnings

warnings.simplefilter(action='ignore')


def xsa(src, length, weight):
    sumf = np.zeros_like(src)
    ma = np.zeros_like(src)
    out = np.zeros_like(src)

    for i in range(length,len(src)):
        sumf[i] = np.nan_to_num(sumf[i - 1]) - np.nan_to_num(src[i - length]) + src[i]
        ma[i] = np.nan if np.isnan(src[i - length]) else sumf[i] / length
        out[i] = ma[i] if np.isnan(out[i - 1]) else (src[i] * weight + out[i - 1] * (length - weight)) / length

    return out

def ema(src, span):
    return src.ewm(span=span, adjust=False).mean()

def Banker_Fund_Trend(data):
    df = data.copy()
    close = df['close']
    low = df['low']
    high = df['high']
    open_ = df['open']
    fundtrend =np.zeros_like(close)
    part_1 = (close - low.rolling(window=27).min()) / (high.rolling(window=27).max() - low.rolling(window=27).min()) * 100
    fundtrend = ((3 * xsa(part_1, 5, 1) - 2 * xsa(xsa(part_1, 5, 1), 3, 1) - 50) * 1.032 + 50)

    typ = (2 * close + high + low + open_) / 5
    lol = low.rolling(window=34).min()
    hoh = high.rolling(window=34).max()

    bullbearline = ema((typ - lol) / (hoh - lol) * 100, 13)
    bankerentry = (fundtrend > bullbearline) & (bullbearline < 25)

    df['fundtrend'] = fundtrend
    df['bullbearline'] = bullbearline
    df['bankerentry'] = bankerentry.astype(int)  # Convert to integer

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
        data = tv.get_hist(symbol=hisse, exchange='BIST', interval=Interval.in_daily, n_bars=100)
        dataref = tv.get_hist(symbol='XU100', exchange='BIST', interval=Interval.in_daily, n_bars=100)
        data = data.reset_index()
        dataref = dataref.reset_index()
        result = data.copy()
        columns_to_divide = ['open', 'high', 'low', 'close', 'volume']
        for column in columns_to_divide:
            result[column] = 100*(data[column] / dataref[column])
        Banker = Banker_Fund_Trend(result)
        Banker.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        Banker.set_index('datetime', inplace=True)

        Buy=False
        Signals = Banker.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'bankerentry'] == False and Signals.loc[1, 'bankerentry'] ==True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [hisse,round(Last_Price,2), Buy]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Dip Sinyali'] == True)]
print(df_True)