
from thoughts.stock_sentiment import generate_thought as sentiment
from thoughts.quarterly_earnings import generate_thought as earnings
from thoughts.technical_indicators import generate_thought as technical
from thoughts.macro_market import generate_thought as macro
from thoughts.fii_dii_flows import generate_thought as fii_dii
from thoughts.budget_policy_impact import generate_thought as budget

tool_map = {
    "sentiment": sentiment,
    "earnings": earnings,
    "technical": technical,
    "macro": macro,
    "fii": fii_dii,
    "budget": budget
}

def resolve_tool(thought, stock_symbol, state):
    for key in tool_map:
        if key in thought.lower():
            return tool_map[key](stock_symbol, state)
    return f"No known tool matched for: '{thought}'"
