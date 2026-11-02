"""Hermes adapter (placeholder until spike 1).

Hermes runs as its own process, installed with `uv tool install hermes-agent==HERMES_VERSION`.
It pins dependencies (for example openai) that conflict with Browser Use, so it does not
share our virtual environment. We talk to it over its TUI gateway JSON-RPC.

Gateway methods we expect to use, to be confirmed on the pinned version:
  - server requests `approval` and `clarify`  -> answered by our gate / voice layer
  - `session.interrupt`, `session.cancel`, `session.resume` -> our stop, cancel, resume
Hermes must call our tool executor, not its own tools or Composio's MCP server (ADR 0001).
"""

from __future__ import annotations

HERMES_VERSION = "0.19.0"


class HermesGatewayRuntime:
    """AgentRuntime backed by the Hermes TUI gateway."""

    def __init__(self, model: str, openrouter_api_key: str) -> None:
        self._model = model
        self._api_key = openrouter_api_key

    async def start(self, task_id: str, request: str) -> None:
        raise NotImplementedError("Hermes gateway connection: spike 1")

    async def send_user_turn(self, task_id: str, text: str) -> None:
        raise NotImplementedError("Hermes gateway connection: spike 1")

    async def interrupt(self, task_id: str) -> None:
        raise NotImplementedError("Hermes session.interrupt: spike 1")

    async def resume(self, task_id: str) -> None:
        raise NotImplementedError("Hermes session.resume: spike 1")

    async def cancel(self, task_id: str) -> None:
        raise NotImplementedError("Hermes session.cancel: spike 1")
