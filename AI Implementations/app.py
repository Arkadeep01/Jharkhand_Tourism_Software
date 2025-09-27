
from fastapi import FastAPI
from chatbot import gpt_response, tribal_response
from db import conversations_col
from datetime import datetime

app = FastAPI()

@app.post("/chat")
def chat(user_id: str, message: str, language: str):
    if language in ["English", "Hindi"]:
        reply = gpt_response(message, language)
    elif language in ["Santhali", "Mundari"]:
        reply = tribal_response(message, language)
    else:
        reply = "Language not supported."

    conversations_col.insert_one({
        "user_id": user_id,
        "message": message,
        "reply": reply,
        "language": language,
        "timestamp": datetime.now()
    })
    return {"reply": reply}
