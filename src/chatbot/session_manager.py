from datetime import datetime
from typing import Tuple
from .config import BotConfig
from .models import Session
from .session_store import SessionStore

class SessionManager:
    def __init__(self, store: SessionStore, cfg: BotConfig):
        self.store = store
        self.cfg = cfg

    def open_or_resume(self, customer_id, now, language):
      s = self.store.get(customer_id, customer_id)
      if s is None:
        return self._new(customer_id, language), "new"
      idle = (now - s.last_activity).total_seconds()
      if idle <= self.cfg.idle_timeout_sec:
        return s, "active"
      if idle <= self.cfg.resume_window_sec:
        s.turns = s.turns[-2:]
        s.pending_clarification = None
        self.store.put(s)
        return s, "resumed"
      return self._new(customer_id, language), "expired"

    def _new(self, customer_id: str, language: str) -> Session:
        s = Session(customer_id=customer_id, session_id=customer_id,
                    language=language)
        self.store.put(s)
        return s

    def touch(self, s: Session, now: datetime) -> None:
        s.last_activity = now
        self.store.put(s)