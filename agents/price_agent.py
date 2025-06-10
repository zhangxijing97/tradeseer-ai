from google.adk.agents import Agent
import yfinance as yf

def get_stock_price(ticker: str):
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice", "Price not available")
    return {"price": price, "ticker": ticker}

price_agent = Agent(
    name="price_agent",
    model="gemini-2.0-flash",
    description="Agent retrieves current stock prices.",
    instruction="Fetch stock price using get_stock_price tool.",
    tools=[get_stock_price],
)