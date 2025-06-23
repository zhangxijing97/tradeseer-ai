from google.adk.agents import Agent
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

def linear_regression(input: dict) -> dict:
    try:
        ticker = input.get("ticker")
        days_ahead = input.get("days_ahead", 1)  # default to 1 day if not specified

        if not ticker:
            return {"status": "error", "error_message": "Missing 'ticker' in input."}

        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")

        if hist.empty or "Close" not in hist:
            return {"status": "error", "error_message": f"No historical data for {ticker}"}

        prices = hist["Close"].values
        days = np.arange(len(prices)).reshape(-1, 1)

        model = LinearRegression()
        model.fit(days, prices)

        future_day = np.array([[len(prices) + days_ahead - 1]])  # e.g. 5 days ahead
        prediction = model.predict(future_day)[0]

        return {
            "status": "success",
            "ticker": ticker,
            "days_ahead": days_ahead,
            "predicted_price": round(prediction, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

linear_regression_agent = Agent(
    name="linear_regression_agent",
    model="gemini-2.0-flash",
    description="Predicts a future stock price using linear regression on all historical data.",
    instruction="""
    You are a price prediction agent.

    Use the linear_regression tool to predict future prices for a given stock.
    Input is a dictionary with:
    - 'ticker': the stock symbol
    - 'days_ahead': number of days into the future to predict (default is 1)

    Respond with the predicted price, days ahead, and timestamp.
    """,
    tools=[linear_regression],
)