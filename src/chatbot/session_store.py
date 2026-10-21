import threading
from datetime import datetime
from typing import Dict, Optional, Tuple
from .config import BotConfig
from .models import Session

class SessionStore:
    """Thread-safe. One Session per (customer_id, session_id)."""

    def __init__(self, cfg: BotConfig):
        self.cfg = cfg
        self._sessions: Dict[Tuple[str, str], Session] = {}
        self._lock = threading.RLock()

    def get(self, customer_id: str, session_id: str) -> Optional[Session]:
        with self._lock:
            return self._sessions.get((customer_id, session_id))

    def put(self, s: Session) -> None:
        with self._lock:
            self._sessions[(s.customer_id, s.session_id)] = s

    def sweep(self, now: datetime) -> None:
        with self._lock:
            for k, s in list(self._sessions.items()):
                if (now - s.last_activity).total_seconds() > self.cfg.resume_window_sec:
                    del self._sessions[k]