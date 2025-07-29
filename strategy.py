import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def generate_signals(data):
    period = 20
    data["sma_20"] = data["Close"].rolling(period).mean()
    data["stdev_20"] = data["Close"].rolling(period).stdev()
    
    #Bollinger bands
    data["upper_bollinger"] = data["sma_20"] + 2 * data["stdev_20"]
    data["lower_bollinger"] = data["sma_20"] - 2 * data["stdev_20"]

    #RSI
    period = 14
    data["delta"] = data["Close"].diff()
    data["gain"] = data["delta"].clip(lower = 0)
    data["loss"] = data["delta"].clip(upper = 0)
    data["avg_gain"] = data["gain"].ewm(period)
    data["avg_loss"] = data["loss"].ewm(period)
    data["rsi_index"] = 100 - (100 / (1 + data["avg_gain"] / data["avg_loss"]))
    
    #Signals
    



