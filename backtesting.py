import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def backtest_strategy(data):
    #let's try to account for intraday
    data["return"] = (data["close"] - data["open"]) / data["open"]
    data["cumulative_return"] = (1 + data["return"]).cumprod()
    data["position"] = data["signal"].shift(1) #if long, 1. if short, -1. if flat, 0.

    #atrs
    data.loc[data["signal"] == 1, "stoploss_long"] = data["open"] - 1.5 * data["atr"]
    data.loc[data["signal"] == -1, "stoploss_short"] = data["open"] + 1.5 * data["atr"]
    #active trade?
    ///////
    I'M STUCK HERE
    //////


    data.loc[(data["high"] > data["stoploss_short"]) & (data["active"] == True), "position"] = 0
    data.loc[(data["low"] < data["stoploss_long"]) & (data["active"] == True), "position"] = 0

    #calculating return
    data["strategy"] = data["return"] * data["position"]
    data["cumulative_strategy"] = (1 + data["strategy"]).cumprod()

