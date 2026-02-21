import os
from dotenv import load_dotenv
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()

# --- 1. SETUP THE BRAIN ---
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

# --- 2. THE ERP EXTRACTOR (Custom SQL Tool) ---
@tool
def query_corporate_db(sql_query: str) -> str:
    """Executes a SQL SELECT query on the corporate database.
    The database has TWO tables:
    1. 'actuals' (columns: id, quarter, account_category, amount)
    2. 'targets' (columns: id, quarter, account_category, amount)
    Write pure SQL to extract the numbers you need."""
    
    print(f"🗄️ [Tool Running] Executing SQL: {sql_query}")
    try:
        # We use Python's built-in SQLite to execute the query safely
        conn = sqlite3.connect("corporate_finance.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    except Exception as e:
        return f"SQL Error: {e}"

# --- 3. THE CONTEXT READER ---
@tool
def read_supply_chain_memo() -> str:
    """Reads the Q4 Supply Chain Update Memo to find qualitative context about financial variances."""
    print("📄 [Tool Running] Reading the Operations Memo...")
    try:
        with open("q4_memo.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: The memo file was not found."

# --- 4. THE QUANT ---
@tool
def calculate_variance(target: float, actual: float) -> str:
    """Calculates the percentage variance between a forecasted target and an actual number."""
    print(f"🧮 [Tool Running] Calculating Variance for Target: {target}, Actual: {actual}")
    variance = (actual - target) / target
    return f"The variance is {variance * 100:.2f}%"

# --- 5. ASSEMBLE THE REGISTRY ---
all_enterprise_tools = [query_corporate_db, read_supply_chain_memo, calculate_variance]