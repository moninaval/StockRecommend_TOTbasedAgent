
def generate_thought(stock_symbol, state):
    # Simulated sentiment analysis
    sentiment = "positive" if stock_symbol.lower() in ["reliance", "tcs"] else "neutral"
    return f"Sentiment for {stock_symbol} is {sentiment} based on recent news headlines."
