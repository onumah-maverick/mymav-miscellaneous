import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# --- Load API key ---
load_dotenv("keys.env")
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client = os.getenv("OPEN_AI_API")
assist_id = os.getenv("assistant_id")
vector_store = os.getenv("vector_store_id")

st.set_page_config(page_title="AI Assistant Demo", page_icon="🤖", layout="wide")
st.title("🤖 OpenAI Assistant Demo")

# --- Session State ---
if "assistant_id" not in st.session_state:
    # ⚠️ Replace with your pre-created assistant ID (with vector store attached)
    st.session_state.assistant_id = assist_id

if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle User Input ---
if user_input := st.chat_input("Type your message..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send user message to thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input,
    )

    # --- Prepare JSON files for Code Interpreter ---
    # scale over 20 files limit
    search = client.vector_stores.search(
        vector_store_id=vector_store,
        query=user_input,
        max_num_results=20
    )
    file_ids = [item.file_id for item in search.data]
    #print(file_ids)

    # files = client.files.list(purpose="assistants")
    # json_file_ids = [f.id for f in files.data if f.filename.lower().endswith(".json")]
    # limited_json_ids = json_file_ids[:20]

    # -- Pre-setup: Do this once, not per user input
    assistant = client.beta.assistants.update(
        assistant_id=assist_id,
        tool_resources={"code_interpreter": {"file_ids": file_ids}}
    )

    # -- Streamlit loop:
    # 1. Thread exists in session_state
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state.thread_id,
        assistant_id=assist_id,
    )

    # --- Get Assistant Reply ---
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id,
        run_id=run.id,
    )

    assistant_reply = None
    for msg in messages.data:
        if msg.role == "assistant" and msg.content:
            # Grab first text content
            for content in msg.content:
                if content.type == "text":
                    assistant_reply = content.text.value
                    break
            if assistant_reply:
                break

    # --- Display Assistant Reply ---
    if assistant_reply:
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


