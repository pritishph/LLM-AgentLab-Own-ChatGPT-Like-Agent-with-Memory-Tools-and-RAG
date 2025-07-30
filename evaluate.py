import json
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

load_dotenv()
rouge = Rouge()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

def evaluate(test_file):
    with open(test_file, "r") as f:
        cases = json.load(f)

    for case in cases:
        prompt = case["input"]
        expected = case["expected"]

        result = llm.predict(prompt)

        bleu = sentence_bleu([expected.split()], result.split())
        rouge_score = rouge.get_scores(result, expected)[0]["rouge-l"]["f"]

        print(f"Input: {prompt}")
        print(f"Output: {result}")
        print(f"BLEU: {bleu:.2f}, ROUGE-L: {rouge_score:.2f}\n")

evaluate("eval/test_cases.json")