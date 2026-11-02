# Traceability between code files and design modules

Explicitly identify what code provides the interfaces and services documented in the design

The MG and MIS do not define modules yet. Until they do, this table maps the SRS S.1 components to code. Update it when the MG assigns module names.

| SRS S.1 component | Code | Status |
|---|---|---|
| Accessible client | `src/web/app/session-controls.tsx`, `src/web/lib/controls.ts` | Connect, keyboard stop, status regions |
| Voice interface | `src/natural_control/voice/worker.py`, `src/web/app/api/token/route.ts`, `src/web/lib/token.ts` | Skeleton; not yet run against LiveKit |
| Task manager | `src/natural_control/task_manager.py`, `src/natural_control/session.py` | S.9 table implemented and tested |
| AI agent (Hermes) | `src/natural_control/adapters/hermes.py`, `src/natural_control/ports.py` (`AgentRuntime`) | Placeholder until spike 1 |
| Action gate | `src/natural_control/action_gate.py` | Implemented and tested with fakes |
| Outcome verification | `src/natural_control/verification.py` | Classification rules; account checks pending |
| Action tools and integrations | `src/natural_control/adapters/composio_tools.py`, `src/natural_control/adapters/browser.py` | Composio wiring untested live; browser placeholder |
| Task history layer | `src/natural_control/history.py`, `src/natural_control/events.py` | In-memory; persistence pending |
| Shared types and settings | `src/natural_control/domain.py`, `src/natural_control/config.py` | |
