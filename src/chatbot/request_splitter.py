import re
from typing import List

SPLIT_RE = re.compile(
    r"(?:[.!?;]|\band\b|\baur\b|\bமற்றும்\b|\by\b|\bऔर\b)",
    re.I,
)

def split_requests(text: str) -> List[str]:
    parts = [s.strip() for s in SPLIT_RE.split(text) if s and s.strip()]
    return parts or [text]