import streamlit as st
import requests

st.set_page_config(page_title="LLM Agent Chat")
st.title("🧠 Chat with Your AI Agent")

user_id = "user123"

# File uploader (PDF, CSV, Markdown, TXT)
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "csv", "md", "txt"])

message = st.text_input("Ask something about the file or anything else")

if message:
    with st.spinner("Thinking..."):
        if uploaded_file:
            # Read file contents as bytes
            files = {"file": (uploaded_file.name, uploaded_file.read())}
            data = {"user_id": user_id, "message": message}
            res = requests.post("http://127.0.0.1:8000/chat-file", data=data, files=files)
        else:
            res = requests.post("http://127.0.0.1:8000/chat", json={"user_id": user_id, "message": message})

        if res.status_code == 200:
            st.success(res.json().get("response", "No response"))
        else:
            st.error(f"Error: {res.text}")
