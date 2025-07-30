import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt4o_image_qa(image_path, prompt):
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
    ext = "png" if image_path.lower().endswith(".png") else "jpeg"
    image_url = f"data:image/{ext};base64,{b64}"
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ],
        max_tokens=512
    )
    return response.choices[0].message.content