# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import pandas as pd
import pandas_ta as ta
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def Alpha_Trend(df, mult=1, n1=14):
    df['TR'] = ta.true_range(df['High'],df['Low'],df['Close'])
    df['ATR'] = ta.sma(df['TR'], length=n1)
    df['mfi'] = ta.mfi(df['High'],df['Low'],df['Close'], df['Volume'], length=n1)
    df['upT'] = df['Low'] - df['ATR'] * mult
    df['downT'] = df['High'] + df['ATR'] * mult
    df['AlphaTrend'] = 0.0
    alpha_trend_values = [0.0]

    for i in range(1, len(df)):
        if df['mfi'].iloc[i] >= 50:
            alpha_trend_values.append(max(df['upT'].iloc[i], alpha_trend_values[i-1]))
        else:
            alpha_trend_values.append(min(df['downT'].iloc[i], alpha_trend_values[i-1]))

    df['AlphaTrend'] = alpha_trend_values
    df['Entry']=False
    prev_signal = False
    for i in range(2, len(df)):
        if df.loc[i, 'AlphaTrend'] > df.loc[i-2, 'AlphaTrend']:
            df.loc[i, 'Entry'] = True
            prev_signal = True
        elif df.loc[i, 'AlphaTrend'] == df.loc[i-2, 'AlphaTrend'] and prev_signal:
            df.loc[i, 'Entry'] = True
        else:
            prev_signal = False
    df['Exit'] = df['Entry'] == False
    return df

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat','Kazanma Oranı','Giriş Sinyali', 'Çıkış Sinyali']

df_signals = pd.DataFrame(columns=Titles)

#Backtest için gerekli class yapısı
class Strategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.data['Entry'] == True and not self.position:
            self.buy()

        elif self.data['Exit'] == True:
            self.position.close()

for i in range(0,len(Hisseler)):
    #print(Hisseler[i])
    try:
        mult=1
        n1=14
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=1000)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        AlphaTrend = Alpha_Trend(data,mult,n1)
        AlphaTrend['datetime'] = pd.to_datetime(AlphaTrend['datetime'])
        AlphaTrend.set_index('datetime', inplace=True)
        bt = Backtest(AlphaTrend, Strategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy = False
        Sell = False
        Signals = AlphaTrend.tail(2)
        Signals = Signals.reset_index()
        Buy = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] ==True
        Sell = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i],Last_Price, round(Stats.loc['Win Rate [%]'], 2), str(Buy), str(Sell)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

df_True = df_signals[(df_signals['Giriş Sinyali'] == 'True')]
print(df_True.to_string())