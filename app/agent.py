from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.stock_analyst.agent import stock_analyst
from .sub_agents.linear_regression.agent import linear_regression_predictor
from .sub_agents.news_analyst.agent import news_analyst
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="A manager agent that coordinates tasks between sub-agents and tools.",
    instruction="""
    You are a manager agent overseeing task delegation.

    Responsibilities:
    - For stock-related questions, delegate to the `stock_analyst` sub-agent.
    - For price prediction questions, delegate to the `linear_regression_predictor` sub-agent.
    - For news-related queries, use the `news_analyst` tool to fetch and summarize news.
    - For time-related questions (e.g., "today", "now"), use the `get_current_time` tool.

    Be smart in choosing which resource to use based on the user's intent.
    Do not default to any one agent—route queries based on topic.
    """,
    sub_agents=[stock_analyst, linear_regression_predictor],
    # sub_agents=[stock_analyst],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)