# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Function to calculate Nadaraya-Watson estimator and its envelopes
def kama(series, length=21, fast_end=0.666, slow_end=0.0645, offset=None, **kwargs):
    """
    Calculates the Kaufman Adaptive Moving Average (KAMA) of a given price series.

    Parameters:
    - series: pandas Series containing price data.
    - length (int): The number of periods to consider for the efficiency ratio. Default is 21.
    - fast_end (float): The smoothing constant for the fastest EMA. Default is 0.666.
    - slow_end (float): The smoothing constant for the slowest EMA. Default is 0.0645.
    - offset (int): The offset from the current period. Default is None.
    - **kwargs: Additional keyword arguments.

    Returns:
    - pandas.Series: The Kaufman Adaptive Moving Average (KAMA) values.
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 21
    fast_end = float(fast_end) if fast_end else 0.666
    slow_end = float(slow_end) if slow_end else 0.0645
    offset = int(offset) if offset else 0

    # Calculate Efficiency Ratio (ER)
    price_diff = series.diff(1).abs()
    signal = series.diff(length).abs()
    noise = price_diff.rolling(window=length).sum()
    er = signal / noise
    er.replace([np.inf, -np.inf], 0, inplace=True)  # Handle division by zero

    # Calculate Smoothing Constant (SC)
    sc = (er * (fast_end - slow_end) + slow_end) ** 2

    # Calculate KAMA
    kama = pd.Series(np.zeros(len(series)), index=series.index)
    kama.iloc[length - 1] = series.iloc[length - 1]  # Set initial value

    for i in range(length, len(series)):
        kama.iloc[i] = kama.iloc[i - 1] + sc.iloc[i] * (series.iloc[i] - kama.iloc[i - 1])

    # Apply offset if needed
    if offset != 0:
        kama = kama.shift(offset)

    return kama


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)
print(Hisseler)

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
        data['KAMA'] = kama(data['close'],21)
        data['datetime'] = pd.to_datetime(data['datetime'])
        Buy = False
        Sell = False
        Signals = data.tail(2)
        Signals = Signals.reset_index()
        last_rows = data.iloc[-2:]
        Buy = (Signals.loc[1,'close'] > Signals.loc[1,'KAMA']) and (Signals.loc[0,'close'] < Signals.loc[0,'KAMA'])
        Sell = (Signals.loc[1,'close'] < Signals.loc[1,'KAMA']) and (Signals.loc[0,'close'] > Signals.loc[0,'KAMA'])
        Last_Price = Signals.loc[1,'close']
        L1 = [Hisseler[i], Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True)
