from __future__ import annotations

import pytest

from natural_control.config import Settings
from natural_control.domain import Outcome
from natural_control.events import Event, EventBus
from natural_control.history import InMemoryTaskHistory, SensitiveFieldError
from natural_control.verification import Evidence, EvidenceSource, classify, combine

TOOL = EvidenceSource.TOOL_RESPONSE
ACCOUNT = EvidenceSource.ACCOUNT_RECORD


class TestVerification:
    def test_no_evidence_is_unknown(self) -> None:
        assert classify([]) is Outcome.UNKNOWN

    def test_queued_request_is_not_verified(self) -> None:
        assert classify([Evidence(TOOL, final=False, matches_intent=True)]) is Outcome.UNKNOWN

    def test_matching_account_record_verifies(self) -> None:
        assert classify([Evidence(ACCOUNT, final=True, matches_intent=True)]) is Outcome.VERIFIED

    def test_contradicting_record_fails(self) -> None:
        assert classify([Evidence(ACCOUNT, final=True, matches_intent=False)]) is Outcome.FAILED

    def test_conflicting_evidence_is_unknown(self) -> None:
        evidence = [
            Evidence(TOOL, final=True, matches_intent=True),
            Evidence(ACCOUNT, final=True, matches_intent=False),
        ]
        assert classify(evidence) is Outcome.UNKNOWN

    @pytest.mark.parametrize(
        ("items", "expected"),
        [
            ([Outcome.VERIFIED, Outcome.VERIFIED], Outcome.VERIFIED),
            ([Outcome.FAILED, Outcome.FAILED], Outcome.FAILED),
            ([Outcome.VERIFIED, Outcome.FAILED], Outcome.PARTIAL),
            ([Outcome.VERIFIED, Outcome.UNKNOWN], Outcome.UNKNOWN),
            ([], Outcome.UNKNOWN),
        ],
    )
    def test_combine(self, items: list[Outcome], expected: Outcome) -> None:
        assert combine(items) is expected


class TestHistory:
    def test_rejects_message_bodies_and_credentials(self) -> None:
        """NFR5: a synthetic secret must never reach history."""
        bus = EventBus()
        InMemoryTaskHistory(bus)
        with pytest.raises(SensitiveFieldError):
            bus.publish(Event("action_started", "t1", {"body": "SYNTHETIC-SECRET-123"}))

    def test_later_outcome_overrides_earlier(self) -> None:
        bus = EventBus()
        history = InMemoryTaskHistory(bus)
        bus.publish(Event("action_outcome", "t1", {"action_id": "a", "outcome": "unknown"}))
        bus.publish(Event("action_outcome", "t1", {"action_id": "a", "outcome": "verified"}))
        assert history.outcomes("t1") == {"a": Outcome.VERIFIED}


class TestSettings:
    def test_secrets_are_masked(self) -> None:
        settings = Settings.from_env({"OPENROUTER_API_KEY": "sk-or-SYNTHETIC"})
        assert "SYNTHETIC" not in repr(settings)
        assert settings.openrouter_api_key.reveal() == "sk-or-SYNTHETIC"

    def test_reports_missing_variables(self) -> None:
        assert "LIVEKIT_API_SECRET" in Settings.from_env({}).missing()

    def test_model_defaults_can_be_overridden(self) -> None:
        settings = Settings.from_env({"AGENT_MODEL": "z-ai/glm-5.3-flash"})
        assert settings.agent_model == "z-ai/glm-5.3-flash"
        assert Settings.from_env({}).agent_model == "deepseek/deepseek-v4.1-flash"
