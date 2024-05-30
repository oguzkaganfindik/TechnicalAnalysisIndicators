#1
# pip install backtesting
# pip install pandas_ta
# pip install git+https://github.com/rongardF/tvdatafeed

#2
import pandas_ta as ta
from tvDatafeed import TvDatafeed , Interval
from backtesting import Backtest, Strategy

#3
Hisse='XU100'
tv=TvDatafeed()
data= tv.get_hist(symbol=Hisse,exchange='BIST',interval=Interval.in_1_hour,n_bars=5000)
print(data)

#4
data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
print(data)

#5-1
data['RSI']=ta.rsi(data['Close'],14)
print(data)

#5-2
data['Entry']=(data['RSI']<30) & (data['RSI'].shift(1)>30)
data['Exit']=(data['RSI']>70) &(data['RSI'].shift(1)<70)
print(data)

#6
class RSI_Strategy(Strategy):
    def init(self):
        pass

    def next(self):
        if self.data['Entry']==True  and not self.position:
            self.buy()

        elif self.data['Exit']==True :
            self.position.close()
            
##
bt = Backtest(data, RSI_Strategy, cash=100000, commission=0.002)
stats = bt.run()
print(stats)

####
bt.plot(filename='RSI_Strategy')