
from agents.thought_selector import select_next_thought
from agents.tool_registry import resolve_tool
from agents.state_manager import initialize_state, add_to_state, get_state_log
from framework.fallback_handler import replan_thought

def run_stock_tot_agent(stock_symbol, max_steps=10):
    state = initialize_state(stock_symbol)

    print(f"\n--- Agentic Reasoning for {stock_symbol.upper()} ---")
    for step in range(max_steps):
        thought = select_next_thought(stock_symbol, get_state_log(state))
        print(f"\n[Step {step+1}] Thought: {thought}")

        if thought.lower().startswith("final decision"):
            print(f"[Agent Conclusion] {thought}")
            break

        result = resolve_tool(thought, stock_symbol, state)

        if "No known tool" in result:
            print(f"[Fallback Triggered] Replanning thought...")
            thought = replan_thought(thought, get_state_log(state))
            print(f"[Replanned Thought] {thought}")
            continue

        add_to_state(state, thought, result)
        print(f"[Step {step+1}] Result: {result}")

    return state
