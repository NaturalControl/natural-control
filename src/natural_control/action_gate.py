"""Action gate: every tool call passes through here (ADR 0001, SRS S.9 P1, P2, P5).

- Reads and preparation run only while the task is Working or Executing.
- Consequential actions run only in Executing, with an unused approval whose
  fingerprint matches the exact details. Each approval is consumed before the call
  starts, so an approved item executes at most once.
- Reconciliation checks of earlier actions may run in any state, including Paused.
- Pausing or cancelling withdraws every pending and unused approval.

Not yet handled: the FR24 exception for rejecting non-essential cookies.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import TypeVar

from natural_control.domain import ActionKind, Outcome, ProposedAction, TaskEvent, TaskState
from natural_control.events import Event, EventBus
from natural_control.task_manager import TaskManager

T = TypeVar("T")

# Tools known to have no external effect. Anything not listed is treated as consequential,
# so a new or renamed tool fails safe. Slugs are Composio's; confirm them in spike 2.
READ_ONLY_TOOLS = frozenset(
    {
        "GMAIL_FETCH_EMAILS",
        "GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID",
        "GMAIL_LIST_THREADS",
        "GOOGLECALENDAR_EVENTS_LIST",
        "GOOGLECALENDAR_FIND_EVENT",
        "GOOGLECALENDAR_FIND_FREE_SLOTS",
    }
)

_DISPATCH_STATES = frozenset({TaskState.WORKING, TaskState.EXECUTING})
_WITHDRAW_ON = frozenset({str(TaskState.PAUSING), str(TaskState.CANCELLING)})


def classify_tool(tool: str) -> ActionKind:
    return ActionKind.READ if tool in READ_ONLY_TOOLS else ActionKind.CONSEQUENTIAL


class GateBlocked(Exception):
    """The gate refused to run an action. The action did not start."""


@dataclass(frozen=True)
class ApprovalRequest:
    task_id: str
    actions: tuple[ProposedAction, ...]
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @property
    def readback(self) -> str:
        """What the voice layer reads back before the user approves."""
        return "; ".join(action.summary for action in self.actions)


@dataclass(frozen=True)
class ExecutionResult[R]:
    action_id: str
    outcome: Outcome
    value: R | None = None


class ActionGate:
    def __init__(self, tasks: TaskManager, bus: EventBus) -> None:
        self._tasks = tasks
        self._bus = bus
        self._pending: dict[str, ApprovalRequest] = {}
        # task_id -> fingerprint -> approved item ids not yet used
        self._approved: dict[str, dict[str, list[str]]] = {}
        bus.subscribe(self._on_event)

    # ---- approval flow -------------------------------------------------------------------

    def request_approval(self, task_id: str, actions: Sequence[ProposedAction]) -> ApprovalRequest:
        if not actions:
            raise ValueError("an approval request needs at least one action")
        request = ApprovalRequest(task_id, tuple(actions))
        self._tasks.handle(task_id, TaskEvent.ACTION_PROPOSED)
        self._pending[task_id] = request
        self._bus.publish(
            Event(
                "approval_requested",
                task_id,
                {
                    "request_id": request.request_id,
                    "items": [a.action_id for a in request.actions],
                    "readback": request.readback,
                },
            )
        )
        return request

    def pending(self, task_id: str) -> ApprovalRequest | None:
        return self._pending.get(task_id)

    def approve(self, task_id: str, request_id: str) -> None:
        request = self._pending.get(task_id)
        if request is None or request.request_id != request_id:
            raise GateBlocked("no matching pending approval; it may have been withdrawn")
        del self._pending[task_id]
        ledger = self._approved.setdefault(task_id, {})
        for action in request.actions:
            ledger.setdefault(action.fingerprint, []).append(action.action_id)
        self._tasks.handle(task_id, TaskEvent.APPROVED)
        self._bus.publish(Event("approval_granted", task_id, {"request_id": request_id}))

    def decline(self, task_id: str, request_id: str) -> None:
        request = self._pending.get(task_id)
        if request is None or request.request_id != request_id:
            raise GateBlocked("no matching pending approval")
        del self._pending[task_id]
        self._tasks.handle(task_id, TaskEvent.DECLINED_OR_CHANGED)
        self._bus.publish(Event("approval_declined", task_id, {"request_id": request_id}))

    # ---- execution -----------------------------------------------------------------------

    def dispatch_open(self, task_id: str) -> bool:
        """True while the task may start new actions (Working or Executing)."""
        return self._tasks.get(task_id).state in _DISPATCH_STATES

    def check(self, task_id: str, action: ProposedAction) -> None:
        """Raise GateBlocked unless the action may start now. Does not consume anything."""
        state = self._tasks.get(task_id).state
        if action.kind is ActionKind.RECONCILE:
            return
        if action.kind in (ActionKind.READ, ActionKind.PREPARE):
            if state not in _DISPATCH_STATES:
                raise GateBlocked(f"task is {state}; new actions are blocked")
            return
        if state is not TaskState.EXECUTING:
            raise GateBlocked(f"consequential action needs approval; task is {state}")
        if not self._approved.get(task_id, {}).get(action.fingerprint):
            raise GateBlocked("no unused approval matches these exact details")

    def execute(
        self,
        task_id: str,
        action: ProposedAction,
        run: Callable[[], T],
        verify: Callable[[T], Outcome] | None = None,
    ) -> ExecutionResult[T]:
        """Run one action through the gate and record its outcome.

        If `run` raises, the outcome is UNKNOWN: the call may have reached the service.
        """
        self.check(task_id, action)
        approved_item: str | None = None
        if action.kind is ActionKind.CONSEQUENTIAL:
            approved_item = self._consume(task_id, action.fingerprint)

        self._bus.publish(
            Event(
                "action_started",
                task_id,
                {"action_id": action.action_id, "tool": action.tool, "kind": str(action.kind)},
            )
        )
        value: T | None = None
        try:
            value = run()
            outcome = verify(value) if verify else Outcome.UNKNOWN
        except Exception as exc:
            outcome = Outcome.UNKNOWN
            self._bus.publish(
                Event(
                    "action_error",
                    task_id,
                    {"action_id": action.action_id, "error": type(exc).__name__},
                )
            )
        self._bus.publish(
            Event(
                "action_outcome",
                task_id,
                {"action_id": action.action_id, "outcome": str(outcome), "summary": action.summary},
            )
        )
        if approved_item is not None:
            self._advance_after_item(task_id)
        return ExecutionResult(action.action_id, outcome, value)

    # ---- internals -----------------------------------------------------------------------

    def _consume(self, task_id: str, fingerprint: str) -> str:
        items = self._approved[task_id][fingerprint]
        item = items.pop(0)
        if not items:
            del self._approved[task_id][fingerprint]
        return item

    def _advance_after_item(self, task_id: str) -> None:
        # A stop may have arrived while the call was in flight. Then the task is no longer
        # Executing and the settled outcome is only recorded (S.9: operations settle separately).
        if self._tasks.get(task_id).state is not TaskState.EXECUTING:
            return
        remaining = any(self._approved.get(task_id, {}).values())
        event = (
            TaskEvent.ITEM_OUTCOME_RECORDED if remaining else TaskEvent.LAST_ITEM_OUTCOME_RECORDED
        )
        self._tasks.handle(task_id, event)

    def _on_event(self, event: Event) -> None:
        if event.type != "state_changed" or event.data.get("to") not in _WITHDRAW_ON:
            return
        pending = self._pending.pop(event.task_id, None)
        unused = self._approved.pop(event.task_id, {})
        withdrawn = (len(pending.actions) if pending else 0) + sum(len(v) for v in unused.values())
        if withdrawn:
            self._bus.publish(Event("approvals_withdrawn", event.task_id, {"count": withdrawn}))
