"""Browser Use adapter (placeholder until spike 3).

Browser Use drives local Chrome inside its own agent loop. Spike 3 decides whether a
consequential click or submit can be held for approval through the action gate. Until
that is shown, the browser is read-only for V1 (ADR 0001): every browser action is
proposed as READ and anything that would submit, buy or change an account is refused.
Requires the `tools` extra: `uv sync --extra tools`.
"""

from __future__ import annotations


class BrowserUseTools:
    async def read_page(self, task_id: str, goal: str) -> str:
        raise NotImplementedError("Browser Use integration: spike 3")
