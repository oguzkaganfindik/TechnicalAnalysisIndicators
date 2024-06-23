import os
import requests
if os.path.exists('StockIndicators.py'):
    os.remove('StockIndicators.py')

# pip install pandas_ta git+https://github.com/rongardF/tvdatafeed tradingview-screener backtesting
    
# StockIndicators.py dosyasını indir ve kaydet
url = "https://raw.githubusercontent.com/oguzkaganfindik/TechnicalAnalysisIndicators/master/TechnicalAnalysisIndicators/StockIndicators/StockIndicators.py"
response = requests.get(url)

with open("StockIndicators.py", "wb") as file:
    file.write(response.content)

print("Dosya indirildi ve kaydedildi.")

import StockIndicators as SI
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from tvDatafeed import TvDatafeed, Interval
from tradingview_screener import Query, Column
import warnings
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm


def model_selection(X, Y):
    seed = 5
    models = [('LR', LogisticRegression()),
        ('LDA', LinearDiscriminantAnalysis()),
        ('KNN', KNeighborsClassifier(n_neighbors=8)),
        ('CART', DecisionTreeClassifier()),
        ('NB', GaussianNB()),
        ('SVM', svm.SVC()),
        ('RFT', RandomForestClassifier())]

    results = []
    names = []
    scoring = 'accuracy'
    for name, model in models:
        kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
        cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)

    # Find the best model based on cross-validation accuracy
    best_model_index = np.argmax(np.mean(results, axis=1))
    best_model_name = names[best_model_index]
    best_model = models[best_model_index][1]
    return best_model

class Strategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.data['Entry'] == True and not self.position:
            self.buy()

        elif self.data['Exit'] == True:
            self.position.close()

Hisseler = [
    "AEFES", "AGROT", "AHGAZ", "AKBNK", "AKCNS", "AKFGY", "AKFYE", "AKSA", "AKSEN",
    "ALARK", "ALBRK", "ALFAS", "ANSGR", "ARCLK", "ASELS", "ASTOR", "BERA", "BFREN",
    "BIENY", "BIMAS", "BIOEN", "BOBET", "BRSAN", "BRYAT", "BTCIM", "CANTE", "CCOLA",
    "CIMSA", "CWENE", "DOAS", "DOHOL", "ECILC", "ECZYT", "EGEEN", "EKGYO", "ENERY",
    "ENJSA", "ENKAI", "EREGL", "EUPWR", "EUREN", "FROTO", "GARAN", "GESAN", "GUBRF",
    "GWIND", "HALKB", "HEKTS", "IPEKE", "ISCTR", "ISGYO", "ISMEN", "IZENR", "KAYSE",
    "KCAER", "KCHOL", "KLSER", "KONTR", "KONYA", "KOZAA", "KOZAL", "KRDMD", "MAVI",
    "MGROS", "MIATK", "ODAS", "OTKAR", "OYAKC", "PETKM", "PGSUS", "QUAGR", "REEDR",
    "SAHOL", "SASA", "SAYAS", "SDTTR", "SISE", "SKBNK", "SMRTG", "SOKM", "TABGD",
    "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB", "TTKOM", "TTRAK", "TUKAS",
    "TUPRS", "TURSG", "ULKER", "VAKBN", "VESBE", "VESTL", "YEOTK", "YKBNK", "YYLGD",
    "ZOREN"]


#Raporlama için kullanılacak başlıklar
Titles = ['Hisse Adı', 'Son Fiyat', 'Algo Öncesi Kazanma Oranı','Algo Öncesi Giriş Sinyali', 'Algo Öncesi Çıkış Sinyali','Algo Sonrası Kazanma Oranı', 'Algo Sonrası Giriş Sinyali', 'Algo Öncesi Çıkış Sinyali']
df_signals = pd.DataFrame(columns=Titles)

