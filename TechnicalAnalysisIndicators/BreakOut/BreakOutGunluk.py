# Gerekli kütüphaneleri yükleyin
# pip install git+https://github.com/rongardF/tvdatafeed tradingview-screener matplotlib openpyxl

import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import get_all_symbols
import warnings
import matplotlib.pyplot as plt
from tabulate import tabulate

warnings.simplefilter(action='ignore', category=FutureWarning)

def breakout_strategy(data, period=20):
    df = data.copy()
    df['High_Max'] = df['High'].rolling(window=period).max()
    df['Low_Min'] = df['Low'].rolling(window=period).min()
    df['Breakout_Up'] = df['Close'] > df['High_Max'].shift(1)
    df['Breakout_Down'] = df['Close'] < df['Low_Min'].shift(1)
    return df

tv = TvDatafeed()
Hisseler = get_all_symbols(market='turkey')
Hisseler = [symbol.replace('BIST:', '') for symbol in Hisseler]
Hisseler = sorted(Hisseler)

# 2 Saatlik, 4 Saatlik ve Günlük veriler için döngü
intervals = [Interval.in_daily]
#intervals = [Interval.in_2_hour, Interval.in_4_hour, Interval.in_daily]

df_all_signals = pd.DataFrame(columns=['Hisse Adı', 'Son Fiyat', 'Breakout Türü', 'Zaman Dilimi'])

for interval in intervals:
    df_signals_up = []
    df_signals_down = []
    for i in range(0, len(Hisseler)):
        try:
            data = tv.get_hist(symbol=Hisseler[i], exchange='BIST', interval=interval, n_bars=500)
            data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
            data = data.reset_index()
            breakout_data = breakout_strategy(data, period=20)
            breakout_data['datetime'] = pd.to_datetime(breakout_data['datetime'])
            breakout_data.set_index('datetime', inplace=True)
            last_signal = breakout_data.iloc[-1]
            Breakout_Up = last_signal['Breakout_Up']
            Breakout_Down = last_signal['Breakout_Down']
            Last_Price = last_signal['Close']
            if Breakout_Up:
                df_signals_up.append([Hisseler[i], Last_Price, 'Breakout Yukarı', interval.name])
                df_all_signals.loc[len(df_all_signals)] = [Hisseler[i], Last_Price, 'Breakout Yukarı', interval.name]
            elif Breakout_Down:
                df_signals_down.append([Hisseler[i], Last_Price, 'Breakout Aşağı', interval.name])
                df_all_signals.loc[len(df_all_signals)] = [Hisseler[i], Last_Price, 'Breakout Aşağı', interval.name]
        except Exception as e:
            print(f"Error processing {Hisseler[i]}: {e}")

    # Print Breakout Yukarı Sinyalleri
    if df_signals_up:
        df_up = pd.DataFrame(df_signals_up, columns=['Hisse Adı', 'Son Fiyat', 'Breakout Türü', 'Zaman Dilimi'])
        plt.figure(figsize=(10, 6))
        table_up = plt.table(cellText=df_up.values, colLabels=df_up.columns, cellLoc='center', loc='center')
        table_up.auto_set_font_size(False)
        table_up.set_fontsize(10)
        table_up.scale(1.5, 1.5)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'breakout_yukari_{interval.name}.png')
        plt.show()

    # Print Breakout Aşağı Sinyalleri
    #if df_signals_down:
    #    df_down = pd.DataFrame(df_signals_down, columns=['Hisse Adı', 'Son Fiyat', 'Breakout Türü', 'Zaman Dilimi'])
    #    plt.figure(figsize=(10, 6))
    #    plt.title(f'Breakout Aşağı Sinyalleri - {interval.name}')
    #    table_down = plt.table(cellText=df_down.values, colLabels=df_down.columns, cellLoc='center', loc='center')
    #    table_down.auto_set_font_size(False)
    #    table_down.set_fontsize(10)
    #    table_down.scale(1.5, 1.5)
    #    plt.axis('off')
    #    plt.tight_layout()
    #    plt.savefig(f'breakout_asagi_{interval.name}.png')
    #    plt.show()


    # Excel dosyasına kaydetme
    excel_file = 'breakout_signals.xlsx'
    df_all_signals.to_excel(excel_file, index=False)
    print(f"\nTüm breakout sinyalleri '{excel_file}' dosyasına kaydedildi.")