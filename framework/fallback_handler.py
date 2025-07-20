
from framework.langchain_model_wrapper import query_langchain_llm

def replan_thought(thought, state_log):
    context = "\n".join([f"Step {i+1}: {t} | {r}" for i, (t, r) in enumerate(state_log)])
    prompt = f"""
You requested: '{thought}', but I have no tool to perform that task.

Here is what you've done so far:
{context}

Please refine your request or propose a new thought that can be performed using tools like: sentiment, earnings, technical, macro, fii, or budget.

Respond with a revised thought or say 'FINAL DECISION:' if you wish to conclude.
"""
    return query_langchain_llm(prompt).strip()
