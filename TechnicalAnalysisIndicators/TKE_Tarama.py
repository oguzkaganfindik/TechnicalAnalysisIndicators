# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def cci(high, low, close, period=14):
    tp = (high + low + close) / 3
    cci = (tp - tp.rolling(window=period).mean()) / (0.015 * tp.rolling(window=period).std())
    return cci

def williams_r(high, low, close, period=14):
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    wr = -100 * (highest_high - close) / (highest_high - lowest_low)
    return wr

def stochastic_oscillator(high, low, close, period=14, smooth_k=3):
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    stoch_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    stoch_k = stoch_k.rolling(window=smooth_k).mean()  # Smoothing the %K line
    return stoch_k

def mfi(high, low, close, volume, period=14):
    tp = (high + low + close) / 3
    mf = tp * volume
    positive_mf = (mf * (tp > tp.shift(1))).rolling(window=period).sum()
    negative_mf = (mf * (tp < tp.shift(1))).rolling(window=period).sum()
    mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
    return mfi

def ultimate_oscillator(high, low, close, period1=7, period2=14, period3=28):
    def average(bp, tr, length):
        return bp.rolling(window=length).sum() / tr.rolling(window=length).sum()

    bp = close - low.rolling(window=period1).min()
    tr = high.rolling(window=period1).max() - low.rolling(window=period1).min()
    avg7 = average(bp, tr, period1)

    bp = close - low.rolling(window=period2).min()
    tr = high.rolling(window=period2).max() - low.rolling(window=period2).min()
    avg14 = average(bp, tr, period2)

    bp = close - low.rolling(window=period3).min()
    tr = high.rolling(window=period3).max() - low.rolling(window=period3).min()
    avg28 = average(bp, tr, period3)

    uo = 100 * (4 * avg7 + 2 * avg14 + avg28) / 7
    return uo

def custom_indicator(df, period=14, emaperiod=5, novolumedata=False):
    df['Momentum'] = (df['Close'] / df['Close'].shift(period)) * 100
    df['CCI'] = cci(df['High'], df['Low'], df['Close'], period)
    df['RSI'] = rsi(df['Close'], period)
    df['WILLR'] = williams_r(df['High'], df['Low'], df['Close'], period)
    df['STOCH'] = stochastic_oscillator(df['High'], df['Low'], df['Close'], period)

    tp = (df['High'] + df['Low'] + df['Close']) / 3
    upper_s = ((df['Volume'] * (tp.diff() <= 0) * tp).rolling(window=period).sum())
    lower_s = ((df['Volume'] * (tp.diff() >= 0) * tp).rolling(window=period).sum())
    df['MFI'] = 100 - (100 / (1 + upper_s / lower_s))

    df['Ultimate'] = ultimate_oscillator(df['High'], df['Low'], df['Close'], 7, 14, 28)

    if novolumedata:
        df['TKEline'] = (df['Ultimate'] + df['Momentum'] + df['CCI'] + df['RSI'] + df['WILLR'] + df['STOCH']) / 6
    else:
        df['TKEline'] = (df['Ultimate'] + df['MFI'] + df['Momentum'] + df['CCI'] + df['RSI'] + df['WILLR'] + df['STOCH']) / 7

    df['EMAline'] = df['TKEline'].ewm(span=emaperiod, adjust=False).mean()
    return df

# Initialize tvDatafeed
tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

# DataFrame to store results
Titles = ['Hisse Adı', 'Son Fiyat', 'TKE']
df_signals = pd.DataFrame(columns=Titles)

# Process each symbol
for i in range(0, len(Hisseler)):
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_daily, n_bars=100)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        data = custom_indicator(data)
        latest_data = data.iloc[-1]
        if 10 < latest_data['TKEline'] < 20:
            L1 = [Hisseler[i], latest_data['Close'], latest_data['TKEline']]
            df_signals.loc[len(df_signals)] = L1
            print(L1)
    except Exception as e:
        print(f"Error processing {Hisseler[i]}: {e}")

# Print results
print(df_signals.to_string())