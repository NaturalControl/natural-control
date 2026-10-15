# Hazard Analysis: working draft answers

Status: **draft for team review, not the submitted document.** Due October 19 with the SRS. These are high-level answers from Aaron's planning session (October 14) for the team to read, challenge, and cut before splitting the writing. Final text goes into `docs/HazardAnalysis/HazardAnalysis.tex`. Terms follow [GLOSSARY.md](../../GLOSSARY.md).

Format follows the AlgoCatan (Team 8) hazard analysis our TA co-wrote: hazard IDs `H<component>-<letter>`, functional safety requirements `FR.Sa.N`, non-functional `NFR.Sa.N`, and a roadmap split into planned and delayed requirements. The TA recommended finishing this before the SRS so the safety requirements feed into it.

## Decisions made in this session

| Topic | Decision |
|---|---|
| Scope | Current scope only: browser tasks and connected-account tools (Gmail, Google Calendar). No rows for deferred features. |
| Losses | Unwanted action; missed or failed task; loss of control or awareness; disclosure or misuse of private information or accounts. |
| Hazard definition | AlgoCatan/Leveson wording (see Glossary). |
| Components | Seven: the simplified diagram, with LiveKit and the voice agent merged into one "Voice interface". |
| Approval rule | Every consequential action (any external write) needs approval. |
| Web writes | Browser Use may perform consequential actions, gated by approval. Intercepting them inside Browser Use is a POC risk; if it can't be shown, the browser becomes read-only for the initial release. |
| FMEA columns | Component, failure mode, effects, causes, recommended action (including how the failure is detected without sight), SR, ref. No separate detection column. |
| Outages | One row under the Hermes agent. |

## 1. Introduction

**Background.** Natural Control is a voice interface that lets blind users delegate tasks in a web browser and in connected accounts (Gmail, Google Calendar) to an AI agent. The user stays informed through spoken progress and results, and stays in control through clarification, approval, correction, and stopping.

**Hazard definition.** A hazard is a property or condition of the system, together with a condition in its environment, that can lead to a loss. Physical harm is not expected. For this project, harm means the losses listed in section 2.

## 2. Scope and purpose

We analyze hazards so that safeguards become requirements before implementation, rather than fixes after a failure.

**Included:** voice interaction, task execution through the Hermes agent, browser tasks through Browser Use, and Gmail/Calendar actions, on a Mac in English, alongside VoiceOver.

**Excluded:** native Mac application control, general local-file tasks, phone calling, and saved workflows. These are deferred, and each would add hazards (for example, broader computer access) to be analyzed if they are built.

**Losses:**
1. **Unwanted action:** something sent, submitted, purchased, created, or deleted that the user did not intend, including duplicates.
2. **Missed or failed task:** a task not done while the user believes it was.
3. **Loss of control or awareness:** the user cannot tell what the agent is doing, cannot stop it, or is told something false.
4. **Privacy or account misuse:** private information exposed, or account access used beyond what the user intended.

**Why this matters more for our users:** a sighted user can glance at the screen to catch a mistake. A blind user often cannot, so detection has to be built into the system, not left to the user.

## 3. System boundaries and components

In: the user's voice and keyboard input. Out: consequential actions on accounts and websites, and spoken feedback. No visual output is relied on.

| # | Component | Built or reused | Role |
|---|---|---|---|
| 1 | Accessible client | Built | Mic, stop key, task history; runs alongside VoiceOver |
| 2 | Voice interface | LiveKit (reused) plus our voice agent (built) | Hears, transcribes, interprets intent, speaks responses |
| 3 | Task bridge | Built | Starts, tracks, stops, and resumes tasks in Hermes; keeps the task log |
| 4 | Hermes agent | Reused | Plans the task and calls tools, using an external AI model |
| 5 | Action gate | Built | Holds consequential actions for approval; verifies outcomes |
| 6 | Browser Use | Reused | Reads and acts on websites |
| 7 | Account tools | Built or adapted MCP server | Gmail and Calendar access through OAuth |

External dependencies: websites, Google services, LiveKit, AI and speech providers, network access, VoiceOver.

**Diagram:** reuse the simplified component diagram (to be redrawn for the document).

## 4. Critical assumptions

- **Setup done correctly.** A setup helper completed the assisted setup: accounts connected and permissions granted. Setup errors are not analyzed as runtime hazards.
- **One authorized speaker.** Only the user gives commands; other voices are noise. We do not verify who is speaking.
- **User's own accounts.** Connected accounts belong to the user, who may act on them. Development and evaluation use test accounts.

We do **not** assume that speech recognition, the AI model, websites, or external services work correctly. Their failures appear in the FMEA.

