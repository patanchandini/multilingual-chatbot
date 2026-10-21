from src.chatbot import BotConfig, Chatbot

def test_multi_request():
    bot = Chatbot(BotConfig())
    r = bot.handle("m1", "track order 12345 and cancel ORD-99887")
    assert "order_status" in r["intents"]
    assert "cancel" in r["intents"]

def test_correction_replaces_id():
    bot = Chatbot(BotConfig())
    bot.handle("c3", "status of order 11111")
    bot.handle("c3", "no, I meant 22222")
    s = bot.store.get("c3", "c3")
    last_user = [t for t in s.turns if t.role == "user"][-2]
    assert any(e.canonical == "22222" for e in last_user.entities)

def test_low_confidence_clarifies():
    bot = Chatbot(BotConfig())
    r = bot.handle("cl1", "blorptastic zibble")
    assert r["mode"] == "clarify"