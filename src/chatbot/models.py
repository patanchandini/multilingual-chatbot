from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple

@dataclass
class Entity:
    kind: str
    raw: str
    canonical: str
    lang: str
    span: Tuple[int, int]

@dataclass
class Turn:
    role: str
    text: str
    lang: str
    intents: List[str] = field(default_factory=list)
    entities: List[Entity] = field(default_factory=list)
    ts: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Session:
    customer_id: str
    session_id: str
    language: str
    turns: List[Turn] = field(default_factory=list)
    summary: str = ""
    last_activity: datetime = field(default_factory=datetime.utcnow)
    pending_clarification: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
