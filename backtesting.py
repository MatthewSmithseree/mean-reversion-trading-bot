import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def backtest_strategy(data):
    #let's try to account for intraday
    data["return"] = (data["close"] - data["open"]) / data["open"]
    data["cumulative_return"] = (1 + data["return"]).cumprod()

    #dynamic trailing stop loss

    for i in range(1, len(data)):
        if i == 1:
            #long
            prev_stoploss_long = data.at[1, "open"] - 1.5 * data.at[1, "atr"]
            data.at[1, "stoploss_long"]  = prev_stoploss_long 
            #short
            prev_stoploss_short = data.at[1, "open"] + 1.5 * data.at[1, "atr"]
            data.at[1, "stoploss_short"] = prev_stoploss_short
            #initial position
            data.at[1, "position"] = 1 
        else:
   
            if data.at[i, "position"] == 0:
                data.at[i, "position"] = data.at[i-1, "signal"]     
                if data.at[i-1, "signal"] == 1:
                    #trigger
                    if data.at[i, "low"] < data.at[i, "stoploss_long"]:
                        data.at[i, "position"] = 0  
                    else:
                        data.at[i, "stoploss_long"] = max(prev_stoploss_long, data.at[i, "close"] - data.at[i, "atr"] * 1.5)
                    prev_stoploss_long = data.at[i, "stoploss_long"] 
                elif data.at[i-1, "signal"] == -1:
                    #trigger
                    if data.at[i, "high"] > data.at[i, "stoploss_short"]:
                        data.at[i, "position"] = 0 
                    else:
                        data.at[i, "stoploss_short"] = min(prev_stoploss_short, data.at[i, "close"] + data.at[i, "atr"] * 1.5)
                    prev_stoploss_short = data.at[i, "stoploss_short"]                

    #calculating return
    data["strategy"] = data["return"] * data["position"]
    data["cumulative_strategy"] = (1 + data["strategy"]).cumprod()
    
    return data

