# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import warnings
import pandas as pd
import numpy as np
import pandas_ta as ta
from scipy.signal import argrelextrema
from scipy import stats
from urllib import request
from tvDatafeed import TvDatafeed, Interval
from backtesting import Backtest, Strategy
from tradingview_screener import get_all_symbols
warnings.simplefilter(action='ignore', category=FutureWarning)

def rsi_divergence(data, window, order):
    df = data.iloc[:-1].copy()
    #calculating RSI with talib
    df['RSI']=ta.rsi(df['Close'], window)
    hh_pairs=argrelextrema(df['Close'].values, comparator=np.greater, order=order)[0]
    hh_pairs=[hh_pairs[i:i+2] for i in range(len(hh_pairs)-1)]
    ll_pairs=argrelextrema(df['Close'].values, comparator=np.less, order=order)[0]
    ll_pairs=[ll_pairs[i:i+2] for i in range(len(ll_pairs)-1)]

    bear_div=[]
    bull_div=[]

    for p in hh_pairs:
        x_price=p
        y_price=[df['Close'].iloc[p[0]], df['Close'].iloc[p[1]]]
        slope_price=stats.linregress(x_price, y_price).slope
        x_rsi=p
        y_rsi=[df['RSI'].iloc[p[0]], df['RSI'].iloc[p[1]]]
        slope_rsi=stats.linregress(x_rsi, y_rsi).slope

        if slope_price>0:
            if np.sign(slope_price)!=np.sign(slope_rsi):
                bear_div.append(p)

    for p in ll_pairs:
        x_price=p
        y_price=[df['Close'].iloc[p[0]], df['Close'].iloc[p[1]]]
        slope_price=stats.linregress(x_price, y_price).slope
        x_rsi=p
        y_rsi=[df['RSI'].iloc[p[0]], df['RSI'].iloc[p[1]]]
        slope_rsi=stats.linregress(x_rsi, y_rsi).slope

        if slope_price<0:
            if np.sign(slope_price)!=np.sign(slope_rsi):
                bull_div.append(p)

    bear_points=[df.index[a[1]] for a in bear_div]
    bull_points=[df.index[a[1]] for a in bull_div]
    pos=[]

    for idx in df.index:
        if idx in bear_points:
            pos.append(-1)
        elif idx in bull_points:
            pos.append(1)
        else:
            pos.append(0)

    df['position']=pos
    df['position']=df['position'].replace(0, method='ffill')
    return df


class Strategy(Strategy):
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

for i in range(0,len(Hisseler)):
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_1_hour, n_bars=500)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        RSIDiv=rsi_divergence(data,14,1)
        RSIDiv['datetime'] = pd.to_datetime(RSIDiv['datetime'])  # Assuming 'Date' is the name of your datetime column
        RSIDiv.set_index('datetime', inplace=True)
        RSIDiv['Entry'] = (RSIDiv['position'] == 1)
        RSIDiv['Exit'] = (RSIDiv['position'] == -1)
        bt = Backtest(RSIDiv, Strategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy=False
        Sell=False
        Signals = RSIDiv.tail(2)
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
print(df_True)