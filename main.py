import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
symbol = "AAPL"
print(symbol)
print()
data = yf.download(symbol, start="2024-01-01", end="2024-12-31", progress=False)
# Check what type the "data" is
# print(type(data))
print()
data = data.drop(["High", "Low", "Open", "Volume"], axis=1)
print(data)
print()
# Below calculates (final-initial)/initial
data["Return"] = data["Close"].pct_change()
print(data)
print()

# 2. Strategy Rules: Moving Average Crossover
short_window = 50
# Making it smaller given the narrow data set
# short_window = 2
long_window = 200

data["SMA50"] = data["Close"].rolling(short_window).mean()
data["SMA200"] = data["Close"].rolling(long_window).mean()
print(data)
print()

# Buy when SMA50 > SMA200, sell when SMA50 < SMA200
data["Signal"] = 0
data.loc[data["SMA50"] > data["SMA200"], "Signal"] = 1  # long
data["Position"] = data["Signal"].shift(1)  # avoid look-ahead bias
print(data)
print()


# # 3. Portfolio Performance
data["StrategyReturn"] = data["Position"] * data["Return"]

# # Cumulative returns
data["CumulativeMarket"] = (1 + data["Return"]).cumprod()
data["CumulativeStrategy"] = (1 + data["StrategyReturn"]).cumprod()

# # 4. Plot Results
plt.figure(figsize=(12, 6))
plt.plot(data["CumulativeMarket"], label=f"{symbol} Buy & Hold")
plt.plot(data["CumulativeStrategy"], label="Strategy (SMA 50/200)")
plt.legend()
plt.title("Backtest: Moving Average Crossover Strategy")
plt.show()

# # 5. Simple Performance Metrics
# cagr = (data["CumulativeStrategy"].iloc[-1]) ** (1 / 5) - 1  # ~5 years
# volatility = data["StrategyReturn"].std() * (252**0.5)
# sharpe = (data["StrategyReturn"].mean() * 252) / volatility

# print(f"CAGR: {cagr:.2%}")
# print(f"Volatility: {volatility:.2%}")
# print(f"Sharpe Ratio: {sharpe:.2f}")
