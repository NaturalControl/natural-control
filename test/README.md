# Automated tests

The folders and files for this folder are as follows:

- `agent/` — pytest suite for the Python agent worker. Runs without network access or API keys: Hermes, Composio and Browser Use are replaced by fakes (`conftest.py`). Run with `uv run pytest` from the repository root.
  - `test_task_manager.py` — every SRS S.9 transition, illegal transitions, one active task per session.
  - `test_action_gate.py` — approval of exact details, single use, withdrawal on stop, blocking while paused, unknown outcomes.
  - `test_session.py` — stop acknowledgment then confirmation, disconnect, resume, cancel.
  - `test_verification_history_config.py` — outcome classification, no sensitive fields in history, masked secrets.

Web client unit tests live next to the code they test (`src/web/lib/*.test.ts`) and run with `npm test` in `src/web`.

CI (`.github/workflows/ci.yml`) runs both suites, Ruff, mypy, ESLint and the TypeScript compiler on every pull request. Live smoke tests against real services and manual VoiceOver checks are described in the V&V Plan.
