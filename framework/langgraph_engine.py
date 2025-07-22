from typing import TypedDict, List, Tuple, Optional
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END

from framework.langchain_model_wrapper import query_langchain_llm
from agents.tool_registry import resolve_tool
from framework.fallback_handler import replan_thought


# Shared state passed between nodes
class StockState(TypedDict, total=False):
    stock_symbol: str
    log: List[Tuple[str, str]]
    thought: Optional[str]


# --- Node: Select next thought or final decision ---
# --- Node: Select next thought or final decision ---
def select_thought_node(state: StockState) -> StockState:
    stock_symbol = state["stock_symbol"]
    state_log = state.get("log", []) # Get existing log
    summary = "\n".join([f"{i+1}. {t} | {r}" for i, (t, r) in enumerate(state_log)]) or "(no prior steps)"

    prompt = f"""
You are analyzing the stock {stock_symbol}.
Here are the reasoning steps so far:
{summary}

Now think carefully. If enough analysis is done, respond with:
FINAL DECISION: <Buy/Hold/Sell with reason>.

Otherwise, propose the next step.
"""
    if len(state_log) >= 4:
        prompt += "\n\nYou've done multiple steps. It's time to give a FINAL DECISION now."

    print("\n[LangGraph] 🧠 Calling LLM with this prompt:\n" + prompt)
    thought = query_langchain_llm(prompt).strip() #
    print(f"[LangGraph] 🧠 Received Thought:\n{thought}\n")

    # Add the newly generated thought to the log immediately
    # Initialize with None for the result, which will be filled later by run_tool_node
    updated_log = state_log + [(thought, None)]

    return {**state, "thought": thought, "log": updated_log} #
# --- Node: Decide where to go next ---
def check_tool_or_finalize(state: StockState) -> str:
    thought = (state.get("thought") or "").strip().lower()
    log_len = len(state.get("log", []))

    print(f"[Router] 🔍 Thought: {thought}")
    print(f"[Router] 📚 Log Length: {log_len}")

    if log_len >= 10:
        print("[Router] ⚠️ Emergency exit: too many reasoning steps")
        return END

    if thought.startswith("final decision"):
        print("[Router] ✅ Detected FINAL DECISION")
        return END

    known_tools = ["sentiment", "earnings", "technical", "macro", "fii", "budget"]
    if any(tool in thought for tool in known_tools):
        print("[Router] 🔧 Routed to run_tool")
        return "run_tool"

    print("[Router] 🔄 No matching tool, routing to replan")
    return "replan"


# --- Node: Run tool based on LLM thought ---
# --- Node: Run tool based on LLM thought ---
def run_tool_node(state):
    log = state.get("log", [])
    stock_symbol = state["stock_symbol"]

    # The thought to be executed is the last one added to the log,
    # which we now expect to be (thought, None)
    if not log or log[-1][1] is not None: # Ensure there's a thought to execute and it hasn't been executed yet
        # This case should ideally not be hit with the fix in select_thought_node,
        # but it's good for robustness.
        # If it happens, it means run_tool_node was called without a pending thought.
        raise ValueError("No unexecuted thought found in log for tool execution.")

    # Get the thought that needs to be executed
    thought_to_execute = log[-1][0] # Get the thought part of the last tuple

    print(f"\n🚀 TOOL EXECUTION for: {thought_to_execute}")
    result = resolve_tool(thought_to_execute, stock_symbol, state)
    print(f"🔁 TOOL RESULT: {result}")

    # Update the last entry in the log with the result
    updated_log = log[:-1] + [(thought_to_execute, result)] #

    return {
        "stock_symbol": stock_symbol,
        "log": updated_log,
        "thought": thought_to_execute # Optionally, keep the current thought if needed for the next step's context
    }
def replan_node(state):
    thought = state.get("thought", "")
    log = state.get("log", [])
    print(f"\n🧠 Replanning thought: {thought}")
    print(f"🧾 Log so far: {[t for t, _ in log]}")

    new_thought = replan_thought(thought, log)
    print(f"🔁 New Thought: {new_thought}")
    return {**state, "thought": new_thought}

def build_stock_graph():
    g = StateGraph(StockState)

    # Wrap each node
    select_thought_lambda = RunnableLambda(select_thought_node)
    check_tool_lambda = RunnableLambda(check_tool_or_finalize)
    run_tool_lambda = RunnableLambda(run_tool_node)
    replan_lambda = RunnableLambda(replan_node)

    # Add nodes
    g.add_node("select_thought", select_thought_lambda)
    g.add_node("run_tool", run_tool_lambda)
    g.add_node("replan", replan_lambda)

    # Set entry point
    g.set_entry_point("select_thought")

    # Conditional decision
    g.add_conditional_edges("select_thought", check_tool_lambda, {
        "run_tool": "run_tool",
        "replan": "replan",
        END: END
    })

    # Loops
    g.add_edge("run_tool", "select_thought")
    g.add_edge("replan", "select_thought")

    return g.compile()
