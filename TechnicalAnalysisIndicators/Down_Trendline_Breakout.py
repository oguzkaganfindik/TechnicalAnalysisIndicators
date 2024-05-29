﻿# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from tradingview_screener import get_all_symbols
from tvDatafeed import TvDatafeed, Interval
from scipy.stats import linregress

def Down_Trend_Line(data, window=5):
    df = data.iloc[:-window].copy()
    hh_pairs = argrelextrema(df['close'].values, comparator=np.greater, order=window)[0]
    highest_point = df.iloc[hh_pairs].nlargest(1, 'close').sort_values(by='datetime')
    max_idx = data.index.get_loc(highest_point.index[0])
    df_next = df.iloc[max_idx:]

    hh_pairs_next = argrelextrema(df_next['close'].values, comparator=np.greater, order=window)[0]
    slopes = []
    intercepts = []

    # Iterate over each next highest point and calculate the slope
    for hh_next in hh_pairs_next:
        next_hp = df_next.iloc[hh_next]
        slope, intercept, _, _, _ = linregress([highest_point.index[0], next_hp.name], [highest_point['close'].values[0], next_hp['close']])
        # Store the slope
        slopes.append(slope)
        intercepts.append(intercept)

    slopes = [slope for slope in slopes if slope != 0]
    intercepts = [intercept for slope, intercept in zip(slopes, intercepts) if slope != 0]
    if slopes:
        # Find the minimum slope and its corresponding intercept
        min_slope_index = np.argmin(np.abs(slopes))
        min_slope = slopes[min_slope_index]
        min_intercept = intercepts[min_slope_index]
        df = data.copy()
        df['trend'] = min_slope * df.index + min_intercept
        df['Entry'] = df['close'] > df['trend']
    return df

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)


Titles = ['Hisse Adı', 'Son Fiyat' ,'Trend Değeri','Yüzde', 'Yakınlık Durumu','Kırılma Durumu']
df_down_trend = pd.DataFrame(columns=Titles)
for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        order = 5
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_4_hour, n_bars=500)
        data = data.reset_index()
        Trend_line = Down_Trend_Line(data, window=order)
        Entry = False
        Signals = Trend_line.tail(order)
        Signals = Signals.reset_index()
        Last_Price = Signals.loc[order-1, 'close']
        Last_Trend = Signals.loc[order-1, 'trend']
        Last_Perc = ((Signals.loc[order-1,'trend']- Signals.loc[order-1,'close'])/Signals.loc[order-1,'trend'])*100
        Close_Status = False
        Break_Status = False
        if Last_Perc<=5 and Last_Trend>Last_Price:
            Close_Status  = True

        Entry = Signals['Entry'].any() and not Signals['Entry'].all()
        Last_Entry = Signals.loc[order-1,'Entry']
        if Entry==True and Last_Entry==True:
              Break_Status = True

        L1 = [Hisseler[i] ,round(Last_Price,2), round(Last_Trend,2), round(Last_Perc,2),Close_Status,Break_Status]
        print(L1)
        df_down_trend.loc[len(df_down_trend)] = L1
    except:
        pass

df_close = df_down_trend[(df_down_trend['Yakınlık Durumu'] == True)]
df_Breakout = df_down_trend[(df_down_trend['Kırılma Durumu'] == True)]

print('Yakın Olan Hisseler')
print(df_close.to_string())
print('Kırılma Gerçekleşmiş Olanlar')
print(df_Breakout.to_string())