from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import pytest

from natural_control.action_gate import ActionGate
from natural_control.domain import ActionKind, ProposedAction
from natural_control.events import EventBus
from natural_control.history import InMemoryTaskHistory
from natural_control.task_manager import TaskManager


@dataclass
class Core:
    bus: EventBus
    tasks: TaskManager
    gate: ActionGate
    history: InMemoryTaskHistory


@pytest.fixture
def core() -> Core:
    bus = EventBus()
    history = InMemoryTaskHistory(bus)
    tasks = TaskManager(bus)
    gate = ActionGate(tasks, bus)
    return Core(bus, tasks, gate, history)


@dataclass
class FakeMailbox:
    """Stands in for a Composio Gmail account. `sent` is the independent check of what happened."""

    sent: list[Mapping[str, Any]] = field(default_factory=list)

    def send(self, args: Mapping[str, Any]) -> Mapping[str, Any]:
        self.sent.append(dict(args))
        return {"successful": True, "id": f"msg-{len(self.sent)}"}


@pytest.fixture
def mailbox() -> FakeMailbox:
    return FakeMailbox()


def send_email(to: str, subject: str = "Lunch") -> ProposedAction:
    return ProposedAction(
        tool="GMAIL_SEND_EMAIL",
        args={"recipient_email": to, "subject": subject},
        kind=ActionKind.CONSEQUENTIAL,
        summary=f"send email '{subject}' to {to}",
    )


def read_inbox() -> ProposedAction:
    return ProposedAction(
        tool="GMAIL_FETCH_EMAILS",
        args={"max_results": 5},
        kind=ActionKind.READ,
        summary="read inbox",
    )


@dataclass
class FakeRuntime:
    """AgentRuntime that records calls instead of talking to Hermes."""

    calls: list[str] = field(default_factory=list)

    async def start(self, task_id: str, request: str) -> None:
        self.calls.append("start")

    async def send_user_turn(self, task_id: str, text: str) -> None:
        self.calls.append("user_turn")

    async def interrupt(self, task_id: str) -> None:
        self.calls.append("interrupt")

    async def resume(self, task_id: str) -> None:
        self.calls.append("resume")

    async def cancel(self, task_id: str) -> None:
        self.calls.append("cancel")
