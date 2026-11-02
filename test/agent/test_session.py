"""Supervision commands the voice layer and client call (FR.Sa.5, S.9 disconnect)."""

from __future__ import annotations

import asyncio

from conftest import FakeRuntime, send_email

from natural_control.domain import TaskState
from natural_control.session import SupervisionSession


def make() -> tuple[SupervisionSession, FakeRuntime, list[str]]:
    runtime, spoken = FakeRuntime(), list[str]()
    return SupervisionSession(runtime, say=spoken.append), runtime, spoken


def test_stop_acknowledges_then_confirms_separately() -> None:
    session, runtime, spoken = make()
    task = asyncio.run(session.start_task("email Bob"))

    asyncio.run(session.stop_work())

    assert task.state is TaskState.PAUSED
    assert runtime.calls == ["start", "interrupt"]
    assert spoken[0] == "Stopping."
    assert spoken[1].startswith("Paused.")


def test_stop_twice_stays_paused() -> None:
    session, _, spoken = make()
    task = asyncio.run(session.start_task("email Bob"))
    asyncio.run(session.stop_work())
    asyncio.run(session.stop_work())
    assert task.state is TaskState.PAUSED
    assert spoken[-1] == "Already paused."


def test_disconnect_pauses_and_withdraws_pending_approval() -> None:
    session, _, _ = make()
    task = asyncio.run(session.start_task("email Bob"))
    session.gate.request_approval(task.task_id, [send_email("bob@example.com")])

    asyncio.run(session.connection_lost())

    assert task.state is TaskState.PAUSED
    assert session.gate.pending(task.task_id) is None


def test_resume_then_cancel() -> None:
    session, runtime, spoken = make()
    task = asyncio.run(session.start_task("email Bob"))
    asyncio.run(session.stop_work())
    asyncio.run(session.resume())
    assert task.state is TaskState.WORKING

    asyncio.run(session.cancel())
    assert session.tasks.get(task.task_id).state is TaskState.CANCELLED
    assert runtime.calls[-1] == "cancel"
    assert "not undone" in spoken[-1]


def test_approve_and_decline_need_a_pending_request() -> None:
    session, _, spoken = make()
    assert not session.approve_pending()
    task = asyncio.run(session.start_task("email Bob"))
    session.gate.request_approval(task.task_id, [send_email("bob@example.com")])
    assert session.decline_pending()
    assert task.state is TaskState.WORKING
    assert spoken[0] == "There is nothing waiting for approval."
