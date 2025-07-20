
def generate_thought(stock_symbol, state):
    # Simulated budget/policy impact
    impact = "positive" if stock_symbol.lower() in ["l&t", "adani"] else "minimal"
    return f"Union Budget has a {impact} impact on {stock_symbol} due to infra or tax policy."
