import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def fetch_stock_data(ticker, startdate, enddate):
    data = yf.download(ticker, start = startdate, end = enddate)
    #rename columns
    data = data.rename(columns= {"Open": "open", "Close": "close", "High": "high", "Low": "low"})
    #Adj Close & Volume will remain unchanged
    return data
