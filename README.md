# DSAI-Electricity_Forecast

## 資料
- 2022 的資料會在程式執行時從[助教提供的網址](https://data.taipower.com.tw/opendata/apply/file/d006002/本年度每日尖峰備轉容量率.csv)載下來。
- 過去資料的部分收集了 2019、2020、2021 的備轉容量。但是在之後的嘗試中，發現好像沒什麼差，所以最後只保留了 [2021](data2021.csv) 的部分。

## 處理
對收集來的資料進行了簡單的處理...
- 把萬瓩換成 MW
- 把兩個 csv 合併
