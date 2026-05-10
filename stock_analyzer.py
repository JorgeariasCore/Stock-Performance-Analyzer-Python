import yfinance as yf
import pandas as pd
import numpy as np
#Configuration
TICKERS = ["AAPL", "MSFT", "GOOGL", "SPY"]
START_DATE = "2023-01-01"
END_DATE = "2026-01-01"
#Download data
def download_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)
    if "Close" in data.columns:
        close_prices = data["Close"]
    else:
        close_prices = data
    close_prices = close_prices.dropna(how="all")#Delate all empty rows
    return close_prices

def calculate_daily_returns(prices):
    return prices.pct_change().dropna()# calculate the percentage change between one value and the previous one.
    
def calculate_cumulative_returns(daily_returns):
    return (1 + daily_returns).cumprod() - 1 #cumulative return instead of growth
def calculate_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252) ## Annualized volatility assuming 252 trading days
def calculate_moving_averages(prices, short_window=20, long_window=50):
    ma_short = prices.rolling(window=short_window).mean() #Moving average for 20 day
    ma_long = prices.rolling(window=long_window).mean() #moving average for 50 day
    return ma_short, ma_long
def best_and_worst_days(daily_returns):
    summary = {}
    for ticker in daily_returns.columns:
        best_day = daily_returns[ticker].idxmax() #ask for the index (position/label) where the maximum value occurs.
        worst_day = daily_returns[ticker].idxmin() #ask for the index (position/label) where the minimum value occurs

        summary[ticker] = {# made a frame with this data
            "best_day_date": best_day, 
            "best_day_return": daily_returns[ticker].max(), #show the best day
            "worst_day_date": worst_day,
            "worst_day_return": daily_returns[ticker].min(), # show the value of worst day
        }
    return summary
def build_summary(prices, daily_returns, cumulative_returns):
    summary = pd.DataFrame(index=prices.columns) #made a pd for all data frame for all information

    summary["Last Price"] = prices.iloc[-1] #show the las day price
    summary["Mean Daily Return"] = daily_returns.mean() #show the Mean daily Return
    summary["Volatility (Annualized)"] = daily_returns.std() * np.sqrt(252)
    summary["Total Cumulative Return"] = cumulative_returns.iloc[-1]

    return summary.sort_values(by="Last Price", ascending=False) # ascending show the data in acending order by the name of the column
# Main Power
def main():
    print("Downloading stock data...")
    prices = download_data(TICKERS, START_DATE, END_DATE)
    print("\nClose Price:")
    print(prices.tail()) #show only 5 las rows

    daily_returns = calculate_daily_returns(prices)
    cumulative_returns = calculate_cumulative_returns(daily_returns)
    volatility = calculate_volatility(daily_returns)
    ma_20, ma_50 = calculate_moving_averages(prices)
    extremes = best_and_worst_days(daily_returns)
    summary = build_summary(prices, daily_returns, cumulative_returns)

    print("\n================ SUMMARY TABLE ================\n")
    print(summary)

    print("\n================ VOLATILITY ================\n")
    print(volatility)
    print("\n================ BEST AND WORST DAYS ================\n")
    for ticker, values in extremes.items():
        print(f"{ticker}:")
        print(f"  Best Day:  {values['best_day_date'].date()} | Return: {values['best_day_return']:.2%}")
        print(f"  Worst Day: {values['worst_day_date'].date()} | Return: {values['worst_day_return']:.2%}")
        print()
    print("\n================ LAST MOVING AVERAGES ================\n")
    for ticker in prices.columns:
        print(f"{ticker}:")
        print(f"  Last Price: {prices[ticker].iloc[-1]:.2f}")
        print(f"  20-Day MA:  {ma_20[ticker].iloc[-1]:.2f}")
        print(f"  50-Day MA:  {ma_50[ticker].iloc[-1]:.2f}")
        print()
if __name__ == "__main__":
    main()