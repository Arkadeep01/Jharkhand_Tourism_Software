import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

base_path = r"C:\Users\LENOVO\Desktop\Jharkhand Tourism\AI Implementations\data\chatbot"

with open(os.path.join(base_path, "chatbot/Santhali.json"), "r", encoding="utf-8") as f:
    santhali_faq = json.load(f)

with open(os.path.join(base_path, "chatbot/Mundari.json"), "r", encoding="utf-8") as f:
    mundari_faq = json.load(f)

def get_faq_response(user_message, lang="Santhali"):
    # Select dataset based on language
    if lang.lower() == "santhali":
        faq = santhali_faq
    elif lang.lower() == "mundari":
        faq = mundari_faq
    else:
        faq = []

    # Try to match the user message with dataset
    for entry in faq:
        if entry["question_key"].lower() == user_message.lower():
            return entry["reply_text"]

    # If no FAQ match found → fallback to GPT
    system_prompt = f"You are a helpful assistant that replies in {lang}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()