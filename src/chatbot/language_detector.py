import re
from typing import Dict, Tuple
from .config import BotConfig
from .language_packs import PACKS


def _script_ratio(text: str, pattern) -> float:
    if pattern is None or not text:
        return 0.0
    hits = len(pattern.findall(text))
    return hits / max(1, len(text))


def detect_language(text: str, cfg: BotConfig) -> Tuple[str, float, Dict[str, float]]:
    tokens = re.findall(r"\w+", text.lower())
    scores: Dict[str, float] = {}

    for code in cfg.languages:
        p = PACKS[code]
        lex_hits = sum(1 for t in tokens if t in p.lexicon)
        translit_hits = sum(1 for t in tokens if t in p.translit)
        script_ratio = _script_ratio(text, p.script_re)

        score = lex_hits * 4 + translit_hits * 3 + script_ratio * 4

        # Strong prior for the default language. This keeps short English
        # messages from being flagged as low-confidence.
        if code == cfg.default_language:
            score += 3.0

        # Penalize languages whose script does not appear at all.
        if p.script_re and script_ratio == 0.0 and code != cfg.default_language:
            score *= 0.1

        scores[code] = score

    total = sum(scores.values()) or 1.0
    norm = {k: v / total for k, v in scores.items()}
    best = max(norm, key=lambda k: norm[k]) if norm else cfg.default_language
    return best, norm.get(best, 0.0), norm