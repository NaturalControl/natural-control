# MVP build plan

Status: proposal by Aaron with AI assistance, November 2, 2026. Not team-ratified. Dates come from SRS P.3/P.4 and the Development Plan; the plan below is how we propose to meet them.

## What the MVP has to prove

The POC demonstration (November 23 to December 3) shows that a user can supervise a running general-purpose agent by voice. One short task from each class:

1. **Email/calendar:** prepare a reply or calendar event from synthetic data in a test account, clarify an ambiguous detail, get approval of exact details, then send or create it.
2. **Unfamiliar website:** find and compare information with general browser tools, report a choice, and take a correction.

Across the two tasks we must exercise at least once: clarification, consequential-action approval, progress updates, correction, and an explicit work stop during a tool operation (Development Plan, POC section). Disconnect/reconnect is evaluated later, before participant sessions.

## Architecture

```
Browser client (Next.js on Vercel, /api/token)
   │  WebRTC audio + data messages
LiveKit Cloud room ── LiveKit Inference (STT, voice LLM, TTS)
   │
Python agent worker (runs on a dev Mac, uv)
   ├─ voice interface      LiveKit AgentSession; turns speech into task commands
   ├─ task manager         S.9 state machine; one active task per session
   ├─ action gate          every tool call goes through it (ADR 0001)
   ├─ outcome verification verified / partial / failed / unknown
   ├─ task history         records states, approvals, action IDs, outcomes
   └─ adapters
        ├─ Hermes          TUI gateway JSON-RPC (plans, proposes tool calls)
        ├─ Composio SDK    Gmail + Calendar, before/after-execute hooks
        └─ Browser Use     local Chrome
                │
             OpenRouter    model behind Hermes (DeepSeek V4.1 Flash default, GLM 5.3 Flash comparison)
```

Code layout (template paths preserved):

| Path | Contents |
|---|---|
| `src/natural_control/` | Python package for the agent worker, one module per SRS S.1 component |
| `src/web/` | Next.js accessible client and LiveKit token route |
| `test/agent/` | pytest suite for the Python package (no network, no keys) |
| `src/web/**/*.test.ts` | Vitest tests next to the web code |
| `src/TraceToDesign.md` | module to file map, kept in sync with the MG/MIS |

Design rules the code must keep:

- **Adapters hide vendors.** Hermes, Composio and Browser Use sit behind small interfaces (`ports.py`), so tests use fakes and a vendor swap touches one file.
- **The gate is not optional.** Tools reach the outside world only through `ActionGate.execute`. Direct Composio MCP from Hermes is not allowed.
- **The state machine is the only place task state changes.** Transitions follow the S.9 table exactly; illegal transitions raise.
- **Approvals bind to exact details.** An approval is a fingerprint of the tool name and arguments, used at most once, withdrawn on pause/cancel/disconnect.
- **No secrets or raw audio in logs or history (NFR5).** History stores action summaries and IDs, not message bodies.

## Workstreams and owners

Owners and cross-reviewers come from the Development Plan.

| Workstream | Owner / reviewer | MVP scope |
|---|---|---|
| Voice and accessible client | Lucas / Curtis | Token route, connect/disconnect, keyboard stop control (FR.Sa.1), live status region, LiveKit worker turn handling, speech interruption vs work stop |
| Agent and tool integration | Aaron / Kevin | Hermes adapter, Composio adapter with gate hooks, Browser Use adapter (or read-only fallback), task manager, action gate |
| Deployment and reliability | Kevin / Aaron | CI, env/secret handling, Vercel project, pinned versions, event logging without payloads, reconnect notes |
| Evaluation and quality | Curtis / Lucas | Demo script and seeded test data, test accounts, V&V traceability, timing measurements for STOP_ACK_TIME |

## Milestones

