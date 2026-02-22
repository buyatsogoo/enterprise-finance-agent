import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

st.set_page_config(page_title="Agentic AI Suite", page_icon="🤖", layout="wide")
st.sidebar.title("Agent Settings")
agent_choice = st.sidebar.selectbox(
    "Choose your Agentic Workflow:",
    ["Oyu Tolgoi CSR Evaluator", "Enterprise Finance Analyst"]
)

st.sidebar.divider()
st.sidebar.info(f"**Current Agent:** {agent_choice}")
st.sidebar.write("Powered by Llama-3.3-70b & LangGraph")
st.title(f"{agent_choice}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if agent_choice == "Oyu Tolgoi CSR Evaluator":
    from project_ot_supervisor import app as agent_app
    default_prompt = "Evaluate the Elephant & Piggie proposal for Tier 2."
else:
    from project4_supervisor import app as agent_app
    default_prompt = "Calculate the Q4 variance for the Logistics department."

if prompt := st.chat_input(f"Ask the {agent_choice}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        config = {"configurable": {"thread_id": f"{agent_choice}_sesssion"}}
        with st.status("Agent is analyzing request...", expanded=True) as status:
            for event in agent_app.stream({"messages": [HumanMessage(content=prompt)]}, config=config):
                for node_name, node_data in event.items():
                    if node_name == "supervisor":
                        messages = node_data.get("messages", [])
                        if messages and hasattr(messages[-1], 'tool_calls') and messages[-1].tool_calls:
                            tool_name = messages[-1].tool_calls[0]['name']
                            st.write(f"**Supervisor:** Routing task to '{tool_name}'...")
                    elif node_name == "tools":
                        messages = node_data.get("messages", [])
                        if messages:
                            tool_name = messages[-1].name
                            st.write(f"**Tool:** '{tool_name}' completed successfully.")        
            status.update(label="Analysis Complete", state="complete", expanded=False)

        final_state = agent_app.get_state(config)
        response_text = final_state.values["messages"][-1].content
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

