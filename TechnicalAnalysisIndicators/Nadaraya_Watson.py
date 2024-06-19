# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Function to calculate Nadaraya-Watson estimator and its envelopes
def nadaraya_watson_envelope(data, bandwidth, mult=3.0):
    df = data.copy()

    def gaussian_kernel(x, bandwidth):
        return np.exp(-0.5 * (x / bandwidth) ** 2) / (bandwidth * np.sqrt(2 * np.pi))

    n = len(df)
    weights = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            weights[i, j] = gaussian_kernel(i - j, bandwidth)
    weights /= weights.sum(axis=1)[:, None]

    nw_estimator = np.dot(weights, df['close'].values)
    nw_estimator_series = pd.Series(nw_estimator, index=df.index)

    # Calculate the scaled absolute error (SAE)
    sae = (df['close'] - nw_estimator_series).abs().rolling(window=n, min_periods=1).mean() * mult

    envelope_upper = nw_estimator_series + sae
    envelope_lower = nw_estimator_series - sae

    df['Mid'] = nw_estimator_series
    df['Lower'] = envelope_lower
    df['Upper'] = envelope_upper

    return df


tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)
print(Hisseler)
#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Potansiyel Giriş Sinyali', 'Potansiyel Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)
for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_daily, n_bars=100)
        data = data.reset_index()
        Nadaraya_Watson = nadaraya_watson_envelope(data,8,3)
        Nadaraya_Watson['datetime'] = pd.to_datetime(Nadaraya_Watson['datetime'])  # Assuming 'Date' is the name of your datetime column
        Nadaraya_Watson.set_index('datetime', inplace=True)

        Buy = False
        Sell = False
        last_row = Nadaraya_Watson.iloc[-1]
        Buy = last_row['Lower'] > last_row['close']
        Sell = last_row['Upper'] < last_row['close']
        Last_Price = last_row['close']
        L1 = [Hisseler[i], Last_Price, str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Potansiyel Giriş Sinyali'] == 'True')]
print(df_True)
