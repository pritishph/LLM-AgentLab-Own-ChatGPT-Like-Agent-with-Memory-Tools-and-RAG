from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from agent_tools import tools
import os
from fastapi import File, UploadFile, Form
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str  # this is the user query

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def needs_tools(message: str) -> bool:
    # Naive heuristic — improve later
    trigger_words = ["calculate", "web", "search", "code", "file", "upload", "read", "extract", "*", "/", "+", "-", "integrate", "solve", "open"]
    return any(word in message.lower() for word in trigger_words)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

@app.post("/chat-file")
async def chat_with_file(
    user_id: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        content = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            import fitz  # PyMuPDF
            from io import BytesIO
            pdf = fitz.open(stream=BytesIO(content), filetype="pdf")
            text = "\n".join([page.get_text() for page in pdf])
        elif filename.endswith(".csv"):
            import pandas as pd
            from io import StringIO
            df = pd.read_csv(StringIO(content.decode()))
            text = df.to_csv(index=False)
        elif filename.endswith(".md") or filename.endswith(".txt"):
            text = content.decode()
        else:
            return {"error": "Unsupported file format"}

        # Inject file content into user query
        full_input = f"The user uploaded this file content:\n{text[:2000]}...\n\nTheir question is:\n{message}"

        if needs_tools(message):
            response = agent.run(full_input)
        else:
            response = llm.predict(full_input)

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}

