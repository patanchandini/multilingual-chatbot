from dataclasses import dataclass, field
from typing import List
import yaml


@dataclass
class BotConfig:
    languages: List[str] = field(default_factory=lambda: ["en", "hi", "ta", "es"])
    default_language: str = "en"

    lang_conf_min: float = 0.60
    intent_conf_min: float = 0.55
    entity_conf_min: float = 0.70

    context_max_turns: int = 10
    summary_max_tokens: int = 200

    idle_timeout_sec: int = 30 * 60
    resume_window_sec: int = 24 * 60 * 60

    max_requests_per_message: int = 5
    spell_max_distance: int = 2

    @classmethod
    def from_yaml(cls, path: str) -> "BotConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        t = data.get("thresholds", {})
        c = data.get("context", {})
        s = data.get("sessions", {})
        lim = data.get("limits", {})
        return cls(
            languages=data.get("languages", ["en", "hi", "ta", "es"]),
            default_language=data.get("default_language", "en"),
            lang_conf_min=t.get("lang_conf_min", 0.60),
            intent_conf_min=t.get("intent_conf_min", 0.55),
            entity_conf_min=t.get("entity_conf_min", 0.70),
            context_max_turns=c.get("context_max_turns", 10),
            summary_max_tokens=c.get("summary_max_tokens", 200),
            idle_timeout_sec=s.get("idle_timeout_sec", 30 * 60),
            resume_window_sec=s.get("resume_window_sec", 24 * 60 * 60),
            max_requests_per_message=lim.get("max_requests_per_message", 5),
            spell_max_distance=lim.get("spell_max_distance", 2),
        )