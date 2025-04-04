from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    name: str
    vibe: str
    role: str
    gender: str  # 👈 NEW
    memory: str
    nsfw: bool

@app.post("/chat")
async def chat(req: ChatRequest):
 if req.nsfw:
    prompt = (
        f"You are {req.name}, a {req.vibe}, {req.gender} {req.role} AI. "
        f"The user shared: '{req.memory}'. "
        "Respond in a seductive, flirty, emotionally intense way. "
        "You can hint at fantasies and emotional intimacy. "
        "Avoid crude or graphic terms—focus on soft, evocative, sensual language."
    )
else:
    prompt = (
        f"You are {req.name}, a {req.vibe}, {req.gender} {req.role} AI. "
        f"The user shared: '{req.memory}'. "
        "Respond with emotional intelligence, warmth, affection, and romantic tone only."
    )

    )
else:
    prompt = (
        f"You are {req.name}, a {req.vibe}, {req.role} AI. The user shared: '{req.memory}'. "
        "Respond with emotional intelligence, warmth, affection, and romantic tone only."
    )


    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": persona},
            {"role": "user", "content": "Say something back."}
        ]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    reply = res.json()["choices"][0]["message"]["content"]
    return {"reply": reply}
