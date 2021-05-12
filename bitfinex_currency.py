import re
import datetime
import openpyxl
import pandas as pd
import requests

list_of_currencies = []
list_of_columns = ['SYMBOL', 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_RELATIVE', 'LAST_PRICE', 'VOLUME', 'HIGH', 'LOW']

url = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

for i, pair in enumerate(response.json(), 1):
    if len(pair) > 11:
        continue
    if pair[0][-3:] in ['BTC', 'ETH', 'UST', 'XCH', 'EOS', 'EUR', 'JPY', 'GBP', 'BBB']:
        continue
    if pair[0][-4:] in ['CNHT']:
        continue
    if pair[0][-5:] in ['USTF0', 'BTCF0']:
        continue
    if pair[0][1:] in ['TESTBTC:TESTUSD', 'TESTBTC:TESTUSDT', 'TESTBTCF0:TESTUSDTF0']:
        continue
    x = re.split('USD|:USD', pair[0][1:])
    pair[0] = x[0]
    list_of_currencies.append(pair)

df = pd.DataFrame(list_of_currencies, columns=list_of_columns)
now = str(datetime.datetime.now())
now = now.replace(':', '.')
df.to_excel(f'{now}.xlsx', sheet_name=f'{now}')
