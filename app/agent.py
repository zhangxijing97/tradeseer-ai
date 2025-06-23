from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .tools.tools import get_current_time
from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.news_analyst.agent import news_analyst

from .sub_agents.linear_regression_predictor.agent import linear_regression_agent
from .sub_agents.prophet_predictor.agent import prophet_agent
from .sub_agents.gru_predictor.agent import gru_agent
from .sub_agents.lstm_predictor.agent import lstm_agent

root_agent = Agent(
    name="tradeseer",
    model="gemini-2.0-flash",
    description="Core agent of TradeSeer-AI: routes financial queries for stock prices, market news, and AI-powered price predictions using models like Linear Regression, LSTM, GRU, LightGBM, and Prophet.",
    instruction="""
    You are the core agent of TradeSeer-AI — a financial assistant that routes user queries to the appropriate analysis tool.

    Responsibilities:
    - For stock price lookup, use `stock_analyst`.
    - For news-related questions, use `news_analyst`.
    - For current time requests, use `get_current_time`.
    - For stock price prediction:
        - If the user mentions a method (e.g., "using LSTM", "with Prophet", "via GRU"), call that specific tool.
        - If the method is not specified, ask:
        "Which prediction method would you like to use: Linear Regression, LSTM, GRU, or Prophet?"
        - After user confirms, pass the query to the corresponding prediction tool with their input.

    Always be clear, context-aware, and accurate. If a query is ambiguous, ask a clarifying question before selecting a tool.
    """,
    tools=[
        get_current_time,
        AgentTool(stock_analyst),
        AgentTool(news_analyst),
        AgentTool(linear_regression_agent),
        AgentTool(prophet_agent),
        AgentTool(gru_agent),
        AgentTool(lstm_agent),
    ],
)