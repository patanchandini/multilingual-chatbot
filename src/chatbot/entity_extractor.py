import re
from typing import List
from .models import Entity

PATTERNS = {
    "order_id":     re.compile(r"\b(?:ORD|ORDER|#)?[-\s]?(\d{5,12})\b", re.I),
    "date":         re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b"),
    "product_code": re.compile(r"\b[A-Z]{2,4}-\d{3,6}\b"),
    "name":         re.compile(r"\b(?:my name is|i am|naam|nombre|पता है मेरा नाम|என் பெயர்)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)", re.I),
}

def extract_entities(text: str, lang: str) -> List[Entity]:
    ents: List[Entity] = []
    for kind, pat in PATTERNS.items():
        for m in pat.finditer(text):
            raw = m.group(0)
            ents.append(Entity(kind=kind, raw=raw, canonical=raw.strip(),
                               lang=lang, span=m.span()))
    return ents