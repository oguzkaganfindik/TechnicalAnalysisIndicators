# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
from backtesting import Backtest, Strategy
import warnings

def lpsar(high, low, close, initial_af=0.02, step_af=0.02, max_af=0.2):
    """
    Calculates the Lucid Parabolic SAR (Lucid PSAR).

    Args:
    high (pd.Series): High prices.
    low (pd.Series): Low prices.
    close (pd.Series): Close prices.
    initial_af (float, optional): The initial acceleration factor. Default is 0.02.
    step_af (float, optional): The step acceleration factor. Default is 0.02.
    max_af (float, optional): The maximum acceleration factor. Default is 0.2.

    Returns:
    pd.Series: The Lucid PSAR values.
    """
    lpsar = pd.Series(index=high.index)
    lpsar[0] = close[0]
    uptrend = True
    af = initial_af
    ep = high[0]

    for i in range(1, len(high)):
        previous_lpsar = lpsar[i - 1]
        previous_high = high[i - 1]
        previous_low = low[i - 1]

        if uptrend:
            lpsar[i] = previous_lpsar + af * (ep - previous_lpsar)
            if low[i] < lpsar[i]:
                uptrend = False
                lpsar[i] = ep
                af = initial_af
                ep = low[i]
            else:
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + step_af, max_af)
                lpsar[i] = min(lpsar[i], previous_low, low[i])
        else:
            lpsar[i] = previous_lpsar + af * (ep - previous_lpsar)
            if high[i] > lpsar[i]:
                uptrend = True
                lpsar[i] = ep
                af = initial_af
                ep = high[i]
            else:
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + step_af, max_af)
                lpsar[i] = max(lpsar[i], previous_high, high[i])

    return lpsar

#Parabolic SAR Signal
def Psar_Signal(data,initial_af=0.02,step_af=0.02,max_af=0.2):
    df=data.copy()
    #Parabolic Stop and Reverse (PSAR)
    parabolic=lpsar(df['high'],df['low'],df['close'],initial_af,step_af,max_af)
    df['Entry'] = df['close'] > parabolic
    df['Exit'] = df['close'] < parabolic
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
        data = tv.get_hist(symbol=hisse, exchange='BIST', interval=Interval.in_1_hour, n_bars=1000)
        data = data.reset_index()
        PsarSignal = Psar_Signal(data)
        PsarSignal.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        PsarSignal.set_index('datetime', inplace=True)
        bt = Backtest(PsarSignal, MyStrategy, cash=100000, commission=0.002)
        Stats = bt.run()
        Buy=False
        Sell=False
        Signals = PsarSignal.tail(2)
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