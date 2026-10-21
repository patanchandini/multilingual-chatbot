from src.chatbot import BotConfig, Chatbot

def show(res):
    print(f"[{res['mode']:<8}] lang={res['language']} "
          f"(conf={res.get('language_confidence')}) "
          f"intents={res['intents']} "
          f"entities={res['entities']}")
    print(f"          bot> {res['reply']}")
    if res.get("summary"):
        print(f"          summary> {res['summary']}")

def main():
    cfg = BotConfig.from_yaml("config.yaml")
    bot = Chatbot(cfg)

    print("=== 1. Mixed-language + multiple requests ===")
    show(bot.handle("cust-1", "Hello, order 12345 ki stithi kya hai? And cancel ORD-99887"))

    print("\n=== 2. Low-confidence language ===")
    show(bot.handle("cust-2", "blorptastic zibble"))

    print("\n=== 3. Correction ===")
    show(bot.handle("cust-3", "status of order 11111"))
    show(bot.handle("cust-3", "no, I meant 22222"))

    print("\n=== 4. Session isolation ===")
    show(bot.handle("alice", "track order 55555"))
    show(bot.handle("bob",   "cancel order 66666"))

    print("\n=== 5. 30-min expiry then resume within 24h ===")
    show(bot.handle("cust-9", "track order 77777"))
    bot.advance_clock("cust-9", 31 * 60)
    show(bot.handle("cust-9", "any update?"))

    print("\n=== 6. Beyond 24h → new session ===")
    bot.advance_clock("cust-9", 25 * 60 * 60)
    show(bot.handle("cust-9", "hello again"))

if __name__ == "__main__":
    main()