"""Action gate: ADR 0001 and SRS S.9 P1, P2, P3, P5."""

from __future__ import annotations

import pytest
from conftest import Core, FakeMailbox, read_inbox, send_email

from natural_control.action_gate import GateBlocked, classify_tool
from natural_control.domain import ActionKind, Outcome, ProposedAction, TaskEvent, TaskState


def approve(core: Core, task_id: str, *actions: ProposedAction) -> None:
    request = core.gate.request_approval(task_id, actions)
    core.gate.approve(task_id, request.request_id)


def test_consequential_action_without_approval_is_blocked(core: Core, mailbox: FakeMailbox) -> None:
    task = core.tasks.start("email Bob")
    action = send_email("bob@example.com")
    with pytest.raises(GateBlocked):
        core.gate.execute(task.task_id, action, run=lambda: mailbox.send(action.args))
    assert mailbox.sent == []


def test_approved_action_runs_once(core: Core, mailbox: FakeMailbox) -> None:
    task = core.tasks.start("email Bob")
    action = send_email("bob@example.com")
    approve(core, task.task_id, action)

    core.gate.execute(task.task_id, action, run=lambda: mailbox.send(action.args))

    assert len(mailbox.sent) == 1
    assert task.state is TaskState.WORKING
    with pytest.raises(GateBlocked):
        core.gate.execute(task.task_id, action, run=lambda: mailbox.send(action.args))
    assert len(mailbox.sent) == 1


def test_changed_recipient_after_approval_is_not_sent(core: Core, mailbox: FakeMailbox) -> None:
    """FR9, FR.Sa.14: approval binds to exact details."""
    task = core.tasks.start("email Bob")
    approve(core, task.task_id, send_email("bob@example.com"))

    changed = send_email("eve@example.com")
    with pytest.raises(GateBlocked):
        core.gate.execute(task.task_id, changed, run=lambda: mailbox.send(changed.args))
    assert mailbox.sent == []


def test_stop_withdraws_unused_approval(core: Core, mailbox: FakeMailbox) -> None:
    """S.9 P2 and FR.Sa.15: pausing withdraws approvals; resuming needs fresh approval."""
    task = core.tasks.start("email Bob")
    action = send_email("bob@example.com")
    approve(core, task.task_id, action)

    core.tasks.handle(task.task_id, TaskEvent.STOP_REQUESTED)
    core.tasks.handle(task.task_id, TaskEvent.PAUSE_SETTLED)
    core.tasks.handle(task.task_id, TaskEvent.RESUME_REQUESTED)

    with pytest.raises(GateBlocked):
        core.gate.execute(task.task_id, action, run=lambda: mailbox.send(action.args))
    assert mailbox.sent == []
    withdrawn = [e for e in core.history.for_task(task.task_id) if e.type == "approvals_withdrawn"]
    assert withdrawn and withdrawn[0].data["count"] == 1


def test_pending_approval_is_withdrawn_on_stop(core: Core) -> None:
    task = core.tasks.start("email Bob")
    request = core.gate.request_approval(task.task_id, [send_email("bob@example.com")])
    core.tasks.handle(task.task_id, TaskEvent.STOP_REQUESTED)

    assert core.gate.pending(task.task_id) is None
    with pytest.raises(GateBlocked):
        core.gate.approve(task.task_id, request.request_id)


def test_reads_blocked_while_paused_but_reconciliation_allowed(core: Core) -> None:
    """S.9 P3."""
    task = core.tasks.start("check inbox")
    core.tasks.handle(task.task_id, TaskEvent.STOP_REQUESTED)
    core.tasks.handle(task.task_id, TaskEvent.PAUSE_SETTLED)

    with pytest.raises(GateBlocked):
        core.gate.execute(task.task_id, read_inbox(), run=lambda: "inbox")

    check = ProposedAction(
        "GMAIL_FETCH_EMAILS", {"q": "subject:Lunch"}, ActionKind.RECONCILE, "check"
    )
    result = core.gate.execute(
        task.task_id, check, run=lambda: "found", verify=lambda _: Outcome.VERIFIED
    )
    assert result.outcome is Outcome.VERIFIED


def test_failed_call_is_unknown_not_failed(core: Core) -> None:
    """FR12: an error after dispatch does not prove the action did not happen."""
    task = core.tasks.start("email Bob")
    action = send_email("bob@example.com")
    approve(core, task.task_id, action)

    def timeout() -> None:
        raise TimeoutError

    result = core.gate.execute(task.task_id, action, run=timeout)
    assert result.outcome is Outcome.UNKNOWN


def test_stop_during_in_flight_call_records_outcome_and_stays_pausing(core: Core) -> None:
    task = core.tasks.start("email Bob")
    action = send_email("bob@example.com")
    approve(core, task.task_id, action)

    def send_while_user_says_stop() -> str:
        core.tasks.handle(task.task_id, TaskEvent.STOP_REQUESTED)
        return "sent"

    result = core.gate.execute(
        task.task_id, action, run=send_while_user_says_stop, verify=lambda _: Outcome.VERIFIED
    )
    assert task.state is TaskState.PAUSING
    assert core.history.outcomes(task.task_id) == {result.action_id: Outcome.VERIFIED}


def test_batch_items_each_run_once_then_task_returns_to_working(
    core: Core, mailbox: FakeMailbox
) -> None:
    task = core.tasks.start("email two people")
    first, second = send_email("a@example.com"), send_email("b@example.com")
    approve(core, task.task_id, first, second)

    core.gate.execute(task.task_id, first, run=lambda: mailbox.send(first.args))
    assert task.state is TaskState.EXECUTING
    core.gate.execute(task.task_id, second, run=lambda: mailbox.send(second.args))
    assert core.tasks.get(task.task_id).state is TaskState.WORKING
    assert len(mailbox.sent) == 2


def test_unknown_tools_are_treated_as_consequential() -> None:
    assert classify_tool("GMAIL_FETCH_EMAILS") is ActionKind.READ
    assert classify_tool("GMAIL_SEND_EMAIL") is ActionKind.CONSEQUENTIAL
    assert classify_tool("SOME_NEW_TOOL") is ActionKind.CONSEQUENTIAL


def test_fingerprint_ignores_argument_order() -> None:
    a = ProposedAction("T", {"x": 1, "y": 2}, ActionKind.CONSEQUENTIAL, "s")
    b = ProposedAction("T", {"y": 2, "x": 1}, ActionKind.CONSEQUENTIAL, "s")
    assert a.fingerprint == b.fingerprint
