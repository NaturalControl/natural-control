"""Shared value types: task states and events (SRS S.9), proposed actions, outcomes."""

from __future__ import annotations

import hashlib
import json
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class TaskState(StrEnum):
    """The set Q from SRS S.9."""

    WORKING = "Working"
    AWAITING_CLARIFICATION = "AwaitingClarification"
    AWAITING_APPROVAL = "AwaitingApproval"
    EXECUTING = "Executing"
    PAUSING = "Pausing"
    PAUSED = "Paused"
    CANCELLING = "Cancelling"
    CANCELLED = "Cancelled"
    DONE = "Done"
    FAILED = "Failed"


RUNNING_STATES = frozenset(
    {
        TaskState.WORKING,
        TaskState.AWAITING_CLARIFICATION,
        TaskState.AWAITING_APPROVAL,
        TaskState.EXECUTING,
    }
)
ACTIVE_STATES = RUNNING_STATES | {TaskState.PAUSING, TaskState.PAUSED, TaskState.CANCELLING}
FINAL_STATES = frozenset({TaskState.CANCELLED, TaskState.DONE, TaskState.FAILED})


class TaskEvent(StrEnum):
    """The input alphabet Sigma from the S.9 transition table."""

    DETAILS_MISSING = "details_missing"
    USER_ANSWERED = "user_answered"
    USER_CORRECTED = "user_corrected"
    ACTION_PROPOSED = "action_proposed"
    APPROVED = "approved"
    DECLINED_OR_CHANGED = "declined_or_changed"
    ITEM_OUTCOME_RECORDED = "item_outcome_recorded"
    LAST_ITEM_OUTCOME_RECORDED = "last_item_outcome_recorded"
    ALL_OUTCOMES_CONFIRMED = "all_outcomes_confirmed"
    CANNOT_CONTINUE = "cannot_continue"
    STOP_REQUESTED = "stop_requested"
    DISCONNECTED_OR_OUTAGE = "disconnected_or_outage"
    PAUSE_SETTLED = "pause_settled"
    STATUS_OR_RECONNECT = "status_or_reconnect"
    RESUME_REQUESTED = "resume_requested"
    CANCEL_REQUESTED = "cancel_requested"
    CANCEL_SETTLED = "cancel_settled"


class ActionKind(StrEnum):
    """How the action gate treats a proposed tool call (ADR 0001)."""

    READ = "read"
    """No external effect: search, open, list."""
    PREPARE = "prepare"
    """Temporary preparation with no consequential effect, e.g. filling a draft in memory."""
    CONSEQUENTIAL = "consequential"
    """Writes and commitments: send, create, submit, purchase. Needs approval."""
    RECONCILE = "reconcile"
    """A check of an earlier action's outcome. Allowed while paused (S.9 P3)."""


class Outcome(StrEnum):
    """Recorded result of a consequential action (SRS S.1, outcome verification)."""

    VERIFIED = "verified"
    PARTIAL = "partial"
    FAILED = "failed"
    UNKNOWN = "unknown"


def _canonical(args: Mapping[str, Any]) -> str:
    return json.dumps(args, sort_keys=True, separators=(",", ":"), default=str)


@dataclass(frozen=True)
class ProposedAction:
    """A tool call proposed by the agent, before the gate lets it run."""

    tool: str
    args: Mapping[str, Any]
    kind: ActionKind
    summary: str
    """Short, payload-free description for speech and history, e.g. "send email to Bob"."""
    action_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @property
    def fingerprint(self) -> str:
        """Hash of the exact details. Any change to tool or arguments changes it (FR.Sa.14)."""
        digest = hashlib.sha256(f"{self.tool}\n{_canonical(self.args)}".encode())
        return digest.hexdigest()
