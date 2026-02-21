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
from project4_tools import all_enterprise_tools

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
).bind_tools(all_enterprise_tools, parallel_tool_calls=False)

class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]

def supervisor_node(state: MessagesState):
    print("[Supervisor] Analyzing request and delegating tasks...")

    system_instruction = SystemMessage(content="""You are a Senior Financial Architect.
    Follow these exact steps sequentially. DO NOT SKIP STEPS.
    1. Use the 'query_corporate_db' tool to find the amount for 'OPEX' in 'Q4' from the 'targets' table.
    2. Use the 'query_corporate_db' tool to find the amount for 'OPEX' in 'Q4' from the 'actuals' table.
    3. Use the 'calculate_variance' tool using the exact target and actual numbers you just found.
    4. Use the 'read_supply_chain_memo' tool to find out WHY the OPEX was high.
    5. Write a brief executive summary. DO NOT call any more tools after writing the summary.""")

    messages_to_send = [system_instruction] + state["messages"]
    response = llm.invoke(messages_to_send)
    return {"messages": [response]}

print("🏗️ Wiring the Enterprise Multi-Agent Graph...")
builder = StateGraph(MessagesState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("tools", ToolNode(all_enterprise_tools))

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", tools_condition)
builder.add_edge("tools", "supervisor")

memory = MemorySaver()
app = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    print("\n🚀 EXECUTING Q4 VARIANCE ANALYSIS...\n")
    
    # The complex prompt that requires multiple agents/tools to solve
    prompt = "I need a Q4 Operating Expense variance report. What was the target vs actual, what is the variance percentage, and why did this happen?"
    
    config = {"configurable": {"thread_id": "capstone_run_01"}}
    
    for event in app.stream({"messages": [HumanMessage(content=prompt)]}, config=config):
        pass 
    
    final_state = app.get_state(config)
    print("\n📊 --- FINAL EXECUTIVE REPORT ---")
    print(final_state.values["messages"][-1].content)
