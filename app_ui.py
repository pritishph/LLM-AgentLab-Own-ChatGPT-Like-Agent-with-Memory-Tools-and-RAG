import streamlit as st
import requests
import os

st.set_page_config(page_title="LLM AgentLab")
st.title("🧠 LLM-AgentLab")

def clear_folder(folder):
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

st.markdown("## 💬 Chat With Agent")

user_id = "user123"
chat_input = st.text_input("Chat: (Ask anything)")

if chat_input:
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://127.0.0.1:8000/chat", json={"user_id": user_id, "message": chat_input})
            if res.status_code == 200:
                chat_resp = res.json().get("response", "")
                if not chat_resp or chat_resp.strip().lower() in ["none", "null", "no response"]:
                    chat_resp = "Sorry, I didn't get that. How can I help?"
                st.success(chat_resp)
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

st.markdown("---")
st.markdown("## 🖼️ Multimodal: Image Q&A with GPT-4o")

uploaded_file = st.file_uploader(
    "Upload an image (JPG/JPEG/PNG, <20MB)", 
    type=["jpg", "jpeg", "png"]
)
image_prompt = st.text_input(
    "Ask anything about this image (e.g. 'Write a poem about it', 'Describe the mood', 'What might happen next?'):",
    key="img_prompt"
)

if uploaded_file and image_prompt:
    st.image(uploaded_file, caption="Uploaded image", use_container_width=True)
    if st.button("Ask GPT-4o"):
        with st.spinner("GPT-4o is thinking..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"prompt": image_prompt}
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/gpt4o-image-gen",
                    files=files,
                    data=data,
                    timeout=180
                )
                if res.status_code == 200:
                    result = res.json()
                    st.markdown(f"**💡 GPT-4o Response:** {result.get('response', '')}")
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

st.markdown("---")
st.markdown("## 📄 Document Q&A (PDF, TXT, CSV, Markdown)")

doc_folder = "uploaded_docs"
os.makedirs(doc_folder, exist_ok=True)

doc_files = st.file_uploader("Upload your documents", accept_multiple_files=True, type=["pdf", "txt", "csv", "md"], key="docs")

if doc_files:
    clear_folder(doc_folder)
    for fname in ["index.faiss", "chunks.pkl"]:
        if os.path.exists(fname):
            os.remove(fname)
    for file in doc_files:
        filepath = os.path.join(doc_folder, file.name)
        with open(filepath, "wb") as f:
            f.write(file.read())
    st.success("Documents uploaded successfully.")

query = st.text_input("Ask a question based on your uploaded documents:", key="doc_prompt")

if query:
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://127.0.0.1:8000/doc-qa", json={"query": query})
            if res.status_code == 200:
                st.markdown(f"**Answer:** {res.json().get('answer', '')}")
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
