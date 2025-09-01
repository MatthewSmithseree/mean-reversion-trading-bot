import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def backtest_strategy(data):
   data["signal"] = data["signal"].fillna(0)
   data["position"] = data["signal"].shift(1)
   data["return"] = data["close"].pct_change()
   data["cumulative_return"] = (1 + data["return"]).cumprod()
   data["strategy"] = data["return"] * data["position"]
   data["cumulative_strategy"] = (1 + data["strategy"]).cumprod()

   cum_return = data["cumulative_return"].iloc[-1]
   cum_strategy = data["cumulative_strategy"].iloc[-1]

   #sharpe
   daily_volatility = data["strategy"].std()
   avg_daily_return = data["strategy"].mean()
   avg_risk_free = 0.04396 / 252 #10 year treasury t bill
   sharpe_ratio = (avg_daily_return - avg_risk_free) / (daily_volatility) * np.sqrt(252)

   #max drawdown


   #gains & losses
   gains = 0
   losses = 0
   for i in data["strategy"]:
      if i > 0:
         gains += 1
      elif i < 0:
         losses += 1
   #winrate
   winrate = gains / (gains + losses)


   print()
   print('Evaluation Metrics:')
   print('-----------------------------------')
   print()
   print(f"Gains: {gains}")
   print(f"Losses: {losses}")
   print(f"Win Rate: {winrate}")
   print(f"Stock return: {cum_return:.3f}")
   print(f"Strategy returns: {cum_strategy:.3f}")
   print(f"Sharpe Ratio: {sharpe_ratio:.3f}")

   return data



 # #dynamic trailing stop loss
    # for i in range(1, len(data)):
    #     if i == 1:
    #         #long
    #         prev_stoploss_long = data.at[1, "open"] - 1.5 * data.at[1, "atr"]
    #         data.at[1, "stoploss_long"]  = prev_stoploss_long 
    #         #short
    #         prev_stoploss_short = data.at[1, "open"] + 1.5 * data.at[1, "atr"]
    #         data.at[1, "stoploss_short"] = prev_stoploss_short
    #         #initial position
    #         data.at[1, "position"] = 1 
    #     else:
    #         if data.at[i, "position"] == 0:
    #             data.at[i, "position"] = data.at[i-1, "signal"]     
    #             if data.at[i-1, "signal"] == 1:
    #                 #check stoploss
    #                 if data.at[i, "low"] < data.at[i, "stoploss_long"]:
    #                     data.at[i, "position"] = 0  
    #                 else:
    #                     data.at[i, "stoploss_long"] = max(prev_stoploss_long, data.at[i, "close"] - data.at[i, "atr"] * 1.5)
    #                 prev_stoploss_long = data.at[i, "stoploss_long"] 
    #             elif data.at[i-1, "signal"] == -1:
    #                 #check stoploss
    #                 if data.at[i, "high"] > data.at[i, "stoploss_short"]:
    #                     data.at[i, "position"] = 0 
    #                 else:
    #                     data.at[i, "stoploss_short"] = min(prev_stoploss_short, data.at[i, "close"] + data.at[i, "atr"] * 1.5)
    #                 prev_stoploss_short = data.at[i, "stoploss_short"]                