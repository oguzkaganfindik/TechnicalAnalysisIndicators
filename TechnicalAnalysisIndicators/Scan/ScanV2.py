# pip install tradingview_screener

from tradingview_screener import Query, Column
import pandas as pd

def Tarama_1():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı 0 ila 15% Arasında
    RSI(14) 50 ila 55 Arasında
    Açılış Fiyatı Güncel Fiyatın Altında
    Fiyat  Yukarı Keser Basit Haraketli Ortalama 20
    Taramasıdır.
    #Bollinger orta bandından dönerken RSI ı yükselen #bist hisseleri taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('RSI').between(50,65),
                    Column('Perf.W').between(0,15),
                     Column('close') > Column('open'),
                    Column('close').crosses_above('SMA20'),
                    Column('relative_volume_10d_calc')>1.0,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_2():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı 0 ila 15% Arasında
    RSI14 50 ila 55 Arasında
    ADX14 30 ila 60 arasında
    Stockastik RSI Hızlı < 20
    Stokastik RSI Hızlı Yukarı Keser Stokastik RSI Yavaş
    Taramasıdır.
    #Üçgen-Flama bulan tarama olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('RSI').between(50,65),
                    Column('Perf.W').between(0,15),
                    Column('ADX').between(30,60),
                    Column('Stoch.RSI.K') < 20.0,
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('relative_volume_10d_calc')>1.0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_3():
    """Bu Tarama Günlük Periyotta
    RSI(14) > 50
    Aylık performansı > 20%
    Basit Hareketli Ortalama (5) < Fiyat
    Basit Hareketli Ortalama (20) < Fiyat
    Basit Hareketli Ortalama (200) < Fiyat
    Göreceli Hacim > 1.5
    Momentum > 1
    Piyasa Değeri > 2 Milyar
    Taramasıdır.
    #Driehaus'un momentum stratejisie uyan #bist hisselerinin taramaası (PD'ye göre)
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('RSI')>50,
                    Column('Perf.1M') > 20,
                    Column('Mom')>1.0,
                    Column('SMA5') < Column('close'),
                    Column('SMA20') < Column('close'),
                    Column('SMA200') < Column('close'),
                    Column('relative_volume_10d_calc')>1.5,
                    Column('market_cap_basic') >2E9
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_4():
    """Bu Tarama Günlük Periyotta
    RSI(14) > 55
    Üstel Hareketli Ortalama (5) < Fiyat
    Üstel Hareketli Ortalama (20) < Fiyat
    Üstel Hareketli Ortalama (50) < Fiyat
    Hacim Aırlıklı Hareketli Ortalama <Fiyat
    Göreceli Hacim > 1.3
    Emtia Kanal Endeksi (CCI20) > 100
    Ichimoku Dönüşüm Hattı < Ichimoku Ana Hattı
    Taramasıdır.
    #Düşeni Kıran #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('RSI')>55,
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('EMA5'),
                    Column('EMA50') < Column('EMA20'),
                    Column('VWAP') <Column('close'),
                    Column('CCI20') > 100,
                    Column('relative_volume_10d_calc')>1.3,
                    Column('Ichimoku.CLine') < (Column('Ichimoku.BLine'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_5():
    """Bu Tarama Günlük Periyotta
    Hacim > 10 Milyon
    Ortalama Hacim >10 Milyon
    Göreceli Hacim > 1.7
    Bollinger Band Upper < Fiyat
    Parabolik SAR <Fiyat
    Macd > Macd Sinyal
    Stokastik RSI Hızlı > Stokastik RSI YAvaş
    Taramasıdır.
    #Bollinger üst bandı üstündeki #bist hisselerinin taraması olarakda bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('volume') > 10E6,
                    Column('average_volume_10d_calc') > 10E6,
                    Column('relative_volume_10d_calc')>1.7,
                    Column('BB.upper') < Column('close'),
                    Column('P.SAR') < Column('close'),
                    Column('Stoch.RSI.K')> (Column('Stoch.RSI.D')),
                    Column('MACD.macd') > Column('MACD.signal')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_6():
    """Bu Tarama Günlük Periyotta
    Hacim > 5 Milyon
    Haftalık Değişim < 0%
    Hull Hareketli Ortalama < Fiyat
    Stokastik RSI Hızlı yukarı Keser Stokastik RSI Yavaş
    Taramasıdır.
    #Dinlenmesi biten #bist hisselerinin taraması olarakda bilinir. (hacimli)
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('volume') > 5E6,
                    Column('Perf.W') < 0,
                    Column('EMA5').crosses_above(Column('SMA5')),
                    Column('HullMA9') < Column('close'),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_7():
    """Bu Tarama Günlük Periyotta
    Momentum 1 ila 4 arasında
    Göreceli hacim >1.5
    Parabolik SAR <Fiyat
    Stokastik RSI Hızlı > Stokastik RSI Yavaş
    Ichimoku Dönüşüm Hattı > Ichimoku Ana Hattı
    Ichimoku Ana Hattı < Fiyat
    Ichimoku Senkou A >Ichımoku Senkou B
    Taramasıdır.
    #Ichimoku göstergeleri olumlu olan #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Mom').between(1,4),
                    Column('P.SAR') < Column('close'),
                    Column('MACD.macd') > Column('MACD.signal'),
                    Column('Stoch.RSI.K') > Column('Stoch.RSI.D'),
                    Column('Ichimoku.BLine') < Column('close'),
                    Column('Ichimoku.CLine') > Column('Ichimoku.BLine'),
                    Column('Ichimoku.Lead1') > Column('Ichimoku.Lead2'),
                    Column('relative_volume_10d_calc') > 1.5
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_8():
    """Bu Tarama Günlük Periyotta
    Göreceli hacim >1.5
    Haftalık Değişim 3 ila 15 arasında
    Williams Yüzde Aralığ -100 ila -70 arasında
    Taramasıdır.
    #Williams %R ile dipten dönen #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('W.R').between(-100,-70),
                    Column('Perf.W').between(3,15),
                    Column('relative_volume_10d_calc') > 1.5
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_9():
    """Bu Tarama Günlük Periyotta
    Hacim > 1 Milyon
    Göreceli hacim >1.5
    Haftalık Değişim < 15%
    Açılış Fiyatı Güncel Fiyatın Altında
    Chaikin Para Akışı -0.2 ila 0.3 arasında
    RSI 45 ila 60 arasında
    RSI7 < 70
    Ichimoku Dönüşüm Hattı < Fiyat
    Stokastik RSI Hızlı >= Stokastik RSI Yavaş
    Taramasıdır.
    #Hull ortalaması üzerinde ve tenkansen üzerinde olan #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('volume') > 1E6,
                     Column('close') > Column('open'),
                    Column('ChaikinMoneyFlow').between(-0.2,0.3),
                    Column('HullMA9') < Column('close'),
                    Column('relative_volume_10d_calc') > 1.5,
                    Column('Perf.W') < 15,
                    Column('RSI').between(45,60),
                    Column('RSI7') < 70,
                    Column('Stoch.RSI.K') >= Column('Stoch.RSI.D'),
                    Column('Ichimoku.CLine') <Column('close')

                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_10():
    """Bu Tarama Günlük Periyotta
    Hacim > 5 Milyon
    Göreceli hacim >1.3
    Açılış Fiyatı Güncel Fiyatın Altında
    Basit Haraketli ortalama 5 >Basit Haraketli Ortalama 100
    RSI 45 ila 60 arasında
    RSI7 40 ila 65 arasında
    Stokastik RSI Hızlı >= Stokastik RSI Yavaş
    Taramasıdır.
    #Hull ortalaması üzerinde SMA in SMA100 üzerinde olduğu #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('volume') > 5E6,
                     Column('close') > Column('open'),
                    Column('HullMA9') < Column('close'),
                    Column('relative_volume_10d_calc') > 1.3,
                    Column('RSI').between(40,65),
                    Column('RSI7').between(40,65),
                    Column('SMA5') > Column('SMA100'),
                    Column('Stoch.RSI.K') >= Column('Stoch.RSI.D')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_11():
    """Bu Tarama Günlük Periyotta
    Göreceli hacim >1.3
    Haftalık Değişim < 15%
    Ichimoku Dönüşüm Hattı yukarı keser Ichimoku Ana Hattı
    Taramasıdır.
    #Tenkansen Kijunseni yukarı kesen #bist hisseleri taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('relative_volume_10d_calc') > 1.3,
                    Column('Ichimoku.CLine').crosses_above(Column('Ichimoku.BLine'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_12():
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
                    Column('RSI').between(30,40),
                    Column('change') > 0,
                    Column('MACD.macd').crosses_above(Column('MACD.signal')),
                    Column('MACD.signal') < 0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_13():
    """Bu Tarama Günlük Periyotta
    Haftalık Değişim < 15%
    Fiyat Yukarı Keser Üstel Hareketli Ortalama 20
    ADX 30 ila 40 arasında
    Taramasıdır.
    #ADX30 'un hemen üzerindeyken EMA20'yi yukarı kesen #bist hisseleriin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('close').crosses_above('EMA20'),
                    Column('ADX').between(30,40)
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_14():
    """Bu Tarama Günlük Periyotta
    Haftalık Değişim < 15%
    Açılış Fiyatı Güncel Fiyatın Altında
    Fiyat Yukarı Keser Basit Hareketli Ortalama 20
    RSI 50 ila 55 Arasında
    Taramasıdır.
    #RSI hemen 50 seviyesi üzerindeyken bollinger orta bandını yukarı kesen #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('close') > Column('open'),
                    Column('close').crosses_above('SMA20'),
                    Column('RSI').between(50,55)
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_15():
    """Bu Tarama Günlük Periyotta
    Haftalık Değişim < 15%
    Fiyat Yukarı Keser Ichimoku Dönüşüm Hattı
    Stokastik RSI Hızlı Yukarı Keser Stokastik RSI Yavaş
    Taramasıdır.
    #Fiyat tenkansen'i yukarı keserken stokastik rsi al veren #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('relative_volume_10d_calc') > 1.3,
                    Column('close').crosses_above('Ichimoku.CLine'),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_16():
    """Bu Tarama Günlük Periyotta
    Haftalık Değişim < 15%
    Üstel Haraketli Ortalama 5 yukarı keser Üstel Hareketli Ortalama 50
    Taramasıdır. (ANKA CROSS)
    #Üstel Hareketli ortalama 5 in üstel hareketli ortalama 50 yi yukarı kesen #bist hisselerinin taraması olarak da bilinir.(By AnkaCross)
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('EMA5').crosses_above('EMA50')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_17():
    """Bu Tarama Günlük Periyotta
    Haftalık Değişim < 15%
    MACD < 0
    MACD yukarı keser MACD Sinyal
    Taramasıdır.
    #MACD negatif bölgede al veren #bist hisselerinin taraması
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('relative_volume_10d_calc') > 1.3,
                    Column('Perf.W') < 15,
                    Column('MACD.macd') < 0,
                    Column('MACD.macd').crosses_above(Column('MACD.signal'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_18():
    """Bu Tarama Günlük Periyotta
    Açılış < Üstel Hareketli Ortalama
    Fiyat Yukarı keser Üstel Hareketli Ortalama

    Taramasıdır.
    #EMA200'ü yukarı kesmiş #bist hisselerinin taranması
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('open') > Column('EMA200'),
                    Column('close').crosses_above(Column('EMA200'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_19():
    """Bu Tarama Günlük Periyotta
    Haftalık Değişim < 20%
    Fiyat > Basit Hareketli Ortalama 200
    Hacim Ağırlıklı Ortalama Fiyat < Fiyat
    Hacim Ağırlıklı Hareketli Ortalama < Fiyat
    Taramasıdır.
    #HAHO ve HAOF üzerinde olup SMA200 ü yukarı kesmiş #bist hisselerinin taraması olarak da bilinir
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 20,
                    Column('close').crosses_above(Column('SMA200')),
                    Column('VWAP') <Column('close'),
                    Column('VWMA') <Column('close')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_20():
    """Bu Tarama Günlük Periyotta
    Fiyat Yukarı Keser Basit Hareketli Ortalama 50
    Stokastik RSI Hızlı Yukarı Keser Stokastik RSI Yavaş
    Stokastik RSI Yavaş <20
    Taramasıdır.
    #Stokastik RSI 20 nin altında al verirken SMA50 den dönen #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('close').crosses_above(Column('SMA50')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('Stoch.RSI.D') <20
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_21():
    """Bu Tarama Günlük Periyotta
    Fiyat Yukarı Keser Basit Hareketli Ortalama 50
    Stokastik RSI Hızlı Yukarı Keser Stokastik RSI Yavaş
    Stokastik RSI Yavaş <20
    Taramasıdır.
    #Stokastik RSI 20 nin altında al Bollinger alt bandıdan döüş veren #bist hisselerinin taranması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('close').crosses_above(Column('BB.lower')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('Stoch.RSI.D') < 20
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_22():
    """Bu Tarama Günlük Periyotta
    Parabolik SAR < Fiyat
    Üstel Haraketli Ortalama 10 Yukarı Keser Üstel Haraketli Ortalama 20
    Taramasıdır.
    #Parabolik SAR aldayken EMA10 EMA20 'i yukarı kesen #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('P.SAR') < Column('close'),
                    Column('EMA10').crosses_above(Column('EMA20'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_23():
    """Bu Tarama Günlük Periyotta
    Fiyat  > Bollinger Alt Bandı
    En düşük Fiyat <Bollinger Alt Bandı
    Stokastik RSI Hızlı >= Stokastik RSI yavaş
    Taramasıdır.
    #Bollinger alt bandı yada alt altından dönen #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('close') > (Column('BB.lower')),
                    Column('low') <= (Column('BB.lower')),
                    Column('Stoch.RSI.K') >= Column('Stoch.RSI.D')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_24():
    """Bu Tarama Günlük Periyotta
    Pozitif Yönsel Gösterge Yuakrı Keser Negatif Yönsel Gösterge
    Göreceli Hacim > 1.3
    MACD < MACD Sinyal
    Chaikin Para Akışı < 0
    Stokastik RSI Hızlı > Stokastik RSI yavaş
    Taramasıdır.
    #Chaikin dipten dönerken DMI al veren #bist hisselerinin tarması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('ADX+DI').crosses_above(Column('ADX-DI')),
                    Column('relative_volume_10d_calc') > 1.3,
                    Column('MACD.macd') < Column('MACD.signal'),
                    Column('ChaikinMoneyFlow') < 0,
                    Column('Stoch.RSI.K') > Column('Stoch.RSI.D')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_25():
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
                    Column('relative_volume_10d_calc') > 1.5,
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('EMA5'),
                    Column('EMA50') < Column('EMA20'),
                    Column('MACD.macd') > Column('MACD.signal'),
                    Column('P.SAR').crosses_below(Column('close')),
                    Column('CCI20') >= 90.0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_26():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    RSI 30 ila 55 arasında
    MACD Yukarı Keser MACD Sinyal
    MACD Sinyal < 0
    Taramasıdır.
    #Swing Trade 3 nolu strateji taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('RSI').between(30,55),
                    Column('MACD.macd').crosses_above(Column('MACD.signal')),
                    Column('MACD.signal') < 0.0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_27():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    ATR < 0.2
    MACD Yukarı Keser MACD Sinyal
    Taramasıdır.
    #Richards Dennis Kaplumbağası MACD kesişimi olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15,
                    Column('ATR') < 0.2,
                    Column('MACD.macd').crosses_above(Column('MACD.signal'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_28():
    """Bu Tarama Günlük Periyotta
    Fiyat Yukarı Keser Basit Haraketli Ortalama 50
    Stokastik RSI Hızlı Yukarı Keser Stokastik RSI Yavaş
    Stokastik RSI Yavaş < 0
    Taramasıdır.
    #Stokastik RSI 40 ı altında al verirken Fiyat yukarı keser SMA50 #bist hisselerinin taranması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('close').crosses_above(Column('SMA50')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('Stoch.RSI.D') < 40.0
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_29():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Stokastik RSI Hızlı > Stokastik RSI Yavaş
    Stokastik RSI Yavaş < 50
    Hull Haraketli Ortalama 9 Yukarı Keser Basit Haraketli Ortalama
    Taramasıdır.
    #HUll9 X SMA20 Statejisi olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('HullMA9').crosses_above(Column('SMA20')),
                    Column('Stoch.RSI.K') > Column('Stoch.RSI.D'),
                    Column('Stoch.RSI.D') < 50.0

                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_30():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.0
    RSI14 45 ile 60 arasında
    RSI7 < 70
    Stokastik RSI Hızlı > Stokastik RSI Yavaş
    Chaikin Para Akışı -0.2 ila 0.3 arasında
    Ichimoku Dönüşüm Hattı Aşağı Keser Fiyat
    Hull Haraketli Ortalama 9 Küçük Fiyat
    Taramasıdır.
    #Fiyat hull9 üzerindeyken tenkanseni yukarı kesen #bist hisselerinin taraması olarakda bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('relative_volume_10d_calc')>1.0,
                    Column('close') > Column('open'),
                    Column('RSI').between(45,60),
                    Column('RSI7') < 70,
                    Column('ChaikinMoneyFlow').between(-0.2,0.3),
                    Column('HullMA9') < Column('close'),
                    Column('Stoch.RSI.K') >= Column('Stoch.RSI.D'),
                    Column('Ichimoku.CLine').crosses_below(Column('close'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_31():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.0
    Fiyat >= Basit Haraketli Ortalama 5
    Basit Haraketli Ortalama 10 > Basit Haraketli Ortalama20
    Macd Yukarı Keser MACD Sinyali
    Taramasıdır.
    #Swint Trade 2 nolu stratejisine uyan #bist hisselerinin taraması olarakda bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('relative_volume_10d_calc')>1.0,
                    Column('close') >= Column('SMA5'),
                    Column('SMA10') >Column('SMA20'),
                    Column('MACD.macd').crosses_above(Column('MACD.signal'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_32():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.0
    Fiyat > Üstel Haraketli Ortalama 5
    Fiyat > Üstel Haraketli Ortalama 10
    Fiyat > Üstel Haraketli Ortalama 20
    Fiyat > Üstel Haraketli Ortalama 30
    Fiyat > Üstel Haraketli Ortalama 50
    Fiyat > Üstel Haraketli Ortalama 100
    Fiyat > Üstel Haraketli Ortalama 200
    Piyasa Değeri <50M
    Taramasıdır.
    #EMA lar üzerinde hacim patlaması yapan #bist hisselerinin taraması olarak da bilinir.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('relative_volume_10d_calc')>1.0,
                    Column('close') > Column('EMA5'),
                    Column('close') > Column('EMA10'),
                    Column('close') > Column('EMA20'),
                    Column('close') > Column('EMA30'),
                    Column('close') > Column('EMA50'),
                    Column('close') > Column('EMA100'),
                    Column('close') > Column('EMA200'),
                    Column('market_cap_basic') <1E7
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_33():
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
                    Column('relative_volume_10d_calc')>1.0,
                    Column('MACD.macd').crosses_above(Column('MACD.signal')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_34():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı < 15%
    Göreceli Hacim > 1.0
    İşlem Hacmi > 5 Milyon
    Fiyat > Açılış
    RSI14 40 ila 65 arasında
    RSI7 40 ila 65 arasında
    Bast Haraketli Ortalama 5 > Basit Haraketli Ortalama 100
    Hull Haraketli Ortalama 9 > Düşük
    Stokastik RSI Hızlı > Stokastik RSI Yavaş
    Taramasıdır.
    #Hull9 u hacimli yukarı kesen #bist hisselerinin taraması
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('relative_volume_10d_calc')>1.0,
                    Column('volume') > 5E6,
                    Column('close') > Column('open'),
                    Column('RSI').between(40,65),
                    Column('RSI7').between(40,65),
                    Column('SMA5') > Column('SMA100'),
                    Column('HullMA9') > Column('low'),
                    Column('Stoch.RSI.K') > (Column('Stoch.RSI.D'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_35():
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
                    Column('close').crosses_above('HullMA9'),
                    Column('ATR').between(0,10),
                    Column('SMA20').crosses_below('close'),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_103():
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
                    Column('RSI') > 55.0,
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('SMA5'),
                    Column('EMA50') < Column('SMA20'),
                    Column('CCI20').crosses_above(100),
                    Column('Value.Traded') > 1E7
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_104():
    """Bu Tarama Günlük Periyotta
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
                .select('name', 'change','close','volume','Perf.W')
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

def Tarama_105():
    """Bu Tarama Günlük Periyotta
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
                .select('name', 'change','close','volume','Perf.W')
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

def Tarama_106():
    """Bu Tarama Günlük Periyotta
    Haftalık Performansı 0 ila 15% arasında
    RSI(14) >55
    Göreceli Hacim > 1.0
    Ichimoku Conversation Line (9,26,52,26) < Kapanış Fiyatı
    Hacim Ağırlıklı Ortalama Fiyat <Kapanış Fiyatı
    Emtia Kanal Endeksi (CCI) Yukarı Keser 100
    Taramasıdır.
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
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

def Tarama_200():
    """
    EMA 20-50 Taraması by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W',)
                .where(
                    Column('Perf.W') < 10,
                    Column('change') < 9.5,
                    Column('close').crosses_above(Column('EMA20')),
                    Column('EMA20') >= Column('EMA50'),
                    Column('relative_volume_10d_calc|1W')>1.7,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_201():
    """
    ADX+CCI Taraması by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W',)
                .where(
                    Column('Perf.W') < 10,
                    Column('change') < 9.5,
                    Column('ADX') > 20,
                    Column('CCI20').crosses_above(100),
                    Column('relative_volume_10d_calc|1W')>1.0,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_202():
    """
    RSI14 x SMA14 kesişimi by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W',)
                .where(
                    Column('Perf.W') < 10,
                    Column('change') < 9.5,
                    Column('RSI7').crosses_above(Column('RSI')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    Column('relative_volume_10d_calc|1W')>2.0,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_203():
    """
    MACD + Stokastik RSI Kesişimi by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc')>1.3,
                    Column('MACD.macd').crosses_above(Column('MACD.signal')),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D'))
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_204():
    """
    MACD 0 yukarı kesenler by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc')>1.5,
                    Column('MACD.macd').crosses_above(0),
                    Column('MACD.macd') > (Column('MACD.signal')),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_205():
    """
    P.SAR + EMA by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10.0,
                    Column('change') < 9.5,
                    Column('relative_volume_10d_calc')>1.0,
                    Column('P.SAR') < Column('close'),
                    Column('EMA10').crosses_above(Column('EMA20')),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_206():
    """
    Williams %R by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W').between(0,10),
                    Column('change').between(0,5),
                    Column('relative_volume_10d_calc')>1.0,
                    Column('W.R').between(-100,-50),
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_207():
    """
    Düşeni Kıran by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10,
                    Column('change') <9.5,
                    Column('relative_volume_10d_calc')>1.0,
                    Column('EMA5') < Column('close'),
                    Column('EMA20') < Column('EMA5'),
                    Column('MACD.macd') > Column('MACD.signal'),
                    Column('P.SAR').crosses_below(Column('close')),
                    Column('CCI20') >= 90,
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_208():
    """
    DAHI by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 10.0,
                    Column('relative_volume_10d_calc') > 1.3,
                    Column('ADX') > 20,
                    Column('ADX+DI') > Column('ADX-DI'),
                    Column('Aroon.Up') > 99,
                    Column('Aroon.Up') > Column('Aroon.Down'),
                    Column('HullMA9') < Column('close'),
                    Column('Ichimoku.BLine') < Column('Ichimoku.CLine')
                    )
        .get_scanner_data())[1]
    return Tarama

def Tarama_209():
    """
    Flame_Ucgen by Anka_Analiz
    """
    Tarama = (Query().set_markets('turkey')
                .select('name', 'change','close','volume','Perf.W')
                .where(
                    Column('Perf.W') < 15.0,
                    Column('relative_volume_10d_calc') > 1.0,
                    Column('ADX').between(20,60),
                    Column('RSI').between(50,65),
                    Column('Stoch.RSI.K').crosses_above(Column('Stoch.RSI.D')),
                    )
        .get_scanner_data())[1]
    return Tarama

Tarama1 = Tarama_1()
Tarama2 = Tarama_2()
Tarama3 = Tarama_3()
Tarama4 = Tarama_4()
Tarama5 = Tarama_5()
Tarama6 = Tarama_6()
Tarama7 = Tarama_7()
Tarama8 = Tarama_8()
Tarama9 = Tarama_9()
Tarama10 = Tarama_10()
Tarama11 = Tarama_11()
Tarama12 = Tarama_12()
Tarama13 = Tarama_13()
Tarama14 = Tarama_14()
Tarama15 = Tarama_15()
Tarama16 = Tarama_16()
Tarama17 = Tarama_17()
Tarama18 = Tarama_18()
Tarama19 = Tarama_19()
Tarama20 = Tarama_20()
Tarama21 = Tarama_21()
Tarama22 = Tarama_22()
Tarama23 = Tarama_23()
Tarama24 = Tarama_24()
Tarama25 = Tarama_25()
Tarama26 = Tarama_26()
Tarama27 = Tarama_27()
Tarama28 = Tarama_28()
Tarama29 = Tarama_29()
Tarama30 = Tarama_30()
Tarama31 = Tarama_31()
Tarama32 = Tarama_32()
Tarama33 = Tarama_33()
Tarama34 = Tarama_34()
Tarama35 = Tarama_35()

Tarama100 = Tarama_103()
Tarama101 = Tarama_104()
Tarama102 = Tarama_105()
Tarama103 = Tarama_106()

Tarama200 = Tarama_200()
Tarama201 = Tarama_201()
Tarama202 = Tarama_202()
Tarama203 = Tarama_203()
Tarama204 = Tarama_204()
Tarama205 = Tarama_205()
Tarama206 = Tarama_206()
Tarama207 = Tarama_207()
Tarama208 = Tarama_208()
Tarama209 = Tarama_209()

tarama_dict = {
    'Tarama 1': Tarama1, 'Tarama 2': Tarama2, 'Tarama 3': Tarama3, 'Tarama 4': Tarama4, 'Tarama 5': Tarama5, 'Tarama 6': Tarama6,
    'Tarama 7': Tarama7, 'Tarama 8': Tarama8, 'Tarama 9': Tarama9, 'Tarama 10': Tarama10, 'Tarama 11': Tarama11,
    'Tarama 12': Tarama12, 'Tarama 13': Tarama13, 'Tarama 14': Tarama14, 'Tarama 15': Tarama15, 'Tarama 16': Tarama16,
    'Tarama 17': Tarama17, 'Tarama 18': Tarama18, 'Tarama 19': Tarama19, 'Tarama 20': Tarama20, 'Tarama 21': Tarama21,
    'Tarama 22': Tarama22, 'Tarama 23': Tarama23, 'Tarama 24': Tarama24, 'Tarama 25': Tarama25, 'Tarama 26': Tarama26,
    'Tarama 27': Tarama27, 'Tarama 28': Tarama28, 'Tarama 29': Tarama29, 'Tarama 30' : Tarama30, 'Tarama 31': Tarama31,
    'Tarama 32': Tarama32, 'Tarama 33': Tarama33, 'Tarama 34': Tarama34, 'Tarama 35': Tarama35,
    'Tarama 100': Tarama100, 'Tarama 101': Tarama101, 'Tarama 102': Tarama102,'Tarama 103': Tarama103,
    'Tarama 200': Tarama200, 'Tarama 201' : Tarama201, 'Tarama 202': Tarama202, 'Tarama 203': Tarama203,
    'Tarama 204': Tarama204, 'Tarama 205' : Tarama205, 'Tarama 206': Tarama206, 'Tarama 207': Tarama207,
    'Tarama 208': Tarama208, 'Tarama 209' : Tarama209
}

for name, df in tarama_dict.items():
    df['Taramalar'] = name

tarama_list = [
    Tarama1, Tarama2, Tarama3, Tarama4, Tarama5, Tarama6, Tarama7, Tarama8, Tarama9,
    Tarama10, Tarama11, Tarama12, Tarama13, Tarama14, Tarama15, Tarama16,
    Tarama17, Tarama18, Tarama19, Tarama20, Tarama21, Tarama22, Tarama23,
    Tarama24, Tarama25, Tarama26, Tarama27, Tarama28, Tarama29, Tarama30,
    Tarama31, Tarama32, Tarama33, Tarama34, Tarama35,
    Tarama100, Tarama101, Tarama102, Tarama103,
    Tarama200, Tarama201, Tarama202, Tarama203, Tarama204, Tarama205, Tarama206, Tarama207, Tarama208, Tarama209,
]

combined_df = pd.concat(tarama_list, ignore_index=True)
print(combined_df.to_string())




