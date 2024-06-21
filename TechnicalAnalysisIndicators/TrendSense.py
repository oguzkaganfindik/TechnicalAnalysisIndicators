# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting
# pip install tabulate
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
import warnings
import matplotlib.pyplot as plt
from tabulate import tabulate

warnings.simplefilter(action='ignore', category=FutureWarning)

def ema(series, length):
    return series.ewm(span=length, adjust=False).mean()

def rsi(series, length):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def NQQE(data, length=14, SSF=5):
    df = data.copy()
    df['RSI'] = rsi(df['Close'], length)
    df['RSII'] = ema(df['RSI'], SSF)
    df['TR'] = (df['RSII'] - df['RSII'].shift(1)).abs()
    df['wwalpha'] = 1 / length
    df['WWMA'] = df['wwalpha'] * df['TR'] + (1 - df['wwalpha']) * df['TR'].shift(1)
    df['ATRRSI'] = df['wwalpha'] * df['WWMA'] + (1 - df['wwalpha']) * df['WWMA'].shift(1)
    df['QQEF'] = ema(df['RSI'], SSF)
    df['QUP'] = df['QQEF'] + df['ATRRSI'] * 4.236
    df['QDN'] = df['QQEF'] - df['ATRRSI'] * 4.236
    df['QQES'] = 0.0

    for i in range(1, len(df)):
        if df['QUP'][i] < df['QQES'][i-1]:
            df.at[i, 'QQES'] = df['QUP'][i]
        elif df['QQEF'][i] > df['QQES'][i-1] and df['QQEF'][i-1] < df['QQES'][i-1]:
            df.at[i, 'QQES'] = df['QDN'][i]
        elif df['QDN'][i] > df['QQES'][i-1]:
            df.at[i, 'QQES'] = df['QDN'][i]
        elif df['QQEF'][i] < df['QQES'][i-1] and df['QQEF'][i-1] > df['QQES'][i-1]:
            df.at[i, 'QQES'] = df['QUP'][i]
        else:
            df.at[i, 'QQES'] = df['QQES'][i-1]



    df['Colorh'] = np.where(df['QQEF'] - 50 > 10, '#007002', np.where(df['QQEF'] - 50 < -10, 'red', '#E8E81A'))
    df['QQF'] = df['QQEF'] - 50
    df['QQS'] = df['QQES'] - 50
    df['buySignalr'] = (df['QQEF'] > df['QQES'])
    df['sellSignallr'] = (df['QQEF'] < df['QQES'])
    df['Entry'] = df['buySignalr']
    df['Exit'] = df['sellSignallr']

    return df

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat', 'Kazanma Oranı', 'Giriş Sinyali', 'Çıkış Sinyali']

df_signals = pd.DataFrame(columns=Titles)

#Backtest için gerekli class yapısı
class Strategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.data['Entry'] == True and not self.position:
            self.buy()
        elif self.data['Exit'] == True and self.position:
            self.position.close()

for i in range(0, len(Hisseler)):
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=500)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        nqqeTrend = NQQE(data, 14, 5)
        nqqeTrend['datetime'] = pd.to_datetime(nqqeTrend['datetime'])  # Assuming 'datetime' is the name of your datetime column
        nqqeTrend.set_index('datetime', inplace=True)
        bt = Backtest(nqqeTrend, Strategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy = False
        Sell = False
        Signals = nqqeTrend.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] == True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i], Last_Price, round(Stats.loc['Win Rate [%]'], 2), str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except Exception as e:
        print(f"Error processing {Hisseler[i]}: {e}")

df_True = df_signals[df_signals['Giriş Sinyali'] == 'True']

print(tabulate(df_True, headers='keys', tablefmt='grid'))

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df_True.values, colLabels=df_True.columns, cellLoc='center', loc='center')
plt.show()