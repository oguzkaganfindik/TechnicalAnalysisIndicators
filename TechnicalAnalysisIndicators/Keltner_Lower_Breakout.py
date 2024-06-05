# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
from backtesting import Backtest, Strategy
import warnings

def rma(series, length=None, offset=None, **kwargs):
    """
    Calculates the Relative Moving Average (RMA) of a given close price series.

    Parameters:
    - series: pandas Series containing price data.
    - length (int): The number of periods to consider. Default is 10.
    - offset (int): The offset from the current period. Default is None.
    - **kwargs: Additional keyword arguments.

    Returns:
    - pandas.Series: The Relative Moving Average (RMA) values.
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    alpha = (1.0 / length) if length > 0 else 0.5

    # Calculate Result
    rma = series.ewm(alpha=alpha, min_periods=length).mean()
    return rma

#HLC3 Calculation
def hlc3(high, low, close):
    """
    Calculate the HLC (High-Low-Close) for the given high, low, and close series.
    """
    hlc3=(high + low + close)/3
    return hlc3


def tr(high, low, close):
    """
    Calculates the True Range (TR).

    Args:
    high (pd.Series): High prices.
    low (pd.Series): Low prices.
    close (pd.Series): Closing prices.

    Returns:
    pd.Series: True Range values.
    """
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr

def atr(high, low, close, period=14):
    """
    Calculates the Average True Range (ATR) using high, low, and close prices.

    Args:
    high (pd.Series or list): The high prices.
    low (pd.Series or list): The low prices.
    close (pd.Series or list): The close prices.
    period (int, optional): The period over which the ATR is calculated. Default is 14.

    Returns:
    pd.Series: The Average True Range (ATR) values.
    """
    # Calculate true range (TR)
    true_range = tr(high, low, close)
    atr = rma(true_range,period)
    return atr

def Keltner_Signal(data, window=20, mult=2):
    """
    Calculates the Keltner Channel breakout strategy signals.

    Args:
    data (pd.DataFrame): The input DataFrame containing columns like 'Upper Channel', 'Lower Channel', 'close', 'high', and 'low'.
    window (int): The window size for the Exponential Moving Average (EMA) calculation.
    mult (float): The multiplier for the True Range (TR) to determine the width of the Keltner Channel.

    Returns:
    pd.DataFrame: DataFrame with Keltner Channel breakout signals added.
    """
    df = data.copy()
    df['hlc3'] = hlc3(df['high'], df['low'], df['close'])
    df['tr'] = tr(df['high'], df['low'], df['close'])
    df['atr'] = atr(df['high'], df['low'], df['close'],window)
    df['ema'] = df['hlc3'].ewm(span=window, adjust=False).mean()

    df['Upper Channel'] = df['ema'] + df['atr'] * mult
    df['Lower Channel'] = df['ema'] - df['atr'] * mult

    df['Entry'] = (df['close'] > df['Lower Channel']) & (df['close'].shift(1) < df['Lower Channel'])
    df['Exit'] = (df['close'] > df['Upper Channel']) & (df['close'].shift(1) < df['Upper Channel'])
    return df

class MyStrategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.data['Entry'] == True and not self.position:
            self.buy()

        elif self.data['Exit'] == True:
            self.position.close()


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat', 'Kazanma Oranı','Giriş Sinyali', 'Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for hisse in Hisseler:
    try:
        data = tv.get_hist(symbol=hisse, exchange='BIST', interval=Interval.in_1_hour, n_bars=500)
        data = data.reset_index()
        KeltnerSignal = Keltner_Signal(data,200,5)
        KeltnerSignal.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        KeltnerSignal.set_index('datetime', inplace=True)
        bt = Backtest(KeltnerSignal, MyStrategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy=False
        Sell=False
        Signals = KeltnerSignal.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] ==True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [hisse,Last_Price, round(Stats.loc['Win Rate [%]'], 2), str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True)