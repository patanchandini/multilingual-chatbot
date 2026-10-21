from src.chatbot import BotConfig
from src.chatbot.language_detector import detect_language

cfg = BotConfig()


def test_english():
    lang, conf, _ = detect_language("hello please track my order", cfg)
    assert lang == "en" and conf >= 0.5


def test_hindi():
    lang, _, _ = detect_language("\u0911\u0930\u094d\u0921\u0930 \u0915\u0940 \u0938\u094d\u0925\u093f\u0924\u093f \u0915\u094d\u092f\u093e \u0939\u0948", cfg)
    assert lang == "hi"


def test_mixed():
    lang, _, scores = detect_language("order ki stithi", cfg)
    assert lang in ("en", "hi") and max(scores.values()) > 0.4