from agent_tools import tools
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os

load_dotenv()

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

print("🔧 Tool-Using Agent Ready. Type 'exit' to quit.\n")
while True:
    prompt = input("You: ")
    if prompt.strip().lower() in ("exit", "quit"):
        break
    response = agent.run(prompt)
    print("Agent:", response)



