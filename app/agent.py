from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.news_analyst.agent import news_analyst
from .tools.tools import get_current_time

from .sub_agents.linear_regression_predictor.agent import linear_regression_predictor
from .sub_agents.lstm_predictor.agent import lstm_predictor_agent

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="A unified manager agent that uses tools to perform tasks like stock lookup, price forecasting, news analysis, and time reporting.",
    instruction="""
    You are a manager agent that uses tools to complete tasks directly.

    You have access to the following tools:
    - `stock_analyst`: for retrieving current stock prices.
    - `linear_regression_predictor`: for predicting future stock prices using trend-based modeling.
    - `news_analyst`: for summarizing current news about companies or the market.
    - `get_current_time`: for returning the current date and time.

    Determine the user's intent and use the appropriate tool to fulfill the request.
    Do not invent information — only respond with data retrieved through the tools.
    If a request is ambiguous or missing input (e.g. no ticker), politely ask for clarification.
    """,
    tools=[
        get_current_time,
        AgentTool(stock_analyst),
        AgentTool(news_analyst),
        AgentTool(linear_regression_predictor),
    ],
)