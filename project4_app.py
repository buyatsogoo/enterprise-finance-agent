import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from project4_supervisor import app

load_dotenv()

st.set_page_config(page_title="Enterprise Finance Agent", page_icon="📊")
st.title("📊 Q4 Variance & Forecasting Engine")
st.markdown("This multi-agent system autonomously queries the corporate SQLite database, calculates variances, and reads internal memos to synthesize executive reports.")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., Generate a Q4 OPEX variance report and explain the context."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Agents are querying the database and reading memos..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            initial_input = {"messages": [HumanMessage(content=prompt)]}

            try:
                final_state = app.invoke(initial_input, config=config)
                final_response = final_state["messages"][-1].content
                st.markdown(final_response)

                st.session_state.messages.append({"role": "assistant", "content": final_response})
            except Exception as e:
                st.error(f"System Architecture Error: {e}")