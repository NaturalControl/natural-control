"""Interfaces the core depends on. Vendors live behind these, in natural_control.adapters.

Tests supply fakes; swapping Hermes, Composio or Browser Use changes one adapter.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class AgentRuntime(Protocol):
    """The planning agent (Hermes). It proposes tool calls; it never runs tools directly."""

    async def start(self, task_id: str, request: str) -> None: ...

    async def send_user_turn(self, task_id: str, text: str) -> None:
        """A correction or a clarification answer."""
        ...

    async def interrupt(self, task_id: str) -> None:
        """Request safe interruption of in-flight work. May return before work settles."""
        ...

    async def resume(self, task_id: str) -> None: ...

    async def cancel(self, task_id: str) -> None: ...


class ConnectedAppClient(Protocol):
    """Runs one connected-app tool call (Composio). Only the action gate calls this."""

    def execute(self, tool: str, args: Mapping[str, Any]) -> Mapping[str, Any]: ...
