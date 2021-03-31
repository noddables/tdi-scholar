'''Imports'''
import requests 
import calendar
import json
from pandas import Series
from pandas import DataFrame
from pandas import to_datetime
from bokeh.plotting import figure
from bokeh.plotting import output_file
from bokeh.plotting import show
import sys
from datetime import datetime
from datetime import timedelta
import winreg
'''Functions'''
def CleanString(InputString):
    CapString = InputString.upper()
    CleanString = CapString.strip()
    return CleanString
def GetUserEnvironmentVariable(name):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment")
    try:
        return winreg.QueryValueEx(key, name)[0]
    except:
        return "demo"
'''Variables'''
StartUrl = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
InputSymbol = input("Enter Symbol:")
MidUrl = "&outputsize=compact&apikey="
ApiKey = GetUserEnvironmentVariable("ALPHA_ADVANTAGE_API_KEY")
UrlSymbol = CleanString(InputSymbol)
DemoUrl = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SHOP.TRT&outputsize=compact&apikey=demo"
'''
The **demo** API key is for demo purposes only. 
Please claim your free API key at (https://www.alphavantage.co/support/#api-key)
'''
'''Procedure: take inputs and construct the URL'''
SubmitUrl = StartUrl + UrlSymbol + MidUrl + ApiKey
'''Procedure: Get all dates for last month'''
myCalendar = calendar.Calendar()
Today = datetime.today()
OneMonthAgo = Today + timedelta(days=-30)
ThatYear = int(OneMonthAgo.strftime('%Y'))
ThatMonth = int(OneMonthAgo.strftime('%m'))
LastMonthDates = []
ClosingPrices = []
Dates = []
for CalDate in myCalendar.itermonthdates(year=ThatYear,month=ThatMonth):
    LastMonthDates.append(str(CalDate))
'''Procedure: submit the url'''
try:
    RawResults = requests.get(url=SubmitUrl)
except:
    RawResults = requests.get(url=DemoUrl)
Results = RawResults.json()
TimeSeries = Results['Time Series (Daily)']
for Date in LastMonthDates:
    try:
        Close = TimeSeries[Date]["4. close"]
        ClosingPrices.append(Close)
        Dates.append(Date)
    except:
        pass
ClosingPricesData = {"Dates": Dates, "Prices": ClosingPrices}
ClosingPricesDataFrame = DataFrame(ClosingPricesData,columns=["Dates","Prices"])
ClosingPricesDataFrame["Prices"] = ClosingPricesDataFrame["Prices"].astype(float)
ClosingPricesDataFrame["Dates"] = ClosingPricesDataFrame["Dates"].astype('datetime64')
ClosingPricesDataFrame["Dates"] = to_datetime(ClosingPricesDataFrame["Dates"] )
''''''
output_file("line.html")
Graph = figure(plot_width=1200, plot_height=800,x_axis_type='datetime')
Graph.line(ClosingPricesDataFrame.Dates,ClosingPricesDataFrame.Prices, line_width=2)
show(Graph)