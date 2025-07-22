from framework.langgraph_engine import build_stock_graph

def main():
    stock_symbol = input("Enter stock symbol (e.g., INFY): ").strip().upper()
    app = build_stock_graph()

    final_state = app.invoke(
        {"stock_symbol": stock_symbol, "log": []},
        config={"recursion_limit": 50}
    )

    print("\n--- Final State ---")
    for step, (thought, result) in enumerate(final_state["log"], 1):
        print(f"Step {step}:\nThought: {thought}\nResult: {result}\n")

if __name__ == "__main__":
    main()
