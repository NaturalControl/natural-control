"""Settings from the environment. Secret values never appear in repr or logs (NFR5)."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass


class Secret:
    """Holds a credential. str() and repr() are masked; call reveal() at the point of use."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        self._value = value

    def reveal(self) -> str:
        return self._value

    def __bool__(self) -> bool:
        return bool(self._value)

    def __repr__(self) -> str:
        return "Secret('***')" if self._value else "Secret('')"

    __str__ = __repr__


@dataclass(frozen=True)
class Settings:
    livekit_url: str
    livekit_api_key: str
    livekit_api_secret: Secret
    openrouter_api_key: Secret
    composio_api_key: Secret
    composio_user_id: str
    # Model behind Hermes, via OpenRouter. GLM 5.3 Flash is the comparison (spike 4).
    agent_model: str = "deepseek/deepseek-v4.1-flash"
    # LiveKit Inference models for the voice loop. Placeholders until spike 5 measures latency.
    voice_stt: str = "deepgram/flux-general-en"
    voice_llm: str = "openai/gpt-oss-120b"
    voice_tts: str = "cartesia/sonic-3"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        e = os.environ if env is None else env
        defaults = cls.__dataclass_fields__
        return cls(
            livekit_url=e.get("LIVEKIT_URL", ""),
            livekit_api_key=e.get("LIVEKIT_API_KEY", ""),
            livekit_api_secret=Secret(e.get("LIVEKIT_API_SECRET", "")),
            openrouter_api_key=Secret(e.get("OPENROUTER_API_KEY", "")),
            composio_api_key=Secret(e.get("COMPOSIO_API_KEY", "")),
            composio_user_id=e.get("COMPOSIO_USER_ID", "natural-control-dev"),
            agent_model=e.get("AGENT_MODEL", str(defaults["agent_model"].default)),
            voice_stt=e.get("VOICE_STT", str(defaults["voice_stt"].default)),
            voice_llm=e.get("VOICE_LLM", str(defaults["voice_llm"].default)),
            voice_tts=e.get("VOICE_TTS", str(defaults["voice_tts"].default)),
        )

    def missing(self) -> list[str]:
        """Names of required variables that are empty, for a startup check."""
        required = {
            "LIVEKIT_URL": bool(self.livekit_url),
            "LIVEKIT_API_KEY": bool(self.livekit_api_key),
            "LIVEKIT_API_SECRET": bool(self.livekit_api_secret),
            "OPENROUTER_API_KEY": bool(self.openrouter_api_key),
            "COMPOSIO_API_KEY": bool(self.composio_api_key),
        }
        return [name for name, present in required.items() if not present]
