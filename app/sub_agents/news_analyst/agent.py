from google.adk.agents import Agent
from google.adk.tools import google_search

news_analyst = Agent(
    name="news_analyst",
    model="gemini-2.0-flash",
    description="Fetches and summarizes current news using search.",
    instruction="""
    Use google_search to retrieve recent news based on the user's query.
    If the query is time-based (e.g., "today's news"), use get_current_time for context.
    """,
    tools=[google_search],
)