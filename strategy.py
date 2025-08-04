import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

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
        data["tr"] = pd.DataFrame({
            "high-low" : high - low, 
            "low-close" : (low - close.shift(1)).abs(),
            "high-close" : (high - close.shift(1)).abs()
        }).max(axis = 1)

        data["atr"] = data["tr"].ewm(span = atr_period).mean()        
        return data

    data = generate_atr(data)
    
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

















