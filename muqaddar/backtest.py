import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime


url = "https://chartink.com/backtest/process"

condition = {"scan_clause" : "( {cash} ( ( {cash} ( latest macd line( 26 , 12 , 9 ) > latest macd signal( 26 , 12 , 9 ) and latest ema( latest close , 9 ) > latest ema( latest close , 21 ) and latest rsi( 14 ) > 50 and latest rsi( 14 ) > latest sma( latest close , 20 ) and latest volume > latest sma( latest volume , 20 ) * 1.5 and monthly close > monthly upper bollinger band( 20 , 2 ) and weekly close > weekly upper bollinger band( 20 , 2 ) and latest close > latest sma( latest close , 20 ) and latest close > latest vwap and latest close > 40 and latest adx( 14 ) > 20 ) ) ) ) "}
with requests.session() as s:
    r_data = s.get("https://chartink.com/screener/process")
    soup = bs(r_data.content, "lxml")
    meta = soup.find("meta", {"name" : "csrf-token"})["content"]

    header = {"x-csrf-token" : meta}
    data = s.post(url, headers=header, data=condition).json()

    date = data["metaData"][0]["tradeTimes"]
    stock = data["aggregatedStockList"]

    final_data = []
    for i in range(0, len(date)):
        stk = []
        if stock[i] != []:
            for j in range(len(stock[i])):
                if j % 3 == 0:
                    stk.append(stock[i][j])


            final_data.append({
                "Date" : datetime.datetime.fromtimestamp(date[i]/1000),
                "Stock" : stk
            })

    print(pd.DataFrame(final_data))

