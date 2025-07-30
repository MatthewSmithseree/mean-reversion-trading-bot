import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def generate_signals(data):
    period = 20
    data["sma_20"] = data["close"].rolling(period).mean()
    data["stdev_20"] = data["close"].rolling(period).std()
    
    #Bollinger bands
    data["upper_bollinger"] = data["sma_20"] + 2 * data["stdev_20"]
    data["lower_bollinger"] = data["sma_20"] - 2 * data["stdev_20"]

    #RSI
    period = 14
    data["delta"] = data["close"].diff()
    data["gain"] = data["delta"].clip(lower = 0)
    data["loss"] = -data["delta"].clip(upper = 0)
    data["avg_gain"] = data["gain"].ewm(span = period).mean()
    data["avg_loss"] = data["loss"].ewm(span = period).mean()
    data["rsi_index"] = 100 - (100 / (1 + data["avg_gain"] / data["avg_loss"]))
    
    #Signals
    data["signal"] = 0
    
    long_condition = (
        (data["rsi_index"] > 70) & (data["close"] > data["upper_bollinger"])
    )


    short_condition = (
        (data["rsi_index"] < 30) & (data["close"] < data["lower_bollinger"])        
    )

    data.loc[long_condition, "signal"] = 1
    data.loc[short_condition, "signal"] = -1

    data.loc[data["sma_20"].isna(), "signal"] = 0 

    return data
