## 5. FMEA

| Ref | Component | Failure mode | Effects | Causes | Recommended action | SR |
|---|---|---|---|---|---|---|
| H1-a | Accessible client | Stop control can't be reached without voice | User can't halt the agent if voice fails; loss of control | Shortcut clashes with VoiceOver; focus in another app; client frozen | Provide a stop shortcut that works whenever the client runs and doesn't clash with VoiceOver; test with VoiceOver on | FR.Sa.1 |
| H1-b | Accessible client | Task history doesn't match what happened | User can't review or catch wrong actions afterward | History written from the agent's claims instead of recorded events; events lost during disconnects | Build history only from recorded actions and verified outcomes; label anything unverified | FR.Sa.2 |
| H2-a | Voice interface | Misunderstands the user: wrong words, names, numbers, a cut-off sentence, or another voice | Wrong task or wrong details acted on | Background noise, accents, turn detection ending too early, TV or other people | Noise cancellation; read back key details (recipient, time, content summary) before every consequential action; allow spoken correction | FR.Sa.3 |
| H2-b | Voice interface | A stop request isn't recognized | Task keeps running; loss of control | Stop classified as chatter; mistranscription; user talking over the system | Recognize stop phrases with a fixed rule before any model interprets them; keyboard stop as backup; acknowledge quickly | FR.Sa.4, NFR.Sa.1 |
| H3-a | Task bridge | Stop is acknowledged but execution continues | Actions happen after the user said stop; false sense of safety | Hermes interrupts only at tool boundaries; an action is already in progress | Say "stopping" and "stopped" as separate messages; once a stop is requested, the gate refuses all further consequential actions for that task; report anything completed after the request | FR.Sa.5 |
| H3-b | Task bridge | A consequential action is repeated after reconnecting | Duplicate email or event | Automatic retry after a dropped connection when the first attempt actually succeeded | Unique ID per approved action; never retry a consequential action automatically; pause new actions while disconnected; on reconnect, report pending items | FR.Sa.6, FR.Sa.7, NFR.Sa.2 |
| H3-c | Task bridge | Task state or pending approvals lost | User never asked, or told the wrong status | Crash or restart of the bridge or Hermes | Save task state and pending approvals; after a restart, announce interrupted tasks and their last known status | FR.Sa.8 |
| H4-a | Hermes agent | Does the wrong task or picks the wrong target | Wrong action prepared (wrong thread, wrong date) | Ambiguous request; model error | Ask a clarifying question when required details are missing or ambiguous; the approval read-back (H2-a) catches the rest | FR.Sa.9 |
| H4-b | Hermes agent | Claims success that didn't happen | Missed task; user misinformed | Model hallucination; partial failure reported as success | Report completion only from verified outcomes; distinguish verified, partial, and unverified results | FR.Sa.10 |
| H4-c | Hermes agent | Stalls or loops | Silence or repeated steps; user unsure what's happening; cost grows | Model loop; slow or broken website | Speak a status update at a regular interval while a task runs; after a step or time limit, pause and ask the user | FR.Sa.11, NFR.Sa.3 |
| H4-d | Hermes agent | AI provider outage or timeout | Task halts partway | Provider down; network loss | Pause, tell the user what was and wasn't done, never claim success | FR.Sa.12 |
| H5-a | Action gate | A consequential action slips through without approval | Unwanted action | Action not recognized as consequential (e.g. a browser click that submits a form); new tool not classified | Default-deny: anything not known to be read-only requires approval; if browser writes can't be intercepted reliably, make the browser read-only | FR.Sa.13 |
| H5-b | Action gate | A stale approval is reused | Action runs with details the user never approved | Details changed after approval (time, recipient) | Bind each approval to its exact details; approvals are single-use; any change requires new approval | FR.Sa.14 |
| H5-c | Action gate | An approval request expires or is withdrawn without a clear result | User unsure whether the action happened | Timeout; disconnect; request superseded | Tell the user explicitly that the action did not happen and what is still pending | FR.Sa.15 |
| H6-a | Browser Use | Acts on the wrong page element | Wrong item chosen or wrong field filled | Poor labels; unusual layout; page changed after reading | Re-check the target against the approved details immediately before acting; verify the result afterward | FR.Sa.10, FR.Sa.14 |
| H6-b | Browser Use | Follows instructions injected by a webpage | Unwanted action or private data sent elsewhere | Page or email text written to manipulate agents | Treat page and email content as data, never as commands; consequential actions must trace to the user's request; tell the user when content tries to give instructions | FR.Sa.16 |
| H7-a | Account tools | Access is broader than needed | Any other failure can do more damage | Requesting broad OAuth permissions for convenience | Request the narrowest permissions each tool needs; keep tokens out of the repository and logs | FR.Sa.17 |
| H7-b | Account tools | Outcome unknown after a timeout | Retrying risks a duplicate; not retrying risks a missed task | Network or API timeout | Check the real account state before any retry; if still unknown, tell the user and ask | FR.Sa.18 |

