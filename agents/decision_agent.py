from google.adk.agents import Agent

def decision_tool(prediction: str):
    if "increase" in prediction.lower():
        decision = "BUY"
    elif "decrease" in prediction.lower():
        decision = "SELL"
    else:
        decision = "HOLD"
    return {"decision": decision}

decision_agent = Agent(
    name="decision_agent",
    model="gemini-2.0-flash",
    description="Agent making trading decisions based on predictions.",
    instruction="Use decision_tool to interpret predictions into trading actions (buy/sell/hold).",
    tools=[decision_tool],
)