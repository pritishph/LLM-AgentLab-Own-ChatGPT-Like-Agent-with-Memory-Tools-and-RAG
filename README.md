# 🧠 LLM-AgentLab

Build your own ChatGPT-like AI Agent with memory, tools, and RAG, all running locally or through APIs. This project brings together everything you'd expect from a modern generalist AI: semantic memory, document understanding, tool use, and more.

---

## 🚀 Features

- **RAG (Retrieval-Augmented Generation)**: Ask questions over uploaded PDFs, CSVs, text, or markdown files.
- **Tools / Agents**: Built-in tools for math, code execution, web search, file reading, and PDF-based retrieval.
- **Long-Term Memory**: Stores user queries and retrieves semantically similar past inputs.
- **OpenAI & Local LLM Ready**: Works with OpenAI models (`gpt-3.5`, `gpt-4`) and easily extendable to local models.
- **FastAPI Backend**: Robust, extendable API server for model serving and agent chaining.
- **Streamlit UI**: Clean, interactive frontend to test conversations, upload files, and chat with your agent.
- **Modular Codebase**: Easy to plug in new tools, prompts, or model providers.
- **LoRA Fine-tuning Ready**: Supports QLoRA with PEFT and bitsandbytes (cloud or GPU-enabled).


---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/llm-agentlab.git
cd llm-agentlab

# Install dependencies
pip install -r requirements.txt
```

Requirements:

* Python 3.10+

* OpenAI API Key

* Optional: NVIDIA GPU if fine-tuning


---
## 🧠 Usage
🛠️ Local CLI Agent
```bash
python tool_agent.py
```

🌐 Run FastAPI Server
```bash
uvicorn main_api:app --reload --port 8000
```

🖥️ Run Streamlit Frontend

```bash
streamlit run app_ui.py
```

---

## 🧪 Fine-Tuning (Optional)
Fine-tune a small LLM (like phi-2) using QLoRA:
```bash
python finetune/qlora_finetune.py
```

⚠️ You'll need a GPU (≥ 12GB VRAM) or use Colab/RunPod for training.

---


## 📁 File Uploads
The Streamlit UI supports .pdf, .csv, .txt, and .md uploads for RAG-based Q&A. Uploaded files are chunked, embedded with sentence-transformers, and stored in FAISS.

---

## 🧠 Memory System
All messages are embedded and stored via FAISS. Future inputs retrieve similar past ones to preserve semantic context across conversations.


---

## 🤖 Tools Available

* Calculator

* Python Code Interpreter

* Web Search

* PDF/CSV/Markdown Reader

* RAG over Uploaded Documents

You can add your own in agent_tools.py.

---

## 🙌 Built With
* LangChain

* Transformers

* SentenceTransformers

* FAISS

* Streamlit

* FastAPI


















