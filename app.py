import streamlit as st
from assistant import client, run_and_stream_response

st.set_page_config(page_title="Market Strategy Assistant", layout="centered")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()

# --- Title ---
st.title("🧠 Market Strategy Assistant")
st.markdown("Ask anything related to marketing strategy, competition, or market analysis.")

# --- Display Message History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
prompt = st.chat_input("What would you like to ask?")

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add user message to assistant thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )

    # Spinner while streaming response
    with st.spinner("Thinking..."):
        full_response = ""
        with st.chat_message("assistant"):
            response_container = st.empty()
            for chunk in run_and_stream_response(st.session_state.thread.id):
                full_response += chunk
                response_container.markdown(full_response + "▌")

            response_container.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
