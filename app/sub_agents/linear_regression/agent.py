from google.adk.agents import Agent
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

def linear_regression(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")

        if hist.empty:
            return {"status": "error", "error_message": f"No historical data for {ticker}"}

        prices = hist["Close"].values
        days = np.arange(len(prices)).reshape(-1, 1)

        model = LinearRegression()
        model.fit(days, prices)

        next_day = np.array([[len(prices)]])
        prediction = model.predict(next_day)[0]

        return {
            "status": "success",
            "ticker": ticker,
            "predicted_price": round(prediction, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

linear_regression_predictor = Agent(
    name="linear_regression_predictor",
    model="gemini-2.0-flash",
    description="Predicts the next day's stock price using linear regression.",
    instruction="""
You are a price prediction agent.

When given a stock ticker, use the linear_regression tool to predict its price for the next trading day.
Respond with the predicted price and the current timestamp.
""",
    tools=[linear_regression],
)