"""Task manager: the SRS S.9 task state machine.

This is the only module that changes task state. Every transition comes from the
S.9 table; anything else raises IllegalTransition.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from natural_control.domain import (
    ACTIVE_STATES,
    FINAL_STATES,
    RUNNING_STATES,
    TaskEvent,
    TaskState,
)
from natural_control.events import Event, EventBus

S = TaskState
E = TaskEvent


def _build_transitions() -> dict[tuple[TaskState, TaskEvent], TaskState]:
    table: dict[tuple[TaskState, TaskEvent], TaskState] = {
        (S.WORKING, E.DETAILS_MISSING): S.AWAITING_CLARIFICATION,
        (S.AWAITING_CLARIFICATION, E.USER_ANSWERED): S.WORKING,
        (S.WORKING, E.USER_CORRECTED): S.WORKING,
        (S.WORKING, E.ACTION_PROPOSED): S.AWAITING_APPROVAL,
        (S.AWAITING_APPROVAL, E.APPROVED): S.EXECUTING,
        (S.AWAITING_APPROVAL, E.DECLINED_OR_CHANGED): S.WORKING,
        (S.EXECUTING, E.ITEM_OUTCOME_RECORDED): S.EXECUTING,
        (S.EXECUTING, E.LAST_ITEM_OUTCOME_RECORDED): S.WORKING,
        (S.WORKING, E.ALL_OUTCOMES_CONFIRMED): S.DONE,
        (S.WORKING, E.CANNOT_CONTINUE): S.FAILED,
        (S.PAUSING, E.PAUSE_SETTLED): S.PAUSED,
        (S.PAUSED, E.STATUS_OR_RECONNECT): S.PAUSED,
        (S.PAUSED, E.STOP_REQUESTED): S.PAUSED,
        (S.PAUSED, E.RESUME_REQUESTED): S.WORKING,
        (S.CANCELLING, E.CANCEL_SETTLED): S.CANCELLED,
    }
    for state in RUNNING_STATES:
        table[(state, E.STOP_REQUESTED)] = S.PAUSING
        table[(state, E.DISCONNECTED_OR_OUTAGE)] = S.PAUSING
    for state in RUNNING_STATES | {S.PAUSING, S.PAUSED}:
        table[(state, E.CANCEL_REQUESTED)] = S.CANCELLING
    return table


TRANSITIONS = _build_transitions()


class IllegalTransition(Exception):
    def __init__(self, state: TaskState, event: TaskEvent) -> None:
        super().__init__(f"no transition from {state} on {event}")
        self.state = state
        self.event = event


class ActiveTaskExists(Exception):
    """S.9 P6: a session has at most one active task."""


@dataclass
class Task:
    request: str
    """The user's request as a short summary. No message bodies or secrets."""
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    state: TaskState = TaskState.WORKING

    @property
    def is_active(self) -> bool:
        return self.state in ACTIVE_STATES

    @property
    def is_final(self) -> bool:
        return self.state in FINAL_STATES


class TaskManager:
    """Owns the session's tasks and applies S.9 transitions."""

    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        self._tasks: dict[str, Task] = {}
        self._active_id: str | None = None

    @property
    def active(self) -> Task | None:
        if self._active_id is None:
            return None
        task = self._tasks[self._active_id]
        return task if task.is_active else None

    def get(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def start(self, request: str) -> Task:
        if self.active is not None:
            raise ActiveTaskExists(self.active.task_id)
        task = Task(request=request)
        self._tasks[task.task_id] = task
        self._active_id = task.task_id
        self._bus.publish(Event("task_started", task.task_id, {"state": str(task.state)}))
        return task

    def handle(self, task_id: str, event: TaskEvent) -> TaskState:
        task = self._tasks[task_id]
        target = TRANSITIONS.get((task.state, event))
        if target is None:
            raise IllegalTransition(task.state, event)
        previous = task.state
        task.state = target
        self._bus.publish(
            Event(
                "state_changed",
                task_id,
                {"from": str(previous), "to": str(target), "event": str(event)},
            )
        )
        return target
