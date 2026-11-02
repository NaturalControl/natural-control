"""SRS S.9 state machine."""

from __future__ import annotations

import pytest

from natural_control.domain import FINAL_STATES, RUNNING_STATES, TaskEvent, TaskState
from natural_control.events import EventBus
from natural_control.task_manager import (
    TRANSITIONS,
    ActiveTaskExists,
    IllegalTransition,
    Task,
    TaskManager,
)

S, E = TaskState, TaskEvent


def manager_with(state: TaskState) -> tuple[TaskManager, Task]:
    tm = TaskManager(EventBus())
    task = tm.start("test")
    task.state = state
    return tm, task


@pytest.mark.parametrize(("state", "event"), sorted(TRANSITIONS, key=str))
def test_every_table_row_reaches_its_target(state: TaskState, event: TaskEvent) -> None:
    tm, task = manager_with(state)
    assert tm.handle(task.task_id, event) is TRANSITIONS[(state, event)]


def test_happy_path_with_one_approval() -> None:
    tm = TaskManager(EventBus())
    task = tm.start("email Bob")
    for event, expected in [
        (E.ACTION_PROPOSED, S.AWAITING_APPROVAL),
        (E.APPROVED, S.EXECUTING),
        (E.LAST_ITEM_OUTCOME_RECORDED, S.WORKING),
        (E.ALL_OUTCOMES_CONFIRMED, S.DONE),
    ]:
        assert tm.handle(task.task_id, event) is expected


@pytest.mark.parametrize("state", sorted(RUNNING_STATES))
def test_stop_from_any_running_state_pauses(state: TaskState) -> None:
    tm, task = manager_with(state)
    assert tm.handle(task.task_id, E.STOP_REQUESTED) is S.PAUSING


@pytest.mark.parametrize("state", sorted(FINAL_STATES))
@pytest.mark.parametrize("event", list(TaskEvent))
def test_final_states_never_move(state: TaskState, event: TaskEvent) -> None:
    """S.9 P4."""
    tm, task = manager_with(state)
    with pytest.raises(IllegalTransition):
        tm.handle(task.task_id, event)


def test_paused_task_cannot_start_work_without_resume() -> None:
    tm, task = manager_with(S.PAUSED)
    for event in (E.ACTION_PROPOSED, E.APPROVED, E.USER_CORRECTED, E.ALL_OUTCOMES_CONFIRMED):
        with pytest.raises(IllegalTransition):
            tm.handle(task.task_id, event)


def test_one_active_task_per_session() -> None:
    """S.9 P6, including Pausing and Cancelling."""
    for state in (S.WORKING, S.PAUSING, S.PAUSED, S.CANCELLING):
        tm, _ = manager_with(state)
        with pytest.raises(ActiveTaskExists):
            tm.start("second task")


def test_new_task_allowed_after_final_state() -> None:
    tm, _ = manager_with(S.DONE)
    assert tm.start("next").state is S.WORKING
