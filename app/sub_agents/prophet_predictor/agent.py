from google.adk.agents import Agent
from prophet import Prophet
import yfinance as yf
import pandas as pd
from datetime import datetime

def prophet_predictor(input: dict) -> dict:
    try:
        ticker = input.get("ticker")
        days_ahead = input.get("days_ahead", 1)

        if not ticker:
            return {"status": "error", "error_message": "Missing 'ticker'"}
        if not isinstance(days_ahead, int) or days_ahead < 1:
            return {"status": "error", "error_message": "'days_ahead' must be a positive integer."}

        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        if hist.empty or "Close" not in hist:
            return {"status": "error", "error_message": f"No historical data for {ticker}"}

        # Prepare DataFrame for Prophet
        df = hist[["Close"]].reset_index()
        df["Date"] = df["Date"].dt.tz_localize(None)  # Remove timezone info
        df.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)

        # Train Prophet
        model = Prophet()
        model.fit(df)

        # Forecast n days into the future
        future = model.make_future_dataframe(periods=days_ahead)
        forecast = model.predict(future)

        # Extract forecast for requested future day
        predicted = forecast.iloc[-1]["yhat"]

        return {
            "status": "success",
            "ticker": ticker.upper(),
            "days_ahead": days_ahead,
            "predicted_price": round(predicted, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)} 

prophet_agent = Agent(
    name="prophet_agent",
    model="gemini-2.0-flash",
    description="Predicts stock prices using Facebook Prophet time series forecasting.",
    instruction="""
    Use the prophet_predictor tool to forecast a stock's price N days into the future.
    
    Input should be a dictionary:
    - 'ticker': stock symbol (e.g., AAPL)
    - 'days_ahead': how many days from today to predict (e.g., 5)

    Return the predicted price and timestamp.
    """,
    tools=[prophet_predictor],
)