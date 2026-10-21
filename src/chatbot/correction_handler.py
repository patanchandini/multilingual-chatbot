import re
from typing import List
from .models import Entity, Session

CORRECTION_RE = re.compile(
    r"\b(no,?\s*i\s*meant|actually|sorry,?\s*change|i\s*meant|correction|"
    r"नहीं\s*मतलब|माफ़\s*करें|சரி\s*இல்லை|perdón|me\s*refería)\b",
    re.I,
)

def is_correction(text: str) -> bool:
    return bool(CORRECTION_RE.search(text))

def apply_corrections(s: Session, text: str, new_ents: List[Entity]) -> None:
    if not is_correction(text):
        return
    for new in new_ents:
        for turn in reversed(s.turns):
            for i, old in enumerate(turn.entities):
                if old.kind == new.kind:
                    turn.entities[i] = new
                    return