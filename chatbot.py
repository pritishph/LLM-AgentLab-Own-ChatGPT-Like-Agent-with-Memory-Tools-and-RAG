import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI client
client = openai.OpenAI()

def ask_gpt(user_input):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()

# Main chat loop
def main():
    print("Welcome to LLM-AgentLab! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            reply = ask_gpt(user_input)
            print(f"Bot: {reply}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    

