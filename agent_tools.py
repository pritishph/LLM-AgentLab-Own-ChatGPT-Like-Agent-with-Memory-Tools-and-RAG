from langchain.tools import Tool
from langchain_openai import ChatOpenAI
import math
from langchain_tavily import TavilySearch
from rag_tool import rag_query_tool
from dotenv import load_dotenv
load_dotenv()


# 1. Simple calculator tool
def calculate(expression: str) -> str:
    try:
        safe_math = math.__dict__.copy()
        safe_math.update({'pi': math.pi, 'e': math.e})
        return str(eval(expression, {"__builtins__": None}, safe_math))
    except Exception as e:
        return f"Error: {e}"

# 2. Basic Python code executor
def run_python_code(code: str) -> str:
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return str(exec_globals.get("result", "No result variable found. Code executed."))
    except Exception as e:
        return f"Error: {e}"

tools = [
    Tool(
        name="Calculator",
        func=calculate,
        description="Useful for math problems. Input should be a valid math expression like '3 * (4 + 5)'"
    ),
    Tool(
        name="PythonExecutor",
        func=run_python_code,
        description="Executes Python code. Input MUST be valid Python code that defines and runs everything directly. Return values should be stored in a variable called 'result'"
    )
]

# Use the underlying TavilySearch tool manually
raw_tavily_tool = TavilySearch()

def tavily_wrapper(query: str) -> str:
    return raw_tavily_tool.invoke({"query": query})

# Wrap it in a standard single-input Tool
search_tool = Tool(
    name="TavilyWebSearch",
    func=tavily_wrapper,
    description="Useful for web search about current events, factual info, or recent updates."
)

tools.append(search_tool)


def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()[:3000]  # limit for token safety
    except Exception as e:
        return f"Error reading file: {e}"

tools.append(
    Tool(
        name="FileReader",
        func=read_file_content,
        description="Reads text or CSV files from disk. Input should be a full file path."
    )
)

llm_summarizer = ChatOpenAI(temperature=0)

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following:\n\n{text[:3000]}"
    return llm_summarizer.invoke(prompt)

tools.append(
    Tool(
        name="Summarizer",
        func=summarize_text,
        description="Summarizes any long text. Input should be a long text string to summarize."
    )
)


tools.append(
    Tool(
        name="PDFDocumentRetriever",
        func=rag_query_tool,
        description="Answers questions using stored PDF documents. Input is a user question."
    )
)

