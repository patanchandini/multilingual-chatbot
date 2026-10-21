from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from .config import BotConfig
from .context_manager import push_turn
from .correction_handler import apply_corrections
from .entity_extractor import extract_entities
from .intent_classifier import classify_intents
from .language_detector import detect_language
from .models import Session, Turn
from .request_splitter import split_requests
from .session_manager import SessionManager
from .session_store import SessionStore
from .spell_corrector import correct_tokens, tokenize

CLARIFY_LANG = "Which language would you like to use? (en / hi / ta / es)"
CLARIFY_INTENT = ("Could you tell me what you'd like to do — "
                  "check an order, cancel, refund, or something else?")


class Chatbot:
    def __init__(self, cfg: BotConfig):
        self.cfg = cfg
        self.store = SessionStore(cfg)
        self.sessions = SessionManager(self.store, cfg)

    def handle(self, customer_id, text, now=None):
        now = now or datetime.utcnow()
        lang, lang_conf, _ = detect_language(text, self.cfg)
        session, mode = self.sessions.open_or_resume(customer_id, now, lang)

        # --- language clarification gate ---
        if lang_conf < self.cfg.lang_conf_min and \
           session.pending_clarification != "language":
            session.pending_clarification = "language"
            self.sessions.touch(session, now)
            return self._clarify(session, CLARIFY_LANG, lang, [])

        if session.pending_clarification == "language":
            session.language = lang
            session.pending_clarification = None
        else:
            session.language = lang

        # --- entities FIRST (protected ledger) ---
        raw_entities = extract_entities(text, session.language)

        # --- multi-request decomposition ---
        segments = split_requests(text)
        all_intents = []
        best_conf = 0.0
        for seg in segments:
            toks = correct_tokens(tokenize(seg), session.language, self.cfg)
            ranked = classify_intents(toks, session.language, self.cfg)
            intent, conf = ranked[0]
            all_intents.append(intent)
            best_conf = max(best_conf, conf)

        # --- intent clarification gate ---
        if best_conf < self.cfg.intent_conf_min and \
           session.pending_clarification != "intent":
            session.pending_clarification = "intent"
            self.sessions.touch(session, now)
            return self._clarify(session, CLARIFY_INTENT,
                                 session.language, raw_entities,
                                 intents=all_intents)

        if session.pending_clarification == "intent":
            session.pending_clarification = None

        # --- corrections then persist ---
        apply_corrections(session, text, raw_entities)
        push_turn(session, Turn(role="user", text=text, lang=session.language,
                                intents=all_intents, entities=raw_entities,
                                ts=now), self.cfg)

        reply = self._dispatch(session, all_intents, raw_entities)
        push_turn(session, Turn(role="bot", text=reply,
                                lang=session.language, ts=now), self.cfg)

        self.sessions.touch(session, now)
        return {
            "session_id": session.session_id,
            "mode": mode,
            "language": session.language,
            "language_confidence": round(lang_conf, 2),
            "intents": all_intents,
            "intent_confidence": round(best_conf, 2),
            "entities": [{"kind": e.kind, "raw": e.raw,
                          "canonical": e.canonical} for e in raw_entities],
            "reply": reply,
            "summary": session.summary,
        }

    # ---------- internals ----------
    def _clarify(self, s: Session, msg: str, lang: str, ents,
                 intents=None) -> Dict[str, Any]:
        return {
            "session_id": s.session_id,
            "mode": "clarify",
            "language": lang,
            "intents": intents or [],
            "entities": [e.raw for e in ents],
            "reply": msg,
            "summary": s.summary,
        }

    def _dispatch(self, s: Session, intents, ents) -> str:
        ids = [e.raw for e in ents if e.kind == "order_id"]
        parts = [f"[{i}]" for i in intents]
        tail = f" for {', '.join(ids)}" if ids else ""
        return f"Handled {' + '.join(parts)}{tail}."

    # ---------- test helper ----------
    def advance_clock(self, customer_id: str, seconds: int) -> None:
        s = self.store.get(customer_id, customer_id)
        if s:
            s.last_activity -= timedelta(seconds=seconds)