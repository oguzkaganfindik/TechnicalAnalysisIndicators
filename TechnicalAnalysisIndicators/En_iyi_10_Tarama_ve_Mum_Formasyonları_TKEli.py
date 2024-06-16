# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import Query, Column
import warnings
from datetime import datetime

def Tarama_1(val):
    """Bu Tarama Günlük Periyotta
    Açılış Fiyatı Güncel Fiyatın Altında
    RSI 30 ila 40 arasında
    MACD Yukarı keser MACD Sinyal
    MACD Sinyal < 0
    Taramasıdır.
    #RSI 30 seviyesinin üzerinde al verirken Macd 0 'ın altında al veren #bist hisselerinin taraması
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('RSI'+ str(val)).between(30,40),
                    Column('change').between(0,9.5),
                    Column('MACD.macd'+ str(val)).crosses_above(Column('MACD.signal'+ str(val))),
                    Column('MACD.signal'+ str(val)) < 0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_2(val):
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.5
    Üstel Haraketli Ortalama 5 < Fiyat
    Üstel Haraketli Ortalama 20 < Üstel Haraketli Ortalama 5
    Üstel Haraketli Ortalama 50 < Üstel Haraketli Ortalama 20
    MACD > MACD Sinyal
    Parabolik SAR Aşağı Keser Fiyat
    Emtia Kanal Endeksi >=90
    Taramasıdır.
    #Alternatif Düşeni kıran #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc'+ str(val)) > 1.0,
                    Column('EMA5'+ str(val)) < Column('close'),
                    Column('EMA20'+ str(val)) < Column('EMA5'+ str(val)),
                    Column('EMA50'+ str(val)) < Column('EMA20'+ str(val)),
                    Column('MACD.macd'+ str(val)) > Column('MACD.signal'+ str(val)),
                    Column('P.SAR'+ str(val)).crosses_below(Column('close')),
                    Column('CCI20'+ str(val)) >= 90.0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_3(val):
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.0
    Fiyat >= Basit Haraketli Ortalama 5
    Basit Haraketli Ortalama 10 > Basit Haraketli Ortalama20
    Macd Yukarı Keser MACD Sinyali
    Taramasıdır.
    #Swing Trade 2 nolu stratejisine uyan #bist hisselerinin taraması olarakda bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc'+ str(val)) > 1.0,
                    Column('close') >= Column('SMA5'+ str(val)),
                    Column('SMA10'+ str(val)) >Column('SMA20'+ str(val)),
                    Column('MACD.macd'+ str(val)).crosses_above(Column('MACD.signal'+ str(val)))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_4(val):
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.0
    Macd Yukarı Keser Macd Sinyal
    Stokastik RSI Hızlı Yukarı keser Stokastik RSI Yavaş
    Taramasıdır.
    #Macd ve Stokastik RSI hanüz al vermiş olan #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc'+ str(val)) > 1.0,
                    Column('MACD.macd'+ str(val)).crosses_above(Column('MACD.signal'+ str(val))),
                    Column('Stoch.RSI.K'+ str(val)).crosses_above(Column('Stoch.RSI.D'+ str(val)))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_5(val):
    """Bu Tarama Günlük Periyotta
    Fiyat Yukarı Keser Hull Haraketl Ortalama
    Ortalama Gerçek Aralık 0 ila 10 arasında
    Basit Haraketli Ortalama Aşağı Keser Fiyat
    Taramasıdır.
    #Richards Dennis Kaplumbağası hull9 a göre oalrak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('close').crosses_above('HullMA9'+ str(val)),
                    Column('change') < 9.5,
                    Column('ATR'+ str(val)).between(0,10),
                    Column('SMA20'+ str(val)).crosses_below('close'),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_6(val):
    """Bu Tarama Günlük Periyotta
    RSI14 > 55
    Üstel Hareketli Ortalama 5 < Kapanış Fiyatı
    Üstel Hareketli Ortalama 20 < Basit Hareketli Ortalama 5
    Üstel Hareketli Ortalama 50 < Basit Hareketli Ortalama 20
    Emtia Kanal Endeksi CCI(20)  Yukarı Keser 100
    Hacim x Fiyat > 10 Milyon
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('RSI'+ str(val)) > 55.0,
                    Column('change') < 9.5,
                    Column('EMA5'+ str(val)) < Column('close'),
                    Column('EMA20'+ str(val)) < Column('SMA5'+ str(val)),
                    Column('EMA50'+ str(val)) < Column('SMA20'+ str(val)),
                    Column('CCI20'+ str(val)).crosses_above(100),
                    Column('Value.Traded') > 1E7
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_7(val):
    """
    ADX+CCI Taraması by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W',)
                .where(
                    Column('Perf.W') < 10,
                    Column('change') < 9.5,
                    Column('ADX'+ str(val)) > 20,
                    Column('CCI20'+ str(val)).crosses_above(100),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_8(val):
    """
    MACD + Stokastik RSI Kesişimi by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc'+ str(val)) > 1.0,
                    Column('MACD.macd'+ str(val)).crosses_above(Column('MACD.signal'+ str(val))),
                    Column('Stoch.RSI.K'+ str(val)).crosses_above(Column('Stoch.RSI.D'+ str(val)))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_9(val):
    """
    MACD 0 yukarı kesenler by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc'+ str(val)) > 1.0,
                    Column('MACD.macd'+ str(val)).crosses_above(0),
                    Column('MACD.macd'+ str(val)) > (Column('MACD.signal'+ str(val))),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_10(val):
    """
    Düşeni Kıran by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10,
                    Column('change') <9.5,
                    Column('relative_volume_10d_calc'+ str(val)) > 1.0,
                    Column('EMA5'+ str(val)) < Column('close'),
                    Column('EMA20'+ str(val)) < Column('EMA5'+ str(val)),
                    Column('MACD.macd') > Column('MACD.signal'+ str(val)),
                    Column('P.SAR'+ str(val)).crosses_below(Column('close')),
                    Column('CCI20'+ str(val)) >= 90,
                    )
        .get_scanner_data())[1]
    return Tarama


def Mum_Formasyon_1(val):
    """Bu Mum_Formasyon Terkedilmiş Bebek Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.AbandonedBaby.Bullish' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

def Mum_Formasyon_2(val):
    """Bu Mum_Formasyon Yutan Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.Engulfing.Bullish' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

def Mum_Formasyon_3(val):
    """Bu Mum_Formasyon Harami Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.Harami.Bullish' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

def Mum_Formasyon_4(val):
    """Bu Mum_Formasyon Tepen Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.Kicking.Bullish' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

def Mum_Formasyon_5(val):
    """Bu Mum_Formasyon Uç Yıldız Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.TriStar.Bullish' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

def Mum_Formasyon_6(val):
    """Bu Mum_Formasyon Uç Yıldız Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.MorningStar' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

def Mum_Formasyon_7(val):
    """Bu Mum_Formasyon Uç Yıldız Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('Candle.Marubozu.White' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon


def Mum_Formasyon_8(val):
    """Bu Mum_Formasyon Uç Yıldız Boğa Mum Formasyonu bulan Mum_Formasyondır."""
    Mum_Formasyon = (Query().set_markets('turkey')
                .select('name', 'change', 'close', 'volume', 'Perf.W')
                .where(
                    Column('open')<Column('close'),
                    Column('Candle.Hammer' + str(val))==1
                    )
        .get_scanner_data())[1]
    return Mum_Formasyon

Check = ["|60","|120","|240","","|1W"]
Check_row = ["Saatlik","2 Saatlik","4 Saatlik","Günlük","Haftalık"]

all_combined_df_1 = pd.DataFrame()
all_combined_df_2 = pd.DataFrame()
for i in range(len(Check)):
    Tarama1 = Tarama_1(Check[i])
    Tarama2 = Tarama_2(Check[i])
    Tarama3 = Tarama_3(Check[i])
    Tarama4 = Tarama_4(Check[i])
    Tarama5 = Tarama_5(Check[i])
    Tarama6 = Tarama_6(Check[i])
    Tarama7 = Tarama_7(Check[i])
    Tarama8 = Tarama_8(Check[i])
    Tarama9 = Tarama_9(Check[i])
    Tarama10 = Tarama_10(Check[i])
    Mum_Formasyon1 = Mum_Formasyon_1(Check[i])
    Mum_Formasyon2 = Mum_Formasyon_2(Check[i])
    Mum_Formasyon3 = Mum_Formasyon_3(Check[i])
    Mum_Formasyon4 = Mum_Formasyon_4(Check[i])
    Mum_Formasyon5 = Mum_Formasyon_5(Check[i])
    Mum_Formasyon6 = Mum_Formasyon_6(Check[i])
    Mum_Formasyon7 = Mum_Formasyon_7(Check[i])
    Mum_Formasyon8 = Mum_Formasyon_8(Check[i])

    tarama_dict = {
        'Tarama 01 : 30 < RSI < 30 ve MACD <0 iken MACD Yukarı Keser MACD Sinyal': Tarama1,
        'Tarama 02 : Alternatif Düşeni Kıran Taraması': Tarama2,
        'Tarama 03 : Swing Trade Taraması': Tarama3,
        'Tarama 04 : Macd ve Stokastik RSI henüz al Vermiş Tarama': Tarama4,
        'Tarama 05 : Richards Dennis Kaplumbağası Hull9 a Göre': Tarama5,
        'Tarama 06 : RSI >55 ve CCI 100 ü Yukarı Kesen Taraması': Tarama6,
        'Tarama 07 : ADX >20 iken ve CCI 100 ü Yukarı Kesen Taraması': Tarama7,
        'Tarama 08 : MACD + Stokastik RSI Kesişimi by Anka_Analiz': Tarama8,
        'Tarama 09 : MACD 0 ı Yukarı Kesenler by Anka_Analiz': Tarama9,
        'Tarama 10 : Düşeni Kıran Taraması by Anka_Analiz': Tarama10}

    Mum_Formasyon_dict = {
        'Terkedilmiş Bebek Boğa Mum Formasyonu': Mum_Formasyon1,
        'Yutan Boğa Mum Formasyonu': Mum_Formasyon2,
        'Harami Boğa Mum Formasyonu': Mum_Formasyon3,
        'Tepen Boğa Mum Formasyonu': Mum_Formasyon4,
        'Uç Yıldız Boğa Mum Formasyonu': Mum_Formasyon5,
        'Sabah Yıldızı Mum Formasyonu': Mum_Formasyon6,
        'Beyaz Maribozu Mum Formasyonu' : Mum_Formasyon7,
        'Yeşil Çekiç Mum Formasyonu': Mum_Formasyon8}

    for name, df in tarama_dict.items():
        df['Taramalar'] = name
        df['Periyot'] = Check_row[i]

    for name, df in Mum_Formasyon_dict.items():
        df['Mum Formasyonu'] = name
        df['Periyot'] = Check_row[i]

    tarama_list = [Tarama1, Tarama2, Tarama3, Tarama4, Tarama5, Tarama6, Tarama7, Tarama8,Tarama9, Tarama10]
    Mum_Formasyon_list = [Mum_Formasyon1, Mum_Formasyon2, Mum_Formasyon3, Mum_Formasyon4, Mum_Formasyon5, Mum_Formasyon6, Mum_Formasyon7, Mum_Formasyon8]

    combined_df_1 = pd.concat(tarama_list, ignore_index=True)
    combined_df_1['close'] = round(combined_df_1['close'] ,2)
    combined_df_1['Perf.W'] = round(combined_df_1['Perf.W'] ,2)
    combined_df_1['change'] = round(combined_df_1['change'] ,2)
    all_combined_df_1 = pd.concat([all_combined_df_1, combined_df_1], ignore_index=True)

    combined_df_2 = pd.concat(Mum_Formasyon_list, ignore_index=True)
    combined_df_2['close'] = round(combined_df_2['close'] ,2)
    combined_df_2['Perf.W'] = round(combined_df_2['Perf.W'] ,2)
    combined_df_2['change'] = round(combined_df_2['change'] ,2)
    all_combined_df_1 = pd.concat([all_combined_df_1, combined_df_1], ignore_index=True)
    all_combined_df_2 = pd.concat([all_combined_df_2, combined_df_2], ignore_index=True)

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

tv = TvDatafeed()

# Merge the two DataFrames on the columns 'name' and 'periot'
all_combined_df_merged = pd.merge(all_combined_df_1, all_combined_df_2, on=['name', 'Periyot'], how='inner')

Hisseler = all_combined_df_merged['name']
Taramalar = all_combined_df_merged['Taramalar']
Periyot = all_combined_df_merged['Periyot']
Mumlar = all_combined_df_merged['Mum Formasyonu']
print(Hisseler)

# DataFrame to store results
Titles = ['Hisse Adı', 'Son Fiyat','Hesaplama Zamanı' ,'TKE','Periyot','Taramalar','Mum Formasyonu']
df_signals = pd.DataFrame(columns=Titles)
today_date = datetime.now().strftime("%Y-%m-%d %H:%M")


# Process each symbol
for i in range(0, len(Hisseler)):
    try:
        data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=Interval.in_daily, n_bars=100)
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        data = data.reset_index()
        data = custom_indicator(data)
        latest_data = data.tail(2).reset_index(drop=True)
        L1 = [Hisseler[i], latest_data.loc[1,'Close'],today_date,round(latest_data.loc[1,'TKEline'],2),Periyot[i],Taramalar[i],Mumlar[i]]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except Exception as e:
        print(f"Error processing {Hisseler[i]}: {e}")

# Print results
print(df_signals.to_string())