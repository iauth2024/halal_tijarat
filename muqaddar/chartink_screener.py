import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

url = "https://chartink.com/screener/process"


condition = {"scan_clause" : "( {cash} ( monthly close > monthly upper bollinger band( 20 , 2 ) and weekly close > weekly upper bollinger band( 20 , 2 ) and latest close > latest sma( latest close , 20 ) and 1 day ago  close <= 1 day ago  sma( latest close , 20 ) and latest close > 100 ) )   "}

with requests.session() as s:
    r_data = s.get(url)
    soup = bs(r_data.content, "lxml")
    meta = soup.find("meta", {"name" : "csrf-token"})["content"]

    header = {"x-csrf-token" : meta}
    data = s.post(url, headers=header, data=condition).json()

    stock_list = pd.DataFrame(data["data"])
    print(stock_list) 
    