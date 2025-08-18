import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from backtesting import backtest_strategy

def fetch_stock_data(ticker, startdate, enddate):
    data = yf.download(ticker, start = startdate, end = enddate)
    data = data.reset_index()
    #rename columns
    data = data.rename(columns= {'Date': 'date', "Open": "open", "Close": "close", "High": "high", "Low": "low", "Volume": "volume"})
    return data

def generate_signals(data):
    bollinger_period = 20
    data["sma_20"] = data["close"].rolling(bollinger_period).mean()
    data["stdev_20"] = data["close"].rolling(bollinger_period).std()
    
    #Bollinger bands
    data["upper_bollinger"] = data["sma_20"] + 2 * data["stdev_20"]
    data["lower_bollinger"] = data["sma_20"] - 2 * data["stdev_20"]

    #RSI
    rsi_period = 14
    data["delta"] = data["close"].diff()
    data["gain"] = data["delta"].clip(lower = 0)
    data["loss"] = data["delta"].clip(upper = 0) * -1
    data["avg_gain"] = data["gain"].ewm(span = rsi_period).mean()
    data["avg_loss"] = data["loss"].ewm(span = rsi_period).mean()
    data["rsi_index"] = 100 - (100 / (1 + data["avg_gain"] / data["avg_loss"]))

    #Finding ATR
    def generate_atr(data):
        atr_period = 14
        high = data["high"]
        low = data["low"]
        close = data["close"]
        tr = pd.concat([
            high - low, 
            (low - close.shift(1)).abs(),
            (high - close.shift(1)).abs()
        ], axis=1).max(axis=1)
        data["tr"] = tr
        data["atr"] = data["tr"].ewm(span = atr_period).mean()        
        return data
    
    data = generate_atr(data)

    #sanity check
    print(data.head())
    print(data.tail())
    
    #Signals
    data["signal"] = 0
    
    long_condition = (
        (data["rsi_index"] < 30) & (data["close"] < data["lower_bollinger"]))

    short_condition = (
        (data["rsi_index"] > 70) & (data["close"] > data["upper_bollinger"]))

    data.loc[long_condition, "signal"] = 1
    data.loc[short_condition, "signal"] = -1

    data.loc[data["sma_20"].isna(), "signal"] = 0 
    data.loc[data["atr"].isna(), "signal"] = 0
    data.loc[data["rsi_index"].isna(), "signal"] = 0

    return data

##
#main program
##
tests = [
    {"ticker": "UNH", "start": "2019-01-01", "end": "2021-12-31"},
    {"ticker": "TSLA", "start": "2020-01-01", "end": "2022-12-31"},
    {"ticker": "SPY", "start": "2022-01-01", "end": "2023-12-31"},
]

for test in tests:
    ticker, start, end = test["ticker"], test["start"], test["end"]
    data = fetch_stock_data(ticker, start, end)
    data = generate_signals(data)

    #sanity check plot
    plt.figure(figsize=(12,5))
    plt.xticks(rotation=45)

    plt.plot(data['date'], data['close'], label = 'Close')
    plt.plot(data['date'], data['sma_20'], label = '20 Ma')
    plt.fill_between(data['date'], data['upper_bollinger'], data['lower_bollinger'], label = 'Bollinger Bands', color='lightgrey')
    plt.title(ticker, fontweight = 'bold')

    plt.legend()        
    plt.show()




