# Gerekli kütüphaneleri yükleyin
# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import warnings
import matplotlib.pyplot as plt
from tradingview_screener import get_all_symbols

warnings.simplefilter(action='ignore')

# TradingView'e giriş yapmadan bağlanın
tv = TvDatafeed()

# Türkiye piyasasındaki tüm hisse senetlerini otomatik olarak alın
symbols = get_all_symbols(market='turkey')
symbols = [symbol.replace('BIST:', '') for symbol in symbols]
symbols = sorted(symbols)

# Camarilla pivot seviyelerini hesaplamak için fonksiyon
def camarilla_pivots(high, low, close):
    r = high - low
    r3 = close + r * (1.1 / 4)  # Bear Reversal Low
    s3 = close - r * (1.1 / 4)  # Bull Reversal High
    cp = (high + low + close) / 3  # CPR
    return r3, s3, cp

# Renk kodlaması için yardımcı fonksiyon
def colorize(val, current_price, is_symbol=False):
    if is_symbol:
        return 'background-color: yellow'
    elif val > current_price:
        return 'background-color: red; color: white'  # Kırmızı arka plan, beyaz metin (Bullish)
    elif val < current_price:
        return 'background-color: green; color: white'  # Yeşil arka plan, beyaz metin (Bearish)
    else:
        return 'background-color: yellow'  # Sarı arka plan (Current Price)

# Verileri saklamak için boş bir DataFrame oluşturun
monthly_data = []

# Her bir hisse senedi için verileri alın ve Camarilla pivotlarını hesaplayın
for symbol in symbols:
    try:
        # Aylık veri çekin (örnek olarak son 12 ay)
        df_monthly = tv.get_hist(symbol=symbol, exchange='BIST', interval=Interval.in_monthly, n_bars=12)

        # Son kapanış verilerini alın (bir önceki ay)
        high = df_monthly['high'].iloc[-2]
        low = df_monthly['low'].iloc[-2]
        close = df_monthly['close'].iloc[-2]

        # Güncel fiyatı alın
        df_daily = tv.get_hist(symbol=symbol, exchange='BIST', interval=Interval.in_daily, n_bars=1)
        current_price = df_daily['close'].iloc[-1]

        # Camarilla pivotlarını ve diğer seviyeleri hesaplayın
        r3, s3, cp = camarilla_pivots(high, low, close)

        # Şu anki fiyata olan uzaklığı yüzde olarak hesaplayın
        pivot_distances = {
            'R3 Distance (%)': ((r3 - current_price) / current_price) * 100,
            'S3 Distance (%)': ((current_price - s3) / current_price) * 100,
            'CP Distance (%)': ((current_price - cp) / current_price) * 100
        }

        # Aylık verileri tabloya ekleyin
        monthly_data.append([symbol, current_price, r3, s3, cp, pivot_distances['R3 Distance (%)'], pivot_distances['S3 Distance (%)'], pivot_distances['CP Distance (%)']])

    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Sonuçları DataFrame'e dönüştürün
df_monthly_results = pd.DataFrame(monthly_data, columns=['Symbol', 'Current Price', 'R3', 'S3', 'CP', 'R3 Distance (%)', 'S3 Distance (%)', 'CP Distance (%)'])

# Stil işlevini oluşturun ve uygulayın
styled_df = df_monthly_results.style.apply(lambda x: [colorize(x[i], x['Current Price'], is_symbol=(i == 0)) if isinstance(x[i], (float, int)) else '' for i in range(len(x))], axis=1)

# Sonuçları ekrana yazdırın
styled_df