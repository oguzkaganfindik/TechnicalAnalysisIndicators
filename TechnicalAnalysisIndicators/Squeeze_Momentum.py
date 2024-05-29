# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener

import pandas as pd
import pandas_ta as ta
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def SqueezeMomentum(data,mult=2,length=20,multKC=1.5,lengthKC=20):
    df=data.copy()
    df['basis']=ta.sma(data['Close'],length)
    df['dev']=multKC*ta.stdev(data['Close'],length)
    df['upperBB']=df['basis']+df['dev']
    df['lowerBB']=df['basis']-df['dev']
    df['ma']=ta.sma(df['Close'],lengthKC)
    df['tr0'] = abs(df["High"] - df["Low"])
    df['tr1'] = abs(df["High"] - df["Close"].shift())
    df['tr2'] = abs(df["Low"] - df["Close"].shift())
    df['range'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
    df['rangema']=ta.sma(df['range'],lengthKC)
    df['upperKC']=df['ma']+df['rangema']*multKC
    df['lowerKC']=df['ma']-df['rangema']*multKC
    df['Squeeze'] = (df['lowerBB'] < df['lowerKC']) & (df['upperBB'] > df['upperKC'])
    return df

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat', 'Squeeze']
df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=100)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        Squeeze = SqueezeMomentum(data,2,20,1.5,20)
        Squeeze['datetime'] = pd.to_datetime(Squeeze['datetime'])
        Squeeze.set_index('datetime', inplace=True)
        Signals = Squeeze.tail(2)
        Signals = Signals.reset_index()
        Sq_Signal = Signals.loc[0, 'Squeeze'] == False and Signals.loc[1, 'Squeeze'] ==True

        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i],Last_Price, Sq_Signal]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Squeeze'] == True)]
print(df_True)
