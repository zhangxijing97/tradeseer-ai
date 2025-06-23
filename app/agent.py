from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .tools.tools import get_current_time
from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.news_analyst.agent import news_analyst

from .sub_agents.linear_regression_predictor.agent import linear_regression_agent
from .sub_agents.lstm_predictor.agent import lstm_agent

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="A tool-based manager agent that handles stock price lookups, news analysis, and price forecasting using linear and LSTM-based models.",
    instruction="""
    You are a manager agent responsible for routing stock-related queries to the appropriate tool.

    Responsibilities:
    - For stock price lookup, use `stock_analyst`.
    - For news queries, use `news_analyst`.
    - For time questions, use `get_current_time`.
    - For price prediction:
        - If the user specifies a method (e.g., "using LSTM" or "with linear regression"), use the corresponding tool.
        - If the method is not specified, ask the user: "Would you like to use Linear Regression or LSTM for the prediction?"

    Be smart in interpreting the user's intent and ask for clarification if needed before proceeding.
    """,
    tools=[
        get_current_time,
        AgentTool(stock_analyst),
        AgentTool(news_analyst),
        AgentTool(linear_regression_agent),
        AgentTool(lstm_agent),
    ],
)