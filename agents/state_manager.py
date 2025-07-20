
def initialize_state(stock_symbol):
    return {
        "symbol": stock_symbol,
        "log": []  # list of (thought, result) tuples
    }

def add_to_state(state, thought, result):
    state["log"].append((thought, result))

def get_state_log(state):
    return state["log"]
