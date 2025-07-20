
from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnableMap
from langchain_core.runnables.graph import Graph
from framework.langchain_model_wrapper import query_langchain_llm
from agents.tool_registry import resolve_tool
from framework.fallback_handler import replan_thought

# --- Nodes as Functions ---

def select_thought_node(inputs):
    stock_symbol, state_log = inputs["stock_symbol"], inputs["log"]
    summary = "\n".join([f"{i+1}. {t} | {r}" for i, (t, r) in enumerate(state_log)])
    prompt = f"""
You are analyzing the stock {stock_symbol}. Here are the reasoning steps so far:
{summary}

Propose the next step or say 'FINAL DECISION: ...'
"""
    thought = query_langchain_llm(prompt)
    return {"thought": thought.strip(), "stock_symbol": stock_symbol, "log": state_log}

def check_tool_or_finalize(inputs):
    thought = inputs["thought"]
    if thought.lower().startswith("final decision"):
        return "end"
    known_tools = ["sentiment", "earnings", "technical", "macro", "fii", "budget"]
    if any(k in thought.lower() for k in known_tools):
        return "run_tool"
    return "replan"

def run_tool_node(inputs):
    thought, stock_symbol, log = inputs["thought"], inputs["stock_symbol"], inputs["log"]
    result = resolve_tool(thought, stock_symbol, log)
    return {"stock_symbol": stock_symbol, "log": log + [(thought, result)]}

def replan_node(inputs):
    thought, stock_symbol, log = inputs["thought"], inputs["stock_symbol"], inputs["log"]
    replanned = replan_thought(thought, log)
    return {"thought": replanned, "stock_symbol": stock_symbol, "log": log}

# --- Build LangGraph ---
def build_stock_graph():
    g = Graph()

    g.add_node("select_thought", RunnableLambda(select_thought_node))
    g.add_node("run_tool", RunnableLambda(run_tool_node))
    g.add_node("replan", RunnableLambda(replan_node))
    g.add_node("end", lambda x: x)

    g.set_entry_point("select_thought")

    g.add_conditional_edges("select_thought", RunnableLambda(check_tool_or_finalize), {
        "run_tool": "run_tool",
        "replan": "replan",
        "end": "end"
    })

    g.add_edge("run_tool", "select_thought")
    g.add_edge("replan", "select_thought")

    return g
