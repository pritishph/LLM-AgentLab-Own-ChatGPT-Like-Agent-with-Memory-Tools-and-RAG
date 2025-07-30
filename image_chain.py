from multimodal.image_tools import caption_image
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

def image_to_story(image_path: str) -> str:
    caption = caption_image(image_path)
    prompt = f"Write a short story inspired by this image description: '{caption}'"
    return llm.predict(prompt)

def image_to_tweet(image_path: str) -> str:
    caption = caption_image(image_path)
    prompt = f"Write a viral tweet about this: '{caption}'"
    return llm.predict(prompt)

def image_to_qa(image_path: str) -> str:
    caption = caption_image(image_path)
    prompt = f"Based on the image described as '{caption}', generate a question someone might ask about it."
    return llm.predict(prompt)