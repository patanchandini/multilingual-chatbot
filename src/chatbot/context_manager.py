from typing import List
from .config import BotConfig
from .models import Session, Turn

def push_turn(s: Session, turn: Turn, cfg: BotConfig) -> None:
    s.turns.append(turn)
    keep = cfg.context_max_turns * 2
    if len(s.turns) > keep:
        overflow = s.turns[: -keep]
        s.summary = summarize(s.summary, overflow, cfg)
        s.turns = s.turns[-keep:]

def summarize(prev: str, turns: List[Turn], cfg: BotConfig) -> str:
    intents = [i for t in turns for i in t.intents if i != "unknown"]
    ents = [f"{e.kind}={e.raw}" for t in turns for e in t.entities]
    merged = f"{prev} | intents: {','.join(intents)} | {','.join(ents)}"
    return merged[-cfg.summary_max_tokens:]