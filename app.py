import streamlit as st
from pdf_qa import load_vector_store, get_top_chunks, ask_with_context

st.set_page_config(page_title="PDF Q&A with GPT")

st.title("📄 Ask Your PDFs")

user_question = st.text_input("Ask a question:")

if user_question:
    with st.spinner("Thinking..."):
        index, chunks = load_vector_store()
        top_chunks = get_top_chunks(user_question, chunks, index)
        response = ask_with_context(user_question, top_chunks)
        st.success(response)
