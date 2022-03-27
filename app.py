import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')

    parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
    args = parser.parse_args()

    #-----分割線-----#

    dfpast = pd.read_csv("data2021.csv", names=None, header=0)
    dfpast["日期"] = pd.to_datetime(dfpast["日期"], format="%Y%m%d")

    #enable to use older data
    #dfpast = pd.read_csv("datapast.csv", names=None, header=0)
    #dfpast["日期"] = pd.to_datetime(dfpast["日期"], format="%Y/%m/%d")
    #dfpast["備轉容量(萬瓩)"] = 10*dfpast["備轉容量(萬瓩)"]
    #dfpast = dfpast.rename(columns={"備轉容量(萬瓩)":"備轉容量(MW)"})
    
    df2022 = pd.read_csv("https://data.taipower.com.tw/opendata/apply/file/d006002/%E6%9C%AC%E5%B9%B4%E5%BA%A6%E6%AF%8F%E6%97%A5%E5%B0%96%E5%B3%B0%E5%82%99%E8%BD%89%E5%AE%B9%E9%87%8F%E7%8E%87.csv", names=None, header=0)
    df2022["日期"] = pd.to_datetime(df2022["日期"], format="%Y/%m/%d")
    df2022["備轉容量(萬瓩)"] = 10*df2022["備轉容量(萬瓩)"]
    df2022 = df2022.rename(columns={"備轉容量(萬瓩)":"備轉容量(MW)"})

    df = pd.concat([dfpast,df2022]).reset_index(drop = True).dropna(axis=1)
    #print(adf_test(df["備轉容量(MW)"]))
    #print(kpss_test(df["備轉容量(MW)"]))

    startDate = pd.Timestamp(2022,3,30,0)
    delta = (df["日期"][len(df)-1] - startDate).days + 1

    train = np.array(df["備轉容量(MW)"])
    model = ARIMA(train, seasonal_order=(7,1,5,7), enforce_stationarity=False, enforce_invertibility=False)
    model = model.fit(method_kwargs={"warn_convergence": False})

    forecast = model.predict(start=len(train)-delta, end=len(train)-delta +14)

    """For testing
    plt.figure(figsize = (10,6))
    truth = np.array(df["備轉容量(MW)"])[len(df)-delta:len(train)-delta+14+1]
    plt.plot(truth, label = "true values", color = "cornflowerblue")
    plt.plot(forecast,label = "forecasts", color='darkorange')
    plt.title("SARIMA Model", size = 14)
    plt.show() 
    score = mean_squared_error(truth, forecast, squared = False)
    print('RMSE: {}'.format(round(score,4)))
    """

    with open(args.output,"w") as f:
        f.write("date,operating_reserve(MW)")
        for i in range (0,15):
            f.write(f"\n{(startDate + pd.DateOffset(days=i)).strftime('%Y%m%d')},{forecast[i]}")