from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

# Load API key from environment variable or .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.2,
    openai_api_key="sk-ownkey"
)

def query_langchain_llm(prompt: str, model: str = "gpt-4") -> str:
    messages = [
        SystemMessage(content="You are a stock market analysis assistant for Indian equities."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)  # ✅ use .invoke instead of calling directly
    return response.content.strip()
