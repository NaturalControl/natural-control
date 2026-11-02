"""Composio adapter: Gmail and Calendar through the Composio SDK, behind the action gate.

The gate wraps every call. A before-execute modifier repeats the gate check inside
Composio, so a call that skipped our wrapper would still be refused (ADR 0001).
Requires the `tools` extra: `uv sync --extra tools`.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from natural_control.action_gate import ActionGate, ExecutionResult, GateBlocked, classify_tool
from natural_control.domain import Outcome, ProposedAction


class ComposioClient:
    """ConnectedAppClient over the Composio SDK, for one Composio user."""

    def __init__(self, api_key: str, user_id: str, gate: ActionGate, task_id: str) -> None:
        from composio import Composio, before_execute  # imported lazily: optional extra

        self._composio: Any = Composio(api_key=api_key)
        self._user_id = user_id
        gate_ref, task_ref = gate, task_id

        @before_execute(toolkits=["GMAIL", "GOOGLECALENDAR"])
        def guard(tool: str, toolkit: str, params: Any) -> Any:
            # Second line of defence: the gate already consumed the approval for this call,
            # so here we only refuse when the task has stopped dispatching.
            if not gate_ref.dispatch_open(task_ref):
                raise GateBlocked(f"{tool} refused: task is not dispatching")
            return params

        self._guard = guard

    def execute(self, tool: str, args: Mapping[str, Any]) -> Mapping[str, Any]:
        response = self._composio.tools.execute(
            tool, dict(args), user_id=self._user_id, modifiers=[self._guard]
        )
        return dict(response)


def run_tool(
    gate: ActionGate,
    client: ComposioClient,
    task_id: str,
    tool: str,
    args: Mapping[str, Any],
    summary: str,
) -> ExecutionResult[Mapping[str, Any]]:
    """Propose and run one tool call through the gate.

    Every outcome is UNKNOWN until spike 2 adds verification against the account (for
    example, finding the sent message with matching recipient and subject).
    """
    action = ProposedAction(tool=tool, args=args, kind=classify_tool(tool), summary=summary)
    return gate.execute(
        task_id,
        action,
        run=lambda: client.execute(tool, args),
        verify=lambda _response: Outcome.UNKNOWN,
    )
