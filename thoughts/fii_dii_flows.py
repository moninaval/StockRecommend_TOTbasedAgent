
def generate_thought(stock_symbol, state):
    # Simulated FII/DII flows
    fii_flow = -1200  # INR Crore
    dii_flow = 900
    return f"FII net selling ₹{abs(fii_flow)} Cr, DII net buying ₹{dii_flow} Cr, showing mixed institutional sentiment for {stock_symbol}."
