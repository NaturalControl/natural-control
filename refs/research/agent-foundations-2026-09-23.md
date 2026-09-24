# Agent foundations — evidence checked September 23, 2026

## Evidence boundaries

**User decisions:** general-purpose agent supervision; Mac/English first; Hermes primary; OpenClaw excluded; ordinary barge-in stops speech only; explicit stop cancels work; disconnected sessions pause new actions unless continuation authorized.

**Team proposals awaiting ratification:** architecture, MIT license, budget allocation, charter, ownership, evaluation targets and custom documents. **Untested assumptions:** reliable integrated stopping, readable voice progress alongside VoiceOver, native control, affordable operation, successful recruitment and independent task completion.

## Primary-source register

| Source | Documented fact used | What still needs testing |
|---|---|---|
| [Hermes programmatic integration](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration) | Custom clients can use streaming session events, steering, interrupts and approval/clarification requests. | Pin a release; test actual cancel and reconnect semantics. An interrupt method is not an end-to-end stop guarantee. |
| [Hermes browser automation](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser/) | Browser Use is a documented browser path with other mechanisms available. | Packaged browser versus existing signed-in Chrome, auth, compatible versions and fallback behavior. |
| [LiveKit voice quickstart](https://docs.livekit.io/agents/start/voice-ai/) and [tools](https://docs.livekit.io/agents/logic/tools/) | Voice sessions and tool integration provide building blocks. | Conversational responsiveness while an external agent runs; downstream action cancellation. |
| [ElevenLabs plugin](https://docs.livekit.io/agents/models/tts/elevenlabs/) | Documented speech-output integration. | Intelligibility, interruption, actual usage cost and provider retention. |
| [Jev](https://vercel.com/ai-gateway/models/jev) | Structured evaluation/routing candidate. | Added value over deterministic decisions; not established as a primary conversation or vision agent. Promotional pricing is temporary. |
| [Codex app server](https://learn.chatgpt.com/docs/app-server) | Alternative custom-client agent surface. | Does not establish inherited desktop plugins/connectors or suitability for our deployment. |
| [WebAIM survey 10](https://webaim.org/projects/screenreadersurvey10/) | Users report navigation barriers; screen readers already support selective navigation. | Self-selected survey is not prevalence in our participants; interview users before prioritizing. |
| [Morae](https://arxiv.org/abs/2508.21456) | Research investigates meaningful user choices during UI-agent execution with blind/low-vision users. | Prior research motivates agency; it does not validate Natural Control. |
| [MIT text](https://choosealicense.com/licenses/mit/) | Permissive terms retain copyright and permission notice. | Team ownership/ratification; dependency-by-dependency notices. |

The bibliography in `refs/CapstoneSources.bib` supports the milestone drafts. These observations are documentation checks, not benchmarks or runtime validation. Avoid copying changing product promises into project guarantees.

## OpenClicky implementation reference

Static inspection of [OpenClicky at e9eb06a](https://github.com/jasonkneen/openclicky/tree/e9eb06a29ff5cd82033d032238f51a936168b05a) found a Swift client using Codex app-server integration and computer-use/voice components. It is an alternative/reference, not the selected harness. Static source inspection does not establish successful local execution, blind usability, or a completely local model stack. Do not copy broad permissions without evaluating our own action boundary.
