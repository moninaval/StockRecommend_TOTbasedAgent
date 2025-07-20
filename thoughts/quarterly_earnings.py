
def generate_thought(stock_symbol, state):
    # Simulated earnings summary
    earnings_result = "beat expectations" if stock_symbol.lower() in ["infosys", "hdfc"] else "met expectations"
    return f"{stock_symbol} has recently released earnings that {earnings_result}."
