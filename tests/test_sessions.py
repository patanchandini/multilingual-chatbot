from datetime import datetime, timedelta
from src.chatbot import BotConfig, Chatbot

def test_isolation():
    bot = Chatbot(BotConfig())
    r1 = bot.handle("alice", "track order 11111")
    r2 = bot.handle("bob",   "cancel order 22222")
    assert r1["session_id"] != r2["session_id"]

def test_resume_within_24h():
    bot = Chatbot(BotConfig())
    bot.handle("c1", "track order 33333")
    bot.advance_clock("c1", 31 * 60)
    r = bot.handle("c1", "any update?")
    assert r["mode"] == "resumed"

def test_expire_after_24h():
    bot = Chatbot(BotConfig())
    bot.handle("c2", "track order 44444")
    bot.advance_clock("c2", 25 * 60 * 60)
    r = bot.handle("c2", "hello")
    assert r["mode"] == "expired"