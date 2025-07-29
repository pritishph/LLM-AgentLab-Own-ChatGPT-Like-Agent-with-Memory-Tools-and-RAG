from pdf_qa import load_vector_store, get_top_chunks, ask_with_context

def rag_query_tool(query: str) -> str:
    try:
        index, chunks = load_vector_store()
        top_chunks = get_top_chunks(query, chunks, index)
        return ask_with_context(query, top_chunks)
    except Exception as e:
        return f"RAG error: {e}"