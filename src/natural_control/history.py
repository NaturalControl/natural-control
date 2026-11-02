"""Task history layer: records what happened, built only from published events (FR.Sa.2).

Stores task states, approvals, action IDs and outcomes. It refuses event fields that
could carry message bodies or credentials (NFR5).
"""

from __future__ import annotations

from typing import Protocol

from natural_control.domain import Outcome
from natural_control.events import Event, EventBus

FORBIDDEN_FIELDS = frozenset(
    {"body", "content", "message", "password", "secret", "token", "api_key", "audio", "code"}
)


class SensitiveFieldError(ValueError):
    pass


class TaskHistory(Protocol):
    def for_task(self, task_id: str) -> list[Event]: ...

    def outcomes(self, task_id: str) -> dict[str, Outcome]: ...


class InMemoryTaskHistory:
    """History for one worker process. A persistent store replaces this for reconnection."""

    def __init__(self, bus: EventBus) -> None:
        self._events: list[Event] = []
        bus.subscribe(self.record)

    def record(self, event: Event) -> None:
        leaked = FORBIDDEN_FIELDS.intersection(event.data)
        if leaked:
            raise SensitiveFieldError(f"event {event.type} has sensitive fields: {sorted(leaked)}")
        self._events.append(event)

    def for_task(self, task_id: str) -> list[Event]:
        return [e for e in self._events if e.task_id == task_id]

    def outcomes(self, task_id: str) -> dict[str, Outcome]:
        """Latest recorded outcome per action. Later evidence overrides earlier (S.9 P4)."""
        result: dict[str, Outcome] = {}
        for event in self.for_task(task_id):
            if event.type == "action_outcome":
                result[event.data["action_id"]] = Outcome(event.data["outcome"])
        return result
