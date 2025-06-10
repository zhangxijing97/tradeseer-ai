from google.adk.agents import Agent

def fake_price_prediction(ticker: str):
    # Fake predictive logic for demonstration purposes
    return {
        "ticker": ticker,
        "prediction": "The stock price is predicted to increase over the next 10 days with moderate confidence."
    }

prediction_agent = Agent(
    name="prediction_agent",
    model="gemini-2.0-flash",
    description="Agent that predicts stock price movements.",
    instruction="Generate a short-term prediction about stock price movements.",
    tools=[fake_price_prediction],
)