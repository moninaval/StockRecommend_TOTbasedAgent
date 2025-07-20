
from agents.stock_tot_agent import run_stock_tot_agent

def main():
    stock_symbol = input("Enter the Indian stock symbol (e.g., RELIANCE, TCS): ").strip().upper()
    state = run_stock_tot_agent(stock_symbol)

    print("\nFinal State Summary:")
    for key, value in state.items():
        print(f" - {key}: {value}")

if __name__ == "__main__":
    main()