## 6. Safety and security requirements

### Functional

- **FR.Sa.1:** The system shall provide a keyboard stop control that works whenever the client is running and does not conflict with VoiceOver commands. (H1-a)
- **FR.Sa.2:** The system shall build the task history only from recorded actions and verified outcomes, labelling unverified entries. (H1-b)
- **FR.Sa.3:** Before each consequential action, the system shall read back its key details and proceed only after explicit approval. (H2-a)
- **FR.Sa.4:** The system shall recognize stop requests with a fixed rule that does not depend on model interpretation. (H2-b)
- **FR.Sa.5:** After a stop request, the system shall refuse all further consequential actions for that task and announce stop acknowledged and stop confirmed as separate messages. (H3-a)
- **FR.Sa.6:** The system shall assign each approved consequential action a unique ID and shall not repeat an action with the same ID. (H3-b)
- **FR.Sa.7:** The system shall pause new actions while the user is disconnected, unless background continuation was authorized for that task. (H3-b)
- **FR.Sa.8:** The system shall save task state and pending approvals, and after a restart shall announce interrupted tasks with their last known status. (H3-c)
- **FR.Sa.9:** The system shall ask a clarifying question when details required for an action are missing or ambiguous. (H4-a)
- **FR.Sa.10:** The system shall report a task as complete only after verifying its outcome, and shall distinguish verified, partial, and unverified results. (H4-b, H6-a)
- **FR.Sa.11:** The system shall pause a task and ask the user after a configured step or time limit is reached. (H4-c)
- **FR.Sa.12:** If an external service fails mid-task, the system shall pause and tell the user what was and was not completed. (H4-d)
- **FR.Sa.13:** The system shall require approval for any action not classified as read-only. (H5-a)
- **FR.Sa.14:** The system shall bind each approval to the action's exact details, use it once, and require new approval if any detail changes. (H5-b, H6-a)
- **FR.Sa.15:** When an approval request expires or is withdrawn, the system shall tell the user that the action did not happen. (H5-c)
- **FR.Sa.16:** The system shall treat webpage and email content as data, and shall only perform consequential actions that trace to the user's request. (H6-b)
- **FR.Sa.17:** The system shall request only the account permissions each tool needs, and shall keep credentials out of source control and logs. (H7-a)
- **FR.Sa.18:** The system shall check the real account state before retrying an action whose outcome is unknown, and shall ask the user if it remains unknown. (H7-b)

### Non-functional

Numbers are proposals; NFR.Sa.1 matches the Development Plan's existing target.

- **NFR.Sa.1:** The system shall audibly acknowledge a stop request within 2 seconds of the end of the utterance or key press. (H2-b)
- **NFR.Sa.2:** The system shall notify the user of a lost connection within 5 seconds, by sound if speech is unavailable. (H3-b)
- **NFR.Sa.3:** While a task is running, the system shall give a spoken status update at least every 20 seconds. (H4-c)

## 7. Roadmap

**For the POC (November):** the safeguards the POC is meant to prove: FR.Sa.3, FR.Sa.4, FR.Sa.5, FR.Sa.13, FR.Sa.14, NFR.Sa.1. FR.Sa.13 includes the test of whether browser actions can be intercepted.

**Before Rev 0 / the participant evaluation:** FR.Sa.1, 2, 6, 7, 8, 9, 10, 12, 15, 16, 17, 18, NFR.Sa.2. These matter as soon as real participants use real-looking accounts.

**Delayed (stretch):** FR.Sa.11 and NFR.Sa.3 tuning. Basic updates exist earlier, but tuned limits need usability evidence. (Team to confirm.)

## Open for the team

- Cut or merge rows. The table has 18 hazards; AlgoCatan had 15.
- Confirm proposed numbers (5 s connection notice, 20 s status interval).
- Check consistency with the SRS once drafted: every FR.Sa/NFR.Sa should appear in, or link from, the SRS.
- Diagram and LaTeX FMEA table formatting. AlgoCatan's team said the multi-page table took as long to format as to write, so start this early.
- Reflection answers (Appendix B) must come from each member's own experience.
- AI disclosure: Aaron used Claude Code (Claude Opus 5.5) to question decisions, research Hermes, LiveKit and Browser Use documentation, and draft these answers. Aaron made the decisions; the team reviews and rewrites.
