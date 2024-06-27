# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import warnings

warnings.simplefilter(action='ignore')

# Standart Moving Average
def sma(series, length):
    """
    Calculate the Simple Moving Average (SMA) for a given series.
    """
    return series.rolling(window=length).mean()

# Exponential Moving Average
def ema(series, length):
    """
    Calculate the Exponential Moving Average (EMA) for a given series.
    """
    return series.ewm(span=length, adjust=False).mean()

def Bankery(data):
    df = data.copy()
    close_minus_rolling_min = data['close'] - pd.Series(data['low']).rolling(window=27).min()
    percentage_change = close_minus_rolling_min / (pd.Series(data['high']).rolling(window=27).max() - pd.Series(data['low']).rolling(window=27).min()) * 100

    sma1 = sma(percentage_change, 5)
    sma2 = sma(sma1, 3)

    fundtrend = (3 * sma1 - 2 * sma2 - 50) * 1.032 + 50

    typ = (2 * data['close'] + data['high'] + data['low'] + data['open']) / 5
    lol = pd.Series(data['low']).rolling(window=34).min()
    hoh = pd.Series(data['high']).rolling(window=34).max()
    bullbearline = ema((typ - lol) / (hoh - lol) * 100, 13)
    bankerentry = (fundtrend > bullbearline) & (bullbearline < 25)
    df['Entry'] = (bankerentry == True)
    return df

# TradingView verisini çekme
tv = TvDatafeed(username='your_username', password='your_password')
symbols = ["BTCUSDT", "XRPUSDT", "ETHUSDT",
             "AVAXUSDT", "ARKUSDT", "ARKMTUSD", "ARBTUSD", "AGIXUSDT", "ATOMUSDT","ATMUSDT", "ASRUSDT","ARPAUSDT","API3USDT","APEUSDT",
             "ANKRUSDT","AMPUSDT", "ALTUSDT", "ALICEUSDT","ALGOUSDT","AIUSDT", "ADAUSDT","ACMUSDT","ACHUSDT","ACEUSDT","ACAUSDT",

             "AXLUSDT", "AEVOUSDT", "ALTUSDT","APTUSDT", "ADAUSDT","ALGOUSDT", "AIUSDT","AXLUSDT","AUDIOUSDT",
             "BONKUSDT", "BNBUSDT","BSWUSDT", "BOMEUSDT","BNXUSDT","BLURUSDT","BELUSDT","BCHUSDT","BARUSDT","BANDUSDT","BAKEUSDT",
             "COMPUSDT","CHZUSDT", "CFXUSDT","CYBERUSDT","CRVUSDT","COTIUSDT","COSUSDT","COMBOUSDT","CKBUSDT","CITYUSDT","CAKEUSDT",
             "DOGEUSDT", "DOTUSDT", "DYDXUSDT","DYMUSDT","DODOUSDT","DENTUSDT","DARUSDT",
             "ETHFIUSDT", "EDUUSDT","ETHUSDT","ETCUSDT","EOSUSDT","ENSUSDT","ENJUSDT",
             "FETUSDT", "FTMUSDT","FLOKIUSDT","FRONTUSDT","FILUSDT","FIDAUSDT",
             "GRTUSDT","GMTUSDT","GASUSDT","GALAUSDT",
             "HOTUSDT","HBARUSDT",
             "IMXUSDT","ICPUSDT","IOTAUSDT", "IDUSDT", "INJUSDT",
             "JUVUSDT", "JUPUSDT","JTOUSDT","JOEUSDT","JASMYUSDT",
             "LUNCUSDT","LDOUSDT", "LINKUSDT", "LAZIOUSDT","LEVERUSDT","LITUSDT","LPTUSDT","LOOMUSDT","LRCUSDT","LTCUSDT","LUNAUSDT",

             "MANTAUSDT", "MATICUSDT","MBOXUSDT", "MAVUSDT", "MANAUSDT","MINAUSDT", "MEMEUSDT","MAGICUSDT","METISUSDT","MKRUSDT","MOVRUSDT",
             "MTLUSDT",
             "NTRNUSDT", "NEARUSDT","NEOUSDT", "NFPUSDT",
             "PEPEUSDT","PORTALUSDT", "PIXELUSDT","PYTHUSDT","PAXGUSDT","PENDLEUSDT","PORTOUSDT","PSGUSDT",
             "OPUSDT","OCEANUSDT","OGUSDT","OGNUSDT","OMUSDT","ONEUSDT","ONTUSDT","ORDIUSDT",
             "RNDRUSDT","RADUSDT","RAREUSDT","RAYUSDT","REEFUSDT","ROSEUSDT","RUNEUSDT","RVNUSDT",
             "SOLUSDT", "SHIBUSDT","SKLUSDT","STRKUSDT", "SXPUSDT","SEIUSDT", "SUIUSDT","SANDUSDT", "SANTOSUSDT", "SEIUSDT","SLPUSDT",
             "SNXUSDT", "SPELLUSDT","STORJUSDT","STRAXUSDT","STXUSDT","SUPERUSDT",

             "THETAUSDT","TIAUSDT","TLMUSDT","TRBUSDT","TWTUSDT",
             "XAIUSDT", "XECUSDT","XLMUSDT","XTZUSDT","XVGUSDT","XVSUSDT",
             "UMAUSDT", "UNIUSDT", "UNFIUSDT",
             "VANRYUSDT", "VETUSDT","VICUSDT",
             "ZILUSDT",
             "WLDUSDT" ,  "WIFUSDT"]
exchange = 'BINANCE'

# Raporlama için kullanılacak başlıklar
Titles = ['Kripto Çifti', 'Son Fiyat', 'Dip Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for symbol in symbols:
    try:
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=100)
        data = data.reset_index()
        Banker = Bankery(data)
        Banker.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        Banker.set_index('datetime', inplace=True)
        Buy = False
        Signals = Banker.tail(2)
        Signals = Signals.reset_index()

        Entry = (Signals.loc[0, 'Entry'] == False) & (Signals.loc[1, 'Entry'] == True)
        Last_Price = Signals.loc[1, 'Close']
        L1 = [symbol, Last_Price, Entry]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

df_True = df_signals[(df_signals['Dip Sinyali'] == True)]
print(df_True)

     