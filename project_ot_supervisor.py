import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

from project_ot_tools import csr_tools

# --- 1. SETUP THE SUPERVISOR BRAIN ---
api_key = os.environ.get("GROQ_API_KEY") 
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
).bind_tools(csr_tools, parallel_tool_calls=False)

class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]

def supervisor_node(state: MessagesState):
    print("[Supervisor] Analyzing CSR proposal metrics...")

    system_instruction = SystemMessage(content="""You are a Corporate Grant Evaluator for Oyu Tolgoi.
    
    CRITICAL RULES:
    1. You MUST use 'query_impact_db' to get the numbers. DO NOT GUESS OR MAKE UP DATA.
    2. If the SQL tool returns a result, use ONLY those numbers for the math.
    3. The budget for Elephant & Piggie should be around $45,000. If you see $1,000,000, the tool failed; re-run the query.
    
    STEPS:
    1. Query the 'program_pitch' table for Elephant & Piggie data.
    2. Pass the exact results to 'calculate_sroi_metrics'.
    3. Read the CSR guidelines.
    4. Compare the calculated Cost-Per-Child against the Tier 2 limits ($20/child) and provide the recommendation.""")

    messages_to_send = [system_instruction] + state["messages"]
    response = llm.invoke(messages_to_send)
    return {"messages": [response]}

print("Wiring the CSR Evaluation Graph...")
builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor_node)
builder.add_node("tools", ToolNode(csr_tools))

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", tools_condition)
builder.add_edge("tools", "supervisor")

memory = MemorySaver()
app = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    print("\n🚀 EXECUTING CSR PROPOSAL EVALUATION...\n")
    
    prompt = "Evaluate our Elephant & Piggie Emotional Literacy Rollout proposal for Oyu Tolgoi Tier 2 funding. Provide the SROI, cost per child, and a final viability recommendation."
    
    config = {"configurable": {"thread_id": "ot_pitch_RETRY_02"}}
    
    for event in app.stream({"messages": [HumanMessage(content=prompt)]}, config=config):
        pass 
    
    final_state = app.get_state(config)
    print("\n📊 --- PITCH VIABILITY REPORT ---")
    print(final_state.values["messages"][-1].content)