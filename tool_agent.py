import os
from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from agent_tools import tools
from memory.memory_store import store_user_message, get_user_memory

# Load environment variables
load_dotenv()

# LLM setup
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # or "gpt-4o" if you have access
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt with required input variables
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who can use tools to solve problems."),
    ("user", "{input}"),
    ("ai", "{agent_scratchpad}")
])

# Build agent
agent = create_openai_functions_agent(llm, tools, prompt)


#agent = initialize_agent(
#    tools=tools,
#    llm=llm,
#    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#    verbose=True,
#    max_iterations=10  # default is 3
#)
#
#print("🔧 Tool-Using Agent Ready. Type 'exit' to quit.\n")

# Agent executor with better config
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=False,
    handle_parsing_errors=True,
    output_key="output"  # required to support `.invoke()`
)

print("🔧 Tool-Using Agent Ready. Type 'exit' to quit.\n")

# Simulated user ID (replace with real auth/user system if needed)
user_id = "user123"

# REPL loop
while True:
    query = input("You: ").strip()
    if query.lower() in ["exit", "quit"]:
        break

    # Retrieve semantic memory
    memory_chunks = get_user_memory(user_id, query)
    context = "\n".join(memory_chunks) if memory_chunks else ""

    # Combine memory context with new input
    full_prompt = f"{context}\n\n{query}" if context else query

    # Run agent
    try:
        response = agent_executor.invoke({"input": full_prompt})
        print("AI:", response["output"])
    except Exception as e:
        print("Error:", str(e))

    # Save message to user memory
    store_user_message(user_id, query)



