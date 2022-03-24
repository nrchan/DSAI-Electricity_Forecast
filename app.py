import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

def adf_test(timeseries):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

def kpss_test(timeseries):
    print('Results of KPSS Test:')
    kpsstest = kpss(timeseries, regression='c', nlags="auto")
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','#Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    print(kpss_output)

# You can write code above the if-main block.
if __name__ == '__main__':
    # You should not modify this part, but additional arguments are allowed.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')

    parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
    args = parser.parse_args()

    # The following part is an example.
    # You can modify it at will.
    df2021 = pd.read_csv("data2021.csv", names=None, header=0)
    df2021["日期"] = pd.to_datetime(df2021["日期"], format="%Y%m%d")
    
    df2022 = pd.read_csv("data2022.csv", names=None, header=0)
    df2022["日期"] = pd.to_datetime(df2022["日期"], format="%Y/%m/%d")
    df2022["備轉容量(萬瓩)"] = 10*df2022["備轉容量(萬瓩)"]
    df2022 = df2022.rename(columns={"備轉容量(萬瓩)":"備轉容量(MW)"})

    df = pd.concat([df2021,df2022]).reset_index(drop = True).dropna(axis=1)
    #print(adf_test(df["備轉容量(MW)"]))
    #print(kpss_test(df["備轉容量(MW)"]))
    
    """
    rolling_mean = df["備轉容量(MW)"].rolling(window=12).mean()
    rolling_std = df["備轉容量(MW)"].rolling(window=12).std()
    plt.figure(figsize = (10,6))
    plt.plot(df["備轉容量(MW)"], color='cornflowerblue', label='Original')
    plt.plot(rolling_mean, color='firebrick', label='Rolling Mean')
    plt.plot(rolling_std, color='limegreen', label='Rolling Std')
    plt.show()
    """

    dftouse = np.asarray(df["備轉容量(MW)"])
    train = dftouse[0:len(dftouse)-14]
    test = dftouse[len(dftouse)-14:]

    model = ARIMA(train, seasonal_order=(7,1,5,7), enforce_stationarity=False, enforce_invertibility=False)
    model = model.fit()

    
    predictions = model.predict(start=len(train), end=len(train)+len(test)-1)
    arima_score = mean_squared_error(test, predictions, squared = False)
    print('RMSE: {}'.format(round(arima_score,4)))

    plt.figure(figsize = (10,6))
    plt.plot(test, label = "true values", color = "cornflowerblue")
    plt.plot(predictions,label = "forecasts", color='darkorange')
    plt.title("ARIMA Model", size = 14)
    plt.show()