import os
from dotenv import load_dotenv
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)

@tool
def query_impact_db(sql_query: str) -> str:
    """Executes a SQL SELECT query on the program impact database.
    The database has ONE table:
    'program_pitch' (columns: id, program_name, target_tier, total_budget_usd, projected_student_reach, projected_social_value_usd)
    Write pure SQL to extract the budget, student reach, and social value."""

    print(f"[Tool Running] Executing SQL: {sql_query}")
    try:
        conn = sqlite3.connect("program_impact.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    except Exception as e:
        return f"SQL Error: {e}"
    
@tool
def read_csr_guidelines() -> str:
    """Reads the Oyu Tolgoi CSR Guidelines to find funding tiers, cost-per-child limits, and SROI requirements."""
    print("📄 [Tool Running] Reading OT CSR Guidelines...")
    try:
        with open("project_ot/ot_csr_guildelines.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: The guidelines file was not found."

@tool
def calculate_sroi_metrics(budget: float, students: int, social_value: float) -> str:
    """Calculates the Cost-Per-Child and the Social Return on Investment (SROI) percentage."""
    print(f"[Tool Running] Calculating Metrics for Budget: {budget}")
    
    try:
        b = float(budget)
        s = int(students)
        v = float(social_value)

        cost_per_child = b / s
        sroi_percentage = (v / b) * 100

        return f"Cost-Per-Child: ${cost_per_child:.2f} | SROI: {sroi_percentage:.0f}%"
    except Exception as e:
        return f"Calculation Error: {e}. Ensure inputs are numbers."
   
        
csr_tools = [query_impact_db, read_csr_guidelines, calculate_sroi_metrics]