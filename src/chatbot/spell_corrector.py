import re
from typing import List
from .config import BotConfig
from .language_packs import PACKS


def _edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _full_vocab(pack):
    vocab = set(pack.lexicon)
    vocab |= set(pack.translit.keys())
    vocab |= set(pack.translit.values())
    for kws in pack.intent_kw.values():
        vocab |= set(kws)
    return vocab


def correct_tokens(tokens: List[str], lang: str, cfg: BotConfig) -> List[str]:
    p = PACKS.get(lang)
    if not p:
        return tokens
    vocab = _full_vocab(p)

    out: List[str] = []
    for t in tokens:
        if not re.search(r"[^\W\d_]", t, re.UNICODE):
            out.append(t)
            continue

        if t in vocab:
            out.append(p.translit.get(t, t))
            continue

        best, best_d = t, cfg.spell_max_distance + 1
        for v in vocab:
            if abs(len(v) - len(t)) > cfg.spell_max_distance:
                continue
            d = _edit_distance(t, v)
            if d < best_d:
                best, best_d = v, d

        if best_d <= cfg.spell_max_distance:
            out.append(p.translit.get(best, best))
        else:
            out.append(t)

    return out


def tokenize(text: str) -> List[str]:
    return re.findall(r"\w+", text.lower())