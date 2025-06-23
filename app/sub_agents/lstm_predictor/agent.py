from google.adk.agents import Agent
from datetime import datetime
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def lstm_predictor(input: dict) -> dict:
    try:
        ticker = input.get("ticker")
        days_ahead = input.get("days_ahead", 1)

        if not ticker:
            return {"status": "error", "error_message": "Missing 'ticker'."}

        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")

        if hist.empty or "Close" not in hist:
            return {"status": "error", "error_message": f"No historical data for {ticker}"}

        prices = hist["Close"].values.reshape(-1, 1)
        if len(prices) < 60:
            return {"status": "error", "error_message": "Not enough data for LSTM (need at least 60 days)."}

        # Normalize price data
        scaler = MinMaxScaler()
        scaled_prices = scaler.fit_transform(prices)

        # Prepare training data (sliding window of 60 days)
        X, y = [], []
        for i in range(60, len(scaled_prices)):
            X.append(scaled_prices[i - 60:i])
            y.append(scaled_prices[i])
        X, y = np.array(X), np.array(y)

        # Build and train the LSTM model
        model = Sequential()
        model.add(LSTM(50, return_sequences=False, input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X, y, epochs=10, batch_size=16, verbose=0)

        # Predict forward for N days
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

lstm_agent = Agent(
    name="lstm_agent",
    model="gemini-2.0-flash",
    description="Predicts future stock prices using an LSTM model.",
    instruction="""
    Use the lstm_predictor tool to predict a stock's future price based on recent historical data.

    The user will provide:
    - 'ticker': stock symbol (e.g. AAPL)
    - 'days_ahead': number of future days to forecast

    Respond with the predicted price and timestamp.
    """,
    tools=[lstm_predictor],
)