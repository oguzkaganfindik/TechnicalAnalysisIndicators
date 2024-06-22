# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def alma(series, window=20, sigma=6, offset=0.85):
    """
    Calculate the Arnaud Legoux Moving Average (ALMA) for a given series.

    :param series: pandas Series of prices.
    :param window: int, window length for the moving average.
    :param sigma: float, standard deviation for the Gaussian distribution.
    :param offset: float, offset for the Gaussian distribution.
    :return: pandas Series with the ALMA values.
    """
    m = (window - 1) * offset
    s = window / sigma

    def gaussian_weight(x, m, s):
        return np.exp(-((x - m) ** 2) / (2 * s ** 2))

    weights = np.array([gaussian_weight(i, m, s) for i in range(window)])
    weights /= np.sum(weights)

    alma = series.rolling(window=window).apply(lambda x: np.dot(x, weights), raw=True)
    return alma


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
print(Hisseler)
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

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
        data['ALMA'] = alma(data['close'],20,6,0.85)
        data['datetime'] = pd.to_datetime(data['datetime'])
        data.set_index('datetime', inplace=True)
        Buy = False
        Sell = False
        Signals = data.tail(2)
        Signals = Signals.reset_index()
        last_rows = data.iloc[-2:]
        Buy = (Signals.loc[1,'close'] > Signals.loc[1,'ALMA']) and (Signals.loc[0,'close'] < Signals.loc[0,'ALMA'])
        Sell = (Signals.loc[1,'close'] < Signals.loc[1,'ALMA']) and (Signals.loc[0,'close'] > Signals.loc[0,'ALMA'])
        Last_Price = Signals.loc[1, 'close']
        L1 = [Hisseler[i] ,Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True.to_string())