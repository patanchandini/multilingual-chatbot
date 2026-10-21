from typing import List, Tuple
from .config import BotConfig
from .language_packs import PACKS

def classify_intents(tokens: List[str], lang: str, cfg: BotConfig
                     ) -> List[Tuple[str, float]]:
    p = PACKS.get(lang)
    if not p:
        return [("unknown", 0.0)]

    results: List[Tuple[str, float]] = []
    for intent, kws in p.intent_kw.items():
        hits = sum(1 for t in tokens if t in kws)
        if hits:
            conf = min(1.0, hits / max(1, len(kws)) + 0.4)
            results.append((intent, conf))

    if not results:
        return [("unknown", 0.0)]
    results.sort(key=lambda x: -x[1])
    return results[: cfg.max_requests_per_message]