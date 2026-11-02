"""In-process event stream from the task manager and gate to history and the voice layer."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

Listener = Callable[["Event"], None]


@dataclass(frozen=True)
class Event:
    """Something that happened to a task. `data` never holds secrets or message bodies (NFR5)."""

    type: str
    task_id: str
    data: dict[str, Any] = field(default_factory=dict)
    at: datetime = field(default_factory=lambda: datetime.now(UTC))


class EventBus:
    """Synchronous publish/subscribe. Listeners run in subscription order."""

    def __init__(self) -> None:
        self._listeners: list[Listener] = []

    def subscribe(self, listener: Listener) -> None:
        self._listeners.append(listener)

    def publish(self, event: Event) -> None:
        for listener in self._listeners:
            listener(event)
