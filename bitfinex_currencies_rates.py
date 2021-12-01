import datetime
import re
from tkinter import filedialog, Tk
import xml.etree.ElementTree as ET
import pandas as pd
import requests

list_of_currencies = []
list_of_columns = ['SYMBOL', 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE',
                   'DAILY_CHANGE_RELATIVE', 'LAST_PRICE', 'VOLUME', 'HIGH', 'LOW', 'TIMESTAMP']

today = datetime.datetime.now()

url_bitfinex = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"

if today.day < 10:
    url_cbr = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req=0{today.day}/{today.month}/{today.year}"
else:
    url_cbr = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req=0{today.day}/{today.month}/{today.year}"

payload = {}
headers = {}

response_bitfinex = requests.request(
    "GET", url_bitfinex, headers=headers, data=payload)
response_cbr = requests.request("GET", url_cbr, headers=headers, data=payload)

root = ET.fromstring(response_cbr.content)

for child in root:
    if child.attrib["ID"] == "R01235":
        for c in child:
            if c.tag == "Value":
                usd_rate = ["USD", "-", "-", c.text, "-", "-", "-", "-",
                            "-", "-", "-", f"{today.year}-{today.month}-{today.day}"]
                list_of_currencies.append(usd_rate)

for i, pair in enumerate(response_bitfinex.json(), 1):
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
    now = str(datetime.datetime.now())
    pair.append(now)
    list_of_currencies.append(pair)

df = pd.DataFrame(list_of_currencies, columns=list_of_columns)

Tk().withdraw()
file_name = filedialog.askopenfile()

with pd.ExcelWriter(file_name.name, engine="openpyxl", mode="a", if_sheet_exists="replace") as f:
    df.to_excel(f, sheet_name="rates", index=False)
