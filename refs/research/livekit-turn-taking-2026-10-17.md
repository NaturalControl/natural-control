# LiveKit turn-taking research

Checked October 17, 2026 against the current official documentation. This is a documentation review, not a tested Natural Control integration. SDK versions and deployment must be checked before selecting an implementation. The recommendations below are proposals for the requirements review, not team agreements.

## What the framework handles

| Mechanism | Question it addresses |
| --- | --- |
| Voice activity detection (VAD) | Is someone speaking, or is there silence? |
| End-of-turn detection | Has the user finished their thought, including after a pause? |
| Endpointing | How long should the system wait before committing that turn? |
| Interruption handling | Should incoming speech interrupt the agent's current speech? |
| Application speech decisions | Is there something useful to say about this task now? |

The first four mechanisms affect conversational timing. They do not determine which task updates are meaningful to a blind user. LiveKit supports different turn-detection strategies, including provider endpointing, its own models, realtime-model detection, and manual control. [Turns overview](https://docs.livekit.io/agents/logic/turns/)

The currently documented audio turn detector combines acoustic and semantic cues rather than treating silence alone as completion. Its full model is hosted; a smaller model runs locally. It requires Python Agents SDK 1.6.1 or later, or Node.js SDK 1.4.7 or later. The older transcript-based detector is deprecated. Realtime models need compatible configuration to avoid two systems controlling turn boundaries. These are current documented options, not proof of availability in a previously installed SDK. [Turn detector](https://docs.livekit.io/agents/logic/turns/turn-detector/)

Adaptive interruption handling attempts to distinguish genuine interruptions from listener acknowledgments such as "uh-huh." Availability depends on SDK version, deployment, and pipeline capabilities. Cloud deployment is supported; local development has limits. Aligned STT transcripts or a compatible realtime configuration matter. Treat this as a candidate to evaluate rather than an unconditional default. [Adaptive interruption handling](https://docs.livekit.io/agents/logic/turns/adaptive-interruption-handling/)

LiveKit exposes timing, false-interruption recovery, and consecutive-speech spacing settings. Its tuning guide treats these as interacting controls, with troubleshooting advice for premature replies and false interruptions. Numeric defaults belong in implementation configuration and experiments, not permanent product requirements. [Turn-taking tuning](https://docs.livekit.io/agents/logic/turns/tuning/)

## Speech interruption and execution are separate

LiveKit explicitly documents that interrupting an agent does not, by default, cancel the running tool's background work. Python tools need explicit cancellation handling; Node.js tools can propagate an abort signal on the supported voice-pipeline path. The documentation recommends protecting irreversible writes from interruption so they do not end partly complete. An SDK cancellation signal also cannot establish that a remote service rolled back a write already received. Test the actual tool, connector, and browser behavior. [Function tools: interruptions and HTTP APIs](https://docs.livekit.io/agents/logic/tools/definition/)

For Natural Control, ordinary conversational barge-in should stop or yield speech while task execution follows its own policy. An explicit work-pause command should immediately block dispatch of further task actions. Work already submitted may complete if it cannot safely be interrupted. The system should then explain what completed, what remains paused, and any outcome it could not determine. Resuming the voice connection should not silently imply permission to resume task execution.

LiveKit's recommended handling of uninterruptible writes must not prevent the accessible pause control from registering intent and blocking subsequent actions. This boundary needs an integration test, especially if the voice session and Hermes run in different processes.

## Proposed SRS wording

These are candidate behavioral requirements, not claims about implemented capabilities:

- The system shall support conversational speech input, including pauses within a user's turn and corrections while the agent speaks, using a supported turn-taking configuration.
- The system shall provide concise, relevant spoken feedback for clarification, approval, task outcomes, and changes requiring user attention. It shall also provide task status on request. Routine updates should reflect the task and user preferences rather than a fixed narration schedule.
- The system shall distinguish an interruption of spoken output from an explicit request to pause work.
- When work is paused, the system shall prevent new task actions, attempt to interrupt safely cancellable work, and report completed work, unfinished work, and unresolved outcomes. It shall wait for an explicit instruction to resume work.
- The system shall allow an interrupted explanation or approval request to be repeated on request without treating the interruption as approval.

Avoid a promise of perfectly natural timing. Naturalness is an evaluation objective supported by configuration and iteration, while essential user control is an observable requirement.

## Evaluation proposal

Use the actual supported SDK and deployment to test: a pause within a sentence; a short acknowledgment during agent speech; a correction; an explicit work-pause during a read; a pause during a submitted write; resuming conversation while work stays paused; and requesting status or repeating an interrupted question. Record premature replies, missed corrections, false interruptions, conversational delay, participant feedback, and whether task actions follow the pause policy. Include slower speech and differing pause patterns in participant testing. Do not infer accessible usability from vendor benchmark results.

The remaining implementation decision is how task events reach the voice agent and how it chooses useful updates. That can begin with a small set of meaningful events and conversational generation. It does not require training a custom turn detector or committing to a fixed progress timer.

## Provenance

Prepared with Codex from official public LiveKit documentation for human review. No runtime results or participant findings are claimed. This shared note contains no private project material.