| By | Deliverable | Done when |
|---|---|---|
| **Nov 2** (P.4) | Component skeleton and CI | Placeholder module per S.1 component, versions pinned in `uv.lock` / `package-lock.json`, CI runs lint, types and tests on every PR, secrets gitignored. *This branch.* |
| **Nov 9** | Integration spikes | Each risk below has a yes/no answer with a short note in `refs/knowledge/`. |
| **Nov 16** (P.4) | Integrations | Voice ↔ task manager wired; Hermes on a pinned version; gate in front of Composio; Browser Use behind the gate or read-only; state machine complete. |
| **Nov 20** | Demo dry run | Both demo tasks run end to end on test accounts; stop during a tool call works; timings recorded. |
| **Nov 23 to Dec 3** | POC demonstration | Live demo, with logs correlating task, action, approval, cancellation and connection events. |

## Spikes to run first (by November 9)

These decide whether the design holds. Each needs evidence, not a guess.

1. **Hermes supervision.** Through the TUI gateway: do we get streamed status, `approval` and `clarify` requests, and does `session.interrupt` stop work? Can we make Hermes call our tool executor instead of its own tools? If not, revisit the harness (Development Plan risk table).
2. **Composio gate hooks.** Confirm `before_execute` can block a call and `after_execute` sees the result, for Gmail send and Calendar create, with managed auth on a test account.
3. **Browser Use interception.** Can a consequential click or form submit be held for approval? If not, browser stays read-only for V1 (ADR 0001).
4. **Model choice.** Run about ten Gmail/Calendar tasks with an approval step on DeepSeek V4.1 Flash and GLM 5.3 Flash via OpenRouter, pinned to fp8-or-better providers. Record tool-call errors, wrong arguments and latency.
5. **Voice latency.** Measure stop acknowledgment and response time with LiveKit Inference to give STOP_ACK_TIME and RESPONSE_TIME provisional values.

## Infrastructure and keys

All keys live in gitignored `.env.local` (template: `.env.example`). Nothing is pasted into chat, Discord or issues.

| Service | Variable | Status |
|---|---|---|
| LiveKit Cloud (project `natural-control`) | `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` | Project created; new key pair needed (old secret lost; revoke the old key in the dashboard) |
| OpenRouter | `OPENROUTER_API_KEY` | To create, with a spend limit |
| Composio | `COMPOSIO_API_KEY`, `COMPOSIO_USER_ID` | To create; connect a test Gmail account, not a personal inbox |
| Vercel | none in env; CLI login | Project created when the web client deploys; copy the LiveKit variables into it |
| Browser Use Cloud | `BROWSER_USE_API_KEY` | Optional, not used for V1 |

Google Cloud is not needed while Composio managed auth covers Gmail and Calendar. Our own OAuth app becomes a question before participant sessions.

Budget (Development Plan): \$120 for model and voice APIs. Set spend limits on every provider.

## Testing approach

Three levels, matching the V&V Plan:

1. **CI, no keys:** task manager, gate, verification and history tested with fake adapters and a controlled clock. Most functional requirements are tested here.
2. **Live smoke, manual trigger:** a few real tasks through LiveKit, Hermes, Composio and Browser Use on test accounts.
3. **Manual / participant:** VoiceOver and keyboard checks, real-speech timing, usability sessions.

Every consequential action is checked against the test account itself, not against the agent's claim.

## Out of scope for the MVP

Native Mac app control, local files, telephony, saved workflows, multi-user hosting, our own Google OAuth app, and participant sessions (those follow the POC).

## Open decisions

- Model: Aaron prefers OpenRouter with DeepSeek V4.1 Flash as default and GLM 5.3 Flash as the comparison (November 2). SRS P.5 still names Claude Sonnet as a candidate and needs updating once the spike settles it.
- Disconnect: the Development Plan allows authorized background continuation; S.9 pauses on every disconnect. Reconcile before the reconnect work.
- Stop key scope: what the keyboard stop does when another app or tab has focus (FR.Sa.1).
- TBD constants: STOP_ACK_TIME (provisionally 2 s), RESPONSE_TIME, CONNECTION_NOTICE_TIME, IDLE_PROMPT_TIME, TARGET_COMPLETION.
