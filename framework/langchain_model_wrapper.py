
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model_name="gpt-4", temperature=0.2)

def query_langchain_llm(prompt, model="gpt-4"):
    messages = [
        SystemMessage(content="You are a stock market analysis assistant for Indian equities."),
        HumanMessage(content=prompt)
    ]
    response = llm(messages)
    return response.content
