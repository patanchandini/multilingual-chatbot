from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.chatbot import BotConfig, Chatbot

cfg = BotConfig.from_yaml("config.yaml")
bot = Chatbot(cfg)

app = FastAPI(title="Multilingual Chatbot")


class ChatRequest(BaseModel):
    customer_id: str
    text: str


@app.post("/chat")
def chat(req: ChatRequest):
    return bot.handle(req.customer_id, req.text, now=datetime.utcnow())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/session/{customer_id}")
def get_session(customer_id: str):
    s = bot.store.get(customer_id, customer_id)
    if not s:
        raise HTTPException(404, "no session")
    return {
        "language": s.language,
        "turns": len(s.turns),
        "summary": s.summary,
        "last_activity": s.last_activity.isoformat(),
    }