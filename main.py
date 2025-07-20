
from framework.langgraph_engine import build_stock_graph

def main():
    stock_symbol = input("Enter stock symbol (e.g., INFY): ").strip().upper()
    graph = build_stock_graph()
    final_state = graph.invoke({"stock_symbol": stock_symbol, "log": []})

    print("\n--- Final State ---")
    for step, (thought, result) in enumerate(final_state["log"], 1):
        print(f"Step {step}:")
        print(f"Thought: {thought}")
        print(f"Result: {result}\n")

if __name__ == "__main__":
    main()
