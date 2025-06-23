from google.adk.agents import Agent
from datetime import datetime
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

def gru_predictor(input: dict) -> dict:
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

        prices = hist["Close"].values.reshape(-1, 1)
        if len(prices) < 60:
            return {"status": "error", "error_message": "Not enough data for GRU (need 60+ days)."}

        scaler = MinMaxScaler()
        scaled_prices = scaler.fit_transform(prices)

        X, y = [], []
        for i in range(60, len(scaled_prices)):
            X.append(scaled_prices[i - 60:i])
            y.append(scaled_prices[i])
        X, y = np.array(X), np.array(y)

        model = Sequential()
        model.add(GRU(50, return_sequences=False, input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X, y, epochs=10, batch_size=16, verbose=0)

        # Predict multiple days ahead
        last_60 = scaled_prices[-60:].reshape(1, 60, 1)
        for _ in range(days_ahead):
            predicted_scaled = model.predict(last_60, verbose=0)
            last_60 = np.append(last_60[:, 1:, :], [[predicted_scaled[0]]], axis=1)

        predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]

        return {
            "status": "success",
            "ticker": ticker.upper(),
            "days_ahead": days_ahead,
            "predicted_price": round(float(predicted_price), 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

gru_agent = Agent(
    name="gru_agent",
    model="gemini-2.0-flash",
    description="Predicts future stock prices using a GRU model.",
    instruction="""
    Use the gru_predictor tool to forecast a stock's price.

    Input format:
    {
        'ticker': 'TSLA',
        'days_ahead': 5
    }

    Return the predicted price and timestamp.
    """,
    tools=[gru_predictor],
)