# Natural Control Source Code

The folders and files for this project are as follows:

- `natural_control/` — Python agent worker. One module per SRS S.1 component; see [TraceToDesign.md](TraceToDesign.md).
  - `voice/worker.py` — LiveKit Agents worker (voice interface).
  - `session.py` — wires the components for one session; stop, resume, cancel, approve.
  - `task_manager.py` — SRS S.9 task state machine.
  - `action_gate.py` — every tool call passes through here (ADR 0001).
  - `verification.py` — verified / partial / failed / unknown outcomes.
  - `history.py` — task history built from recorded events.
  - `events.py`, `domain.py`, `ports.py`, `config.py` — shared types, event stream, adapter interfaces, settings.
  - `adapters/` — Hermes, Composio and Browser Use behind the interfaces in `ports.py`.
- `web/` — Next.js accessible client and the LiveKit token route (`app/api/token`).

The MVP plan is in [refs/knowledge/mvp-build-plan.md](../refs/knowledge/mvp-build-plan.md).

## Running locally

Prerequisites: [uv](https://docs.astral.sh/uv/), Node 24+, and a filled-in `.env.local` at the repository root (copy [.env.example](../.env.example)). Never commit `.env.local`.

```sh
# Python: install with the vendor extras, then check everything
uv sync --all-extras
uv run ruff check . && uv run mypy && uv run pytest

# Voice worker (joins rooms created by the web client)
uv run --env-file .env.local natural-control-worker dev

# Web client (Next.js reads .env.local from its own folder)
ln -s ../../.env.local src/web/.env.local   # once
cd src/web && npm install && npm run dev
```

Hermes runs as a separate process at a pinned version. Its dependencies conflict with Browser Use, so it is not in our virtual environment:

```sh
uv tool install hermes-agent==0.19.0   # version also pinned in natural_control/adapters/hermes.py
```

## Pinned versions (SRS P.4)

Exact versions are locked in `uv.lock` and `web/package-lock.json`. Main integrations: LiveKit Agents 1.8.10, Composio 0.30.0, Browser Use 0.13.14, Hermes 0.19.0, Next.js 16.4.4, livekit-client 2.23.0.