for i in range(0,len(Hisseler)):
    try:
        data = SI.TVGet(Hisseler[i], 'BIST', '4h', 1000)
        """İndikatörlerin Hesaplanması"""
        data['RSI'] = SI.rsi(data['close'], 14)
        data['OBV'] = SI.obv(data['close'], data['volume'])
        data['MOM'] = SI.momentum(data['close'], 14)
        data['SALMA'] = SI.salma(data['close'])

        """Giriş ve Çıkış Koşullarının Belirlenmesi"""
        data['Entry'] = (data['SALMA'] > data['SALMA'].shift(1)).astype(int)
        data['Exit'] = (data['Entry'] == 0).astype(int)

        """Öğrenme Algoritmasında Kullanılacak Unsurlar ve Hedefin Tanımlanması"""
        features = ['RSI', 'OBV','MOM']
        target = 'Entry'

        """Varsa Verideki NaN Değerlerinin Silinmesi"""
        data = data.dropna().reset_index(drop=True)

        """Makine Öğrenmesinde Kullanılacak X ve y nin tanımlanması"""
        X = data[features]
        y = data[target]

        """ Standart Scaler ' ın çağırılması ve Verilerin Scale edilmesi"""
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)


        """ En uygun Modelin bulunması"""
        best_model = model_selection(X_scaled, y)

        """ Verilerin En uygun modele göre fit edilmesi"""
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        best_model.fit(X_train, y_train)

        """Sonuçların Karışlaştırılması için test kümesinde teni bir dataframe oluşturulması"""
        df_X_test = pd.DataFrame()
        df_X_test['datetime'] = data.loc[:len(X_test)-1, 'datetime']
        df_X_test['Open'] = data.loc[:len(X_test)-1, 'open']
        df_X_test['High'] = data.loc[:len(X_test)-1, 'high']
        df_X_test['Low'] = data.loc[:len(X_test)-1, 'low']
        df_X_test['Close'] = data.loc[:len(X_test)-1, 'close']
        df_X_test['Volume'] = data.loc[:len(X_test)-1, 'volume']
        df_X_test['Entry'] = data.loc[:len(X_test)-1, 'Entry']
        df_X_test['Exit'] = data.loc[:len(X_test)-1, 'Exit']
        df_test = df_X_test.copy()

        """Algoritma Öncesi Backtest Sonuçları ve Kazanma Oranı"""
        df_test['datetime'] = pd.to_datetime(df_X_test['datetime'])
        df_test.set_index('datetime', inplace=True)
        bt = Backtest(df_test, Strategy, cash=100000, commission=0.002)
        Stats= bt.run()
        Buy_1 = False
        Sell_1 = False
        Signals = df_test.tail(2)
        Signals = Signals.reset_index()
        Buy1 = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] == True
        Sell1 = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        WR1 = round(Stats.loc['Win Rate [%]'], 2)

        """Algoritma Sonrası Backtest Sonuçları ve Kazanma Oranı"""
        df_test['Entry'] = best_model.predict(X_test)
        df_test['Exit']  = (df_test['Entry'] == 0).astype(int)
        bt = Backtest(df_test, Strategy, cash=100000, commission=0.002)
        Stats= bt.run()
        Signals = df_test.tail(2)
        Signals = Signals.reset_index()
        Buy2 = Signals.loc[0, 'Entry'] == False and Signals.loc[1, 'Entry'] == True
        Sell2 = Signals.loc[0, 'Exit'] == False and Signals.loc[1, 'Exit'] == True
        WR2 = round(Stats.loc['Win Rate [%]'], 2)

        """Sonuçların Liste Halinde birleştirilmesi"""
        Last_Price = Signals.loc[1, 'Close']
        L1 = [Hisseler[i],Last_Price, WR1, str(Buy1), str(Sell1),WR2, str(Buy2), str(Sell2)]
        df_signals.loc[len(df_signals)] = L1
        print(L1)
    except:
        pass

"""Algoritma Sonrası Sonuçların Önceki Sonuçtan Daha iyi olduğu ve Giriş Sinyali'nin oluştuğu verilerin filtrelenmesi """
df_True = df_signals[(df_signals['Algo Sonrası Kazanma Oranı'] > df_signals['Algo Öncesi Kazanma Oranı']) &
                     (df_signals['Algo Sonrası Giriş Sinyali'] == 'True')]

"""Sonuçların Basılması """
print(df_True.to_string())