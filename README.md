
# 🧠 ToT Stock Decider (Indian Markets)

A modular AI agentic framework that uses Tree-of-Thoughts (ToT) reasoning to analyze Indian stocks like INFY, RELIANCE, or TCS using LangChain and custom tools.

## 🔍 Features

- **Multi-Step LLM Agent**: Guides reasoning with thoughts like "check earnings" or "analyze sentiment"
- **Tool-Based Execution**: Each thought maps to a Python module simulating analysis (mock or real)
- **LLM Fallback Planner**: If no tool is found, the LLM replans the next best thought
- **Modular & Extensible**: Add your own tools or connect to real APIs
- **LangChain Integration**: GPT-4 powered decision-making using ChatOpenAI

---

## 🚀 Usage

### 1. Set your OpenAI key in `framework/config.py`:
```python
OPENAI_API_KEY = "your-api-key-here"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Agent
```bash
python src/main.py
```

---

## 🧠 Thoughts Simulated
- Stock sentiment
- Quarterly earnings
- Technical indicators
- Macro conditions
- FII/DII flows
- Budget and policy impact

---

## 🧩 Project Structure

```
tot-stock-decider/
├── src/
│   ├── agents/
│   │   ├── stock_tot_agent.py
│   │   ├── tool_registry.py
│   │   ├── thought_selector.py
│   │   └── state_manager.py
│   ├── framework/
│   │   ├── config.py
│   │   ├── fallback_handler.py
│   │   └── langchain_model_wrapper.py
│   ├── thoughts/
│   │   ├── stock_sentiment.py
│   │   ├── quarterly_earnings.py
│   │   ├── technical_indicators.py
│   │   ├── macro_market.py
│   │   ├── fii_dii_flows.py
│   │   └── budget_policy_impact.py
│   └── main.py
```

---

## 🛠 Future Additions
- Real-time market data (NSE API, Screener)
- UI with dashboards
- Web search fallback
- Long-term memory via vector store

---

## 📄 License
MIT

---

Developed as a learning project on LangChain and AI agents for Indian equity analysis.


---

## 🌐 LangGraph Agent (Advanced)

This project now supports a LangGraph-based multi-step agent:
- Each node is a reasoning or execution step
- Agent dynamically replans unsupported thoughts
- Graph flow built using LangChain’s LangGraph primitives

Run via `framework/langgraph_engine.py` by calling `build_stock_graph()`.

Example:
```python
from framework.langgraph_engine import build_stock_graph
graph = build_stock_graph()
graph.invoke({"stock_symbol": "INFY", "log": []})
```
