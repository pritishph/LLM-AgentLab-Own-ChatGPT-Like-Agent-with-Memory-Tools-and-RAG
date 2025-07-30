import os
import fitz  # PyMuPDF
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import openai
import pickle

# Load environment variables (for API key)
load_dotenv()

# Set up OpenAI client (new API format)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Load PDFs from folder
def extract_text_from_pdfs(folder_path):
    full_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            doc = fitz.open(path)
            for page in doc:
                page_text = page.get_text()
                print(f"Text from page in {filename}: {repr(page_text[:200])}")
                full_text += page_text
    return full_text

# 2. Chunk text into pieces
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# 3. Embed chunks and create vector store
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_store(chunks, index_path="index.faiss", chunks_path="chunks.pkl"):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    faiss.write_index(index, index_path)
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)

    return index, chunks

def load_vector_store(index_path="index.faiss", chunks_path="chunks.pkl"):
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

# 4. Get top-k matching chunks for a query
def get_top_chunks(query, chunks, index, k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    return [chunks[i] for i in I[0]]

# 5. Ask OpenAI with context using new SDK
def ask_with_context(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question below using ONLY the provided context. Be concise and accurate.

Context:
{context}

Question: {question}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# 6. Run the interactive CLI
if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing PDFs: ").strip()

    if os.path.exists("index.faiss") and os.path.exists("chunks.pkl"):
        print("Loading existing vector store...")
        index, chunks = load_vector_store()
    else:
        print("Building new vector store...")
        text = extract_text_from_pdfs(folder_path)
        chunks = chunk_text(text)
        index, chunks = create_vector_store(chunks)


    print("PDFs loaded and indexed. Ask questions below.\nType 'exit' to quit.")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            top_chunks = get_top_chunks(question, chunks, index)
            answer = ask_with_context(question, top_chunks)
            print("AI:", answer + "\n")
        except Exception as e:
            print(f"Error: {e}")


