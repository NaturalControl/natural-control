"""Outcome verification: turn evidence into verified, partial, failed, or unknown (FR.Sa.10).

A result is only verified or failed with evidence that is final and that matches or
contradicts the intended details. Anything else, including a request that was only
queued or accepted, is unknown.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from natural_control.domain import Outcome


class EvidenceSource(StrEnum):
    TOOL_RESPONSE = "tool_response"
    ACCOUNT_RECORD = "account_record"
    PAGE_CONFIRMATION = "page_confirmation"


@dataclass(frozen=True)
class Evidence:
    source: EvidenceSource
    final: bool
    """False for "queued", "accepted", or anything that does not show the end state."""
    matches_intent: bool | None
    """True if the record matches the approved details, False if it contradicts them."""


def classify(evidence: Iterable[Evidence]) -> Outcome:
    """Outcome of one action from all evidence gathered for it."""
    final = [e for e in evidence if e.final and e.matches_intent is not None]
    if any(e.matches_intent for e in final):
        if any(e.matches_intent is False for e in final):
            return Outcome.UNKNOWN  # conflicting evidence: report it, do not guess
        return Outcome.VERIFIED
    if final:
        return Outcome.FAILED
    return Outcome.UNKNOWN


def combine(outcomes: Iterable[Outcome]) -> Outcome:
    """Outcome of a task or batch from its actions' outcomes."""
    items = list(outcomes)
    if not items or Outcome.UNKNOWN in items:
        return Outcome.UNKNOWN
    if all(o is Outcome.VERIFIED for o in items):
        return Outcome.VERIFIED
    if all(o is Outcome.FAILED for o in items):
        return Outcome.FAILED
    return Outcome.PARTIAL
