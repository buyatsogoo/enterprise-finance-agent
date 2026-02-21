# 📊 Enterprise Finance Agent: Q4 Variance & Forecasting Engine

## Overview
This project demonstrates a production-ready, hierarchical Multi-Agent AI system designed to automate complex corporate finance-planning and forecasting. 

Rather than relying on a single, hallucination-prone LLM, this architecture utilizes **LangGraph** to deploy a Supervisor AI that manages specialized worker tools. It seamlessly merges structured ERP data with unstructured qualitative documents to synthesize executive-level variance reports.

## System Architecture

* **The Supervisor (Controller):** Receives natural language queries and dynamically routes tasks to the appropriate worker node, enforcing strict sequential execution to prevent data hallucination.
* **ERP Extractor (SQL Tool):** Executes deterministic queries against a local SQLite database containing historical Actuals and forecasted Targets.
* **Context Reader (RAG Tool):** Parses unstructured operational memos (e.g., supply chain updates) to identify the qualitative drivers behind budget variances.
* **The Quant (Math Engine):** A dedicated Python tool that strictly calculates variance percentages based *only* on the extracted database numbers.
* **Frontend:** A clean, user-friendly Streamlit chat interface.

## Observability
The system is fully integrated with **LangSmith** for enterprise LLMOps tracing, ensuring token efficiency, mathematical accuracy, and complete auditability of the AI's reasoning path.

## How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your API keys in your environment (Groq API, LangSmith API).
4. Run the database setup: `python project4_database.py`
5. Launch the UI: `streamlit run project4_app.py`