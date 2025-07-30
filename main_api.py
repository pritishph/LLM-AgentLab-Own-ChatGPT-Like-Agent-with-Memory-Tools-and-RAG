from fastapi import FastAPI, UploadFile, File, Form, Request
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from agent_tools import tools
from gpt4o_image import gpt4o_image_qa
from pdf_qa import (
    extract_text_from_pdfs, chunk_text, create_vector_store,
    get_top_chunks, ask_with_context
)
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=10
)

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        message = req.message.strip()
        lower = message.lower()

        # Explicit trigger words for tools
        tool_patterns = [
            "calculate", "math", "evaluate", "run python", "execute python", 
            "use the pythonexecutor", "python code", "what is the output", "web search", 
            "search", "summarize", "file", "document", "rag", "csv", "pdf"
        ]

        # Use agent/tools only if prompt *clearly* matches a tool trigger
        if any(pat in lower for pat in tool_patterns):
            response = agent.run(message)
            # If agent/tool fails, fallback to LLM
            if not response or (isinstance(response, str) and (
                response.strip() == "" or
                response.strip().lower() in ["none", "null", "no response"] or
                response.strip().startswith("NO_EXEC_RESULT")
            )):
                response = llm.predict(message)
        else:
            # Default: use LLM for all general chat, info, and non-tool questions
            response = llm.predict(message)

        if not response or response.strip().lower() in ["none", "null", "no response"]:
            response = "Sorry, I'm having trouble answering that."
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}


@app.post("/gpt4o-image-gen")
async def gpt4o_image_gen(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())
        response = gpt4o_image_qa(image_path, prompt)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.post("/doc-qa")
async def doc_qa(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        doc_folder = "uploaded_docs"
        text = extract_text_from_pdfs(doc_folder)
        chunks = chunk_text(text)
        index, chunks = create_vector_store(chunks)
        top_chunks = get_top_chunks(query, chunks, index)
        answer = ask_with_context(query, top_chunks)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

