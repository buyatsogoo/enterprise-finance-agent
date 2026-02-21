# 🤖 Multi-Agent AI Orchestration Suite

A collection of production-ready, agentic AI systems built with **LangGraph** and **Llama-3.3-70b**. This suite demonstrates how to bridge the gap between Large Language Models and deterministic enterprise data (SQL & Vector RAG).

---

## 🏗️ Core Architecture
All agents in this suite follow the **Supervisor-Worker Pattern**:
- **The Supervisor:** Routes tasks and enforces logic sequentiality.
- **The Worker Tools:** Custom Python functions for SQL extraction, RAG parsing, and mathematical computation.
- **State Management:** LangGraph for resilient, stateful conversations.

---

## 📂 Featured Agents

### 1. CSR-Impact Engine (Oyu Tolgoi Grant Evaluator)
**Goal:** Automates the vetting process for corporate social responsibility proposals against specific grant mandates.
- **Database:** `program_impact.db` (SROI & Budget metrics).
- **RAG Context:** `ot_csr_guidelines.txt` (Strategic pillars & cost limits).
- **Key Logic:** Calculates Cost-Per-Child and SROI to verify Tier 2 eligibility ($20/child threshold).
- **Run:** `python project5_supervisor.py`

### 2. Enterprise Finance Agent (Q4 Variance Engine)
**Goal:** Analyzes corporate financial performance by merging ERP data with qualitative operational memos.
- **Database:** `corporate_finance.db` (Actuals vs. Targets).
- **RAG Context:** Operational variance memos.
- **Key Logic:** Sequential extraction of SQL "Actuals" vs. "Targets" to calculate variance % without hallucination.
- **Run:** `python project4_supervisor.py`

---

## 🛠️ Technical Stack
- **Orchestration:** LangGraph / LangChain
- **Models:** Llama-3.3-70b (via Groq)
- **Database:** SQLite
- **Deployment:** Streamlit Community Cloud
- **Observability:** LangSmith (for LLM tracing and debugging)

## 🚀 Getting Started
1. Clone the repo.
2. Setup environment variables in `.env` (refer to `.env.example`).
3. Run the desired database script (`project4_database.py` or `project5_database.py`).
4. Launch the interface: `streamlit run project5_app.py`