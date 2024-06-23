# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
print(Hisseler)
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

# Define custom functions for weighted moving average (WMA) and standard deviation (STDEV)
def wma(series, length):
    weights = np.arange(1, length + 1)
    return series.rolling(length).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

def stdev(series, length):
    deviation = series.rolling(window=length).std()
    return deviation

# Define the SmoothAndLazyMA (SALMA) calculation function
def SALMA(series, length=10, smooth=3, mult=0.3, sd_len=5):
    baseline = wma(series, sd_len)
    dev = mult * stdev(series, sd_len)
    upper = baseline + dev
    lower = baseline - dev
    cprice = np.where(series > upper, upper, np.where(series < lower, lower, series))
    cprice = pd.Series(cprice)
    REMA = wma(wma(cprice, length), smooth)
    return REMA

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Giriş Sinyali', 'Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_weekly, n_bars=100)
        # Interval.in_1_minute  
        # Interval.in_3_minute  
        # Interval.in_5_minute   
        # Interval.in_15_minute  
        # Interval.in_30_minute  
        # Interval.in_45_minute  
        # Interval.in_1_hour  
        # Interval.in_2_hour  
        # Interval.in_3_hour  
        # Interval.in_4_hour  
        # Interval.in_daily 
        # Interval.in_weekly  
        # Interval.in_monthly
        data = data.reset_index()
        data['SALMA'] = SALMA(pd.Series(data['close']))
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['Entry'] = data['SALMA'] > data['SALMA'].shift(1)
        data['Exit'] = data['SALMA'] < data['SALMA'].shift(1)
        data.set_index('datetime', inplace=True)
        Buy = False
        Sell = False
        Signals = data.tail(2)
        Signals = Signals.reset_index()
        last_rows = data.iloc[-2:]
        Buy = (Signals.loc[1,'Entry'] ==True ) and (Signals.loc[0,'Entry'] == False)
        Sell = (Signals.loc[1,'Exit'] ==True ) and (Signals.loc[0,'Exit'] == False)
        Last_Price = Signals.loc[1, 'close']
        L1 = [Hisseler[i] ,Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True.to_string())
