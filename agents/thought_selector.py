
from framework.langchain_model_wrapper import query_langchain_llm

def select_next_thought(stock_symbol, state_log):
    summary = "\n".join([f"Step {i+1}: Thought: {t} | Result: {r}" for i, (t, r) in enumerate(state_log)])
    prompt = f"""
You are reasoning about the Indian stock {stock_symbol}.
Here is what you have thought and observed so far:

{summary}

Based on this, what is the next reasoning step you want to take?
Respond only with a single clear thought or say 'FINAL DECISION:' if you are ready to conclude.
"""
    return query_langchain_llm(prompt).strip()
