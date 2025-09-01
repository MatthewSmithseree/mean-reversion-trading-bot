import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

data = yf.download("AAPL", start="2020-01-01", end="2021-01-01")

data.columns = data.columns.get_level_values(0)

print(data)
