"""Supervision session: wires the components for one user session and exposes the
commands the voice interface and client controls call.

Stop handling follows FR.Sa.5: block new actions immediately, acknowledge, request safe
interruption, then confirm the pause as a separate message.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from natural_control.action_gate import ActionGate
from natural_control.domain import RUNNING_STATES, Outcome, TaskEvent, TaskState
from natural_control.events import EventBus
from natural_control.history import InMemoryTaskHistory
from natural_control.ports import AgentRuntime
from natural_control.task_manager import Task, TaskManager

Say = Callable[[str], None]


@dataclass(frozen=True)
class StatusReport:
    state: TaskState
    completed: int
    failed: int
    uncertain: int

    def spoken(self) -> str:
        parts = [f"{self.completed} done"]
        if self.failed:
            parts.append(f"{self.failed} failed")
        if self.uncertain:
            parts.append(f"{self.uncertain} uncertain")
        return f"Task is {self.state}: " + ", ".join(parts) + "."


class SupervisionSession:
    def __init__(self, runtime: AgentRuntime, say: Say) -> None:
        self.bus = EventBus()
        self.history = InMemoryTaskHistory(self.bus)
        self.tasks = TaskManager(self.bus)
        self.gate = ActionGate(self.tasks, self.bus)
        self._runtime = runtime
        self._say = say

    async def start_task(self, request: str) -> Task:
        task = self.tasks.start(request)
        await self._runtime.start(task.task_id, request)
        return task

    async def stop_work(self) -> None:
        task = self.tasks.active
        if task is None:
            self._say("Nothing is running.")
            return
        if task.state is TaskState.PAUSED:
            self.tasks.handle(task.task_id, TaskEvent.STOP_REQUESTED)
            self._say("Already paused.")
            return
        if task.state not in RUNNING_STATES:
            return
        # Blocks dispatch and withdraws approvals before anything else happens (S.9 P3).
        self.tasks.handle(task.task_id, TaskEvent.STOP_REQUESTED)
        self._say("Stopping.")
        await self._pause(task)
        self._say("Paused. " + self.status(task.task_id).spoken())

    async def connection_lost(self) -> None:
        """S.9: a disconnect pauses a running task. Nothing is spoken; the user is gone."""
        task = self.tasks.active
        if task is None or task.state not in RUNNING_STATES:
            return
        self.tasks.handle(task.task_id, TaskEvent.DISCONNECTED_OR_OUTAGE)
        await self._pause(task)

    async def _pause(self, task: Task) -> None:
        await self._runtime.interrupt(task.task_id)
        self.tasks.handle(task.task_id, TaskEvent.PAUSE_SETTLED)

    async def resume(self) -> None:
        task = self.tasks.active
        if task is None or task.state is not TaskState.PAUSED:
            self._say("There is no paused task to resume.")
            return
        self.tasks.handle(task.task_id, TaskEvent.RESUME_REQUESTED)
        await self._runtime.resume(task.task_id)

    async def cancel(self) -> None:
        task = self.tasks.active
        if task is None:
            self._say("Nothing to cancel.")
            return
        self.tasks.handle(task.task_id, TaskEvent.CANCEL_REQUESTED)
        await self._runtime.cancel(task.task_id)
        self.tasks.handle(task.task_id, TaskEvent.CANCEL_SETTLED)
        self._say(
            "Cancelled. Earlier actions were not undone. " + self.status(task.task_id).spoken()
        )

    def approve_pending(self) -> bool:
        task = self.tasks.active
        request = self.gate.pending(task.task_id) if task else None
        if task is None or request is None:
            self._say("There is nothing waiting for approval.")
            return False
        self.gate.approve(task.task_id, request.request_id)
        return True

    def decline_pending(self) -> bool:
        task = self.tasks.active
        request = self.gate.pending(task.task_id) if task else None
        if task is None or request is None:
            self._say("There is nothing waiting for approval.")
            return False
        self.gate.decline(task.task_id, request.request_id)
        return True

    def status(self, task_id: str) -> StatusReport:
        outcomes = list(self.history.outcomes(task_id).values())
        return StatusReport(
            state=self.tasks.get(task_id).state,
            completed=outcomes.count(Outcome.VERIFIED),
            failed=outcomes.count(Outcome.FAILED),
            uncertain=outcomes.count(Outcome.UNKNOWN) + outcomes.count(Outcome.PARTIAL),
        )
