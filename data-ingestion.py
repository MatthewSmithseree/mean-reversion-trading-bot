import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def fetch_stock_data(ticker, startdate, enddate):
    data = yf.download(ticker, start = startdate, end = enddate)
    return data

print(fetch_stock_data("AAPL", "2019-01-01", "2019-01-15"))
