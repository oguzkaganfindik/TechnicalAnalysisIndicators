# !pip install tradingview-screener
from tradingview_screener import Query, Column
import pandas as pd

def Tarama_1():
    """Bu tarama Günlük periyotta
    Haftalık Performansı 0 ila 15% Arasında
    RSI(14) 50 ila 55 Arasında
    Açılış Fiyatı Güncel Fiyatın Altında
    Fiyat  Yukarı Keser Basit Haraketli Ortalama 20
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change_from_open','close','volume','Perf.W','RSI','SMA20','relative_volume_10d_calc')
                .where(
                    Column('RSI').between(50,65),
                    Column('Perf.W').between(0,15),
                    Column('change_from_open')>0,
                    Column('close').crosses_above('SMA20'),
                    Column('relative_volume_10d_calc')>1.0,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_2():
    """Bu tarama Günlük periyotta
    Haftalık Performansı 0 ila 15% Arasında
    RSI14 50 ila 55 Arasında
    ADX14 30 ila 60 arasında
    Stockastik RSI Hızlı < 20
    Stokastik RSI Hızlı Yukarı Keser Stokastik RSI Yavaş
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change_from_open','close','volume','Perf.W','RSI','ADX','relative_volume_10d_calc')
                .where(
                    Column('RSI').between(50,65),
                    Column('Perf.W').between(0,15),
                    Column('ADX').between(30,60),
                    Column('Stoch.RSI.K') < 20.0,
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('relative_volume_10d_calc')>1.0,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_3():
    """Bu tarama Günlük periyotta
    RSI14 > 55
    Üstel Hareketli Ortalama 5 < Kapanış Fiyatı
    Üstel Hareketli Ortalama 20 < Basit Hareketli Ortalama 5
    Üstel Hareketli Ortalama 50 < Basit Hareketli Ortalama 20
    Emtia Kanal Endeksi CCI(20)  Yukarı Keser 100
    Hacim x Fiyat > 10 Milyon
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change_from_open','close','volume','RSI','EMA5','EMA20','EMA50','SMA5','SMA20','CCI20')
                .where(
                    Column('RSI') > 55.0,
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('SMA5'),
                    Column('EMA50') < Column('SMA20'),
                    Column('CCI20').crosses_above(100),
                    )
        .get_scanner_data())[1]
    Tarama['VP']=Tarama['volume']*Tarama['close']
    Tarama = Tarama[Tarama['VP'] > 1E7]
    Tarama = Tarama.reset_index(drop=True)
    return Tarama

def Tarama_4():
    """Bu Tarama Günlük periyotta
    RSI (14) >55
    Ortalama Yönsel Endeks (ADX14) >= 19
    Momentum (10) >= 0
    Üstel Hareketli Ortalama (5) < Kapanış Fiyatı
    Üstel Hareketli Ortalama (10) < Kapanış Fiyatı
    Üstel Hareketli Ortalama (20) < Kapanış Fiyatı
    Üstel Hareketli Ortalama (50) < Kapanış Fiyatı
    Üstel Hareketli Ortalama (100) < Kapanış Fiyatı
    Üstel Hareketli Ortalama (200) < Kapanış Fiyatı
    Stokastik %K(14,3,3) >= 50
    Para Akışı (14) > 40
    Chaikin Para Akışı (20) >= -0.7
    Ichimoku Ana Hattı (9,26,52,26) < Fiyat
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change_from_open','close','volume','ADX','Mom','EMA10','EMA50','EMA200','MoneyFlow','Ichimoku.BLine')
                .where(
                    Column('RSI')>55.0,
                    Column('ATR')>1.0,
                    Column('ADX') >= 19.0,
                    Column('Mom') >= 0.0,
                    Column('EMA5') < Column('close'),
                    Column('EMA10') < Column('close'),
                    Column('EMA20') < Column('close'),
                    Column('EMA50') < Column('close'),
                    Column('EMA100') < Column('close'),
                    Column('EMA200') < Column('close'),
                    Column('Stoch.K')>=50.0,
                    Column('MoneyFlow') >= 40.0,
                    Column('ChaikinMoneyFlow')>=-0.7,
                    Column('Ichimoku.BLine').crosses_below(Column('close')),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_5():
    """Bu Tarama Günlük periyotta
    RSI5 > RSI9
    Hull Haraketli Ortalama (HullMA9) < Kapanış Fiyatı
    Para Akışı (MFI14) > 50
    Üstel Hareketli Ortalama 5 Yukarı Keser Basit Hareketli Ortalama 10
    MACD Seviyesi > MACD Sinyal
    Ichimoku Conversation Line (9,26,52,26) < Kapanış Fiyatı
    Haftalık Ichimoku Ana Hattı (9,26,52,26) < Kapanış Fiyatı
    Bağıl Hacim > 1.00
    Taramasıdır.
    by Özkan FİLİZ"""
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change_from_open','close','volume','RSI5','RSI9','EMA5','SMA10','HullMA9','MoneyFlow','MACD.macd','MACD.signal','Ichimoku.CLine','Ichimoku.BLine|1W','relative_volume_10d_calc')
                .where(
                    Column('RSI5')>Column('RSI9'),
                    Column('HullMA9') < Column('close'),
                    Column('MoneyFlow') >= 50.0,
                    Column('EMA5').crosses_above(Column('SMA10')),
                    Column('MACD.macd') > Column('MACD.signal'),
                    Column('Ichimoku.CLine') < Column('close'),
                    Column('Ichimoku.BLine|1W') < Column('close'),
                    Column('relative_volume_10d_calc')>1.0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_6():
    """Bu Tarama Haftalık periyotta
    Haftalık Performansı 0 ila 15% arasında
    RSI(14) >55
    Bağıl Hacim > 1.0
    Ichimoku Conversation Line (9,26,52,26) < Kapanış Fiyatı
    Hacim Ağırlıklı Ortalama Fiyat <Kapanış Fiyatı
    Emtia Kanal Endeksi (CCI) Yukarı Keser 100
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change_from_open','close','volume','Perf.W','RSI','CCI20','EMA5','EMA20','EMA50','Ichimoku.CLine','relative_volume_10d_calc')
                .where(
                    Column('RSI')>55,
                    Column('CCI20').crosses_above(100),
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('EMA5'),
                    Column('EMA50') < Column('EMA20'),
                    Column('VWAP') <Column('close'),
                    Column('Perf.W').between(0,15),
                    Column('relative_volume_10d_calc|1W')>1.0,
                    Column('Ichimoku.CLine') < (Column('close'))
                    )
        .get_scanner_data())[1]
    return Tarama


Tarama1 = Tarama_1()
Tarama2 = Tarama_2()
Tarama3 = Tarama_3()
Tarama4 = Tarama_4()
Tarama5 = Tarama_5()
Tarama6 = Tarama_6()
print('TARAMA 1 SONUÇLARI')
print(Tarama1)
print('TARAMA 2 SONUÇLARI')
print(Tarama2)
print('TARAMA 3 SONUÇLARI')
print(Tarama3)
print('TARAMA 4 SONUÇLARI')
print(Tarama4)
print('TARAMA 5 SONUÇLARI')
print(Tarama5)
print('TARAMA 6 SONUÇLARI')
print(Tarama6)
