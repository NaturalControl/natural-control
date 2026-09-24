# Voice access to the web: research and project options

Research date: September 14, 2026. This is a source-based feasibility and product brief, not a tested product evaluation. Product documentation establishes advertised capabilities; research results establish findings only within each study's conditions. Recommendations and estimates below are our design proposals.

## Recommendation

Build a voice-controlled browser companion with blind and low-vision participants. Begin with finding, comparing, and reading information on real websites. Add one bounded interactive workflow after users demonstrate that they can inspect results, correct the agent, and recover independently.

The proposed product promise: **Get to the information and actions you want, with control over what is read, skipped, and done.**

Do not make abandoning screen readers a success criterion. Preserve keyboard, text, and Braille-compatible output. A useful outcome is less navigation effort and less dependence on another person. Whether people replace or combine tools is their decision.

See [the accessibility landscape](accessibility-landscape.md) for screen readers, existing AI products, and studies with blind participants.

## 1. What Codex and Grok Bot actually provide

### Codex browser and computer use

The desktop product offers an integrated browser with its own profile; a browser extension can work in existing supported browser sessions. The integrated browser capability is not automatically available in the Codex CLI or IDE extension. Native computer use is a separate capability on supported macOS and Windows configurations. These distinctions matter when choosing a foundation for another product. Sources: [browser documentation](https://learn.chatgpt.com/docs/browser?surface=app), [computer-use documentation](https://learn.chatgpt.com/docs/computer-use).

Codex's open-source app-server is a supported integration surface for custom clients, including streaming events, conversation state, and approvals. It should not be treated as a promise that the proprietary desktop browser runtime is bundled into any custom client. Source: [app-server](https://learn.chatgpt.com/docs/app-server).

Conceptually, the host gives an agent observations and actions. Observations may be rendered page structure or screenshots; actions may be browser operations, API calls, or mouse/keyboard input. The host executes the proposed action and returns the new state. A model is not literally installed inside every web page. This is an architectural explanation, not a claim about undisclosed Codex internals.

### Grok Bot

The current first-party product is distinct from unrelated GitHub repositories called GrokBot. Its documented environment is a persistent cloud computer with browser, terminal, files, and connectors. Bots on one account share credentials and browser sessions, although they have separate screens. Authentication and other blocked steps may require user takeover. Source: [Grok Bot computer and apps](https://docs.x.ai/grok-bot/computer-and-apps).

Accessibility implication: a visual remote-desktop preview and a request to “take over” are not sufficient evidence of accessible supervision. We would need to test the actual handoff with screen readers, keyboard input, passkeys, and errors. This review did not test Grok Bot's UI or establish its accessibility conformance.

### Other relevant foundations

- [Playwright MCP](https://github.com/microsoft/playwright-mcp) exposes structured accessibility snapshots and browser actions. It is a practical prototype building block; browser automation reliability is distinct from making the agent's own interface accessible.
- [Claude computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) exposes screenshot and input tools executed by the application. This is another possible model backend, not an accessibility interface by itself.
- [Magentic-UI](https://www.microsoft.com/en-us/research/blog/magentic-ui-an-experimental-human-centered-web-agent/) is an open-source research prototype for collaborative planning, execution, and intervention. Its interaction concepts are relevant; its existence does not prove independent usability by blind people.

## 2. The frontier that matters for this project

### Preserving choice while reducing work

[Morae, UIST 2025](https://arxiv.org/abs/2508.21456), studies pausing agents at decisions so blind and low-vision users can express preferences. This is closely aligned with our opportunity: completing an instruction is not sufficient if the agent hides meaningful alternatives.

[A11y-CUA, CHI 2026](https://arxiv.org/abs/2602.09310), evaluates agents under assistive-technology conditions and documents a collaboration gap. A strong score on a conventional browser benchmark does not establish that a blind user can supervise or recover from that agent.

Our design inference: prioritize understandable state and choices alongside task completion. A summary should reduce noise without silently narrowing the user's options.

### More capable local models

Microsoft released [Fara1.5](https://microsoft.github.io/fara/) in 4B, 9B, and 27B variants in July 2026. These open-weight agents use screenshots and actions. They make local experimentation credible, but benchmark results do not establish reliable accessible browsing on a participant's laptop.

Recent research also challenges “just let it think longer.” A [July 2026 study of local computer-use agents](https://arxiv.org/abs/2607.28573) reports diminishing returns and shifting failure modes when increasing inference-time compute. An [August 2026 GUI/MCP study](https://arxiv.org/abs/2608.03327) finds that adding tools can help or hurt depending on the model's tool decisions. Both are recent preprints, not deployment guarantees.

### Websites exposing agent actions

[WebMCP](https://developer.chrome.com/docs/ai/webmcp) lets websites expose structured actions through page APIs. Chrome's documented origin trial starts in Chrome 149; this remains an evolving capability, not universal website support. It could make some tasks substantially easier, but it requires website cooperation. Treat it as an optional route, not the sole foundation for access.

## 3. Proposed architecture

Use one user-controlled session and one active browser action stream for the first prototype.

1. **Input:** speech, keyboard command, or text. Include a local interrupt that stops both speech and queued actions.
2. **Intent:** keep the user's goal, constraints, and unresolved choices in explicit session state.
3. **Observation:** use the permitted API or browser page; associate facts with their source and capture time.
4. **Action:** use a narrow allowlist of operations. Read and prepare freely within the task; review consequential submissions.
5. **Verification:** obtain fresh state after actions. A generated sentence saying “done” is not verification.
6. **Presentation:** offer brief speech, detailed speech, exact source text, and accessible text/Braille output from the same state.

Preferred execution order, adjusted to what the task actually needs:

| Route | When it helps | Remaining dependency |
|---|---|---|
| Service API / approved connector | Structured email, calendar, records | Provider coverage, scopes, authentication |
| WebMCP | A visited site advertises the needed action | Site implementation and browser support |
| DOM / accessibility tree | Page text, links, tables, form fields | Missing labels, custom controls, dynamic state |
| Screenshot + OCR / vision | Unlabelled or visually rendered content | Ambiguity, crop context, latency, grounding |

DOM means the browser's structured representation of the page. The accessibility tree describes roles, names, states, and relationships exposed to assistive tools. They overlap but are not interchangeable.

Combining these routes reduces dependence on correctly labelled controls. It does not make inaccessible design harmless: a screenshot can miss hidden content or state, and a guessed control label can be wrong.

### The spoken interface

Proposed commands:

- “What is this page?” Short orientation, including site and page title.
- “Answer my question.” Relevant information with source and uncertainty.
- “Read it exactly.” Literal source text, clearly distinguished from a summary.
- “What did you leave out?” Other sections, alternatives, and exclusions.
- “Compare these two.” Stable named options and relevant differences.
- “What changed?” Last verified action and current state.
- “Stop.” Immediate interruption independent of model inference.
- “Go back.” Navigate back where possible; explain when a submitted action cannot be undone.
- “Let me take over.” Restore a usable focus position and give a short state explanation.

Use user-adjustable speech speed and verbosity. Design audio ownership so the assistant and screen reader do not talk over one another. For expert users, short commands and exact reading may matter more than conversational warmth. Validate this rather than assuming one preference.

### Voice plumbing

For the first prototype, a speech-to-text → agent → text-to-speech pipeline makes stages inspectable and interchangeable. [OpenAI's voice architecture guide](https://developers.openai.com/api/docs/guides/voice-agents) also documents realtime and full-duplex alternatives. Natural turn-taking is useful, but it must not obscure the distinction between a plan, a pending action, and a verified result.

Local speech recognition is a realistic starting component; [whisper.cpp](https://github.com/ggml-org/whisper.cpp) provides microphone transcription examples. Select and benchmark engines on actual devices and voices. Do not send passwords through the spoken assistant or require users to dictate them in public.

## 4. MCP and Composio: opt-in connections

MCP is a protocol for exposing capabilities to a client. It does not itself supply universal app access or decide what a user has authorized. Source: [MCP architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture).

[Composio authentication](https://docs.composio.dev/docs/authentication) provides per-user connected accounts and manages credentials and refresh. Its [session MCP interface](https://docs.composio.dev/docs/sessions-via-mcp) can expose a configured user's tool access. These are useful implementation services, not substitutes for the product's consent model.

Proposed connection flow:

1. User asks for a task requiring an account.
2. Assistant explains the service, account, and requested access in plain language.
3. User authenticates in an accessible provider-owned flow; test every handoff.
4. Begin with read-only scopes where available. If a provider only offers broader scopes, disclose that and restrict actions in the host.
5. Use a small tool allowlist and verify account selection for each task.
6. Provide an accessible list of connections with revoke/disconnect controls.

For a first trial, one calendar or email integration is enough. Do not load hundreds of tools into every prompt. Do not mix personal and work accounts invisibly. Composio introduces a hosted service dependency even when the speech and model run locally.

## 5. Local inference and cost

Separate four questions: where the browser runs, where speech recognition runs, where reasoning runs, and where external data is stored. A local app or local Codex subprocess does not imply local model inference.

Recommended initial approach: local browser and basic speech/control, a cloud reasoning model to establish usefulness, then benchmark a local model on exactly the same tasks. Offer a genuinely local-only mode with explicit limitations; cloud escalation should be an informed opt-in.

Avoid per-minute claims before measuring. Track:

`cost per independently completed task = total inference + speech + connector + hosting cost / independently completed tasks`

Count failed attempts, retries, and long pauses. For local processing include memory, battery, heat, startup/download friction, and device cost rather than treating inference as free.

Useful optimizations to test:

- Extract relevant text locally and keep source pointers.
- Cache page observations; invalidate after navigation or meaningful changes.
- Send changed regions instead of replaying every screenshot.
- Read exact text directly through speech synthesis without asking a language model to rewrite it.
- Handle stop, repeat, and speed changes locally.
- Use narrow tools and known workflows; add vision only when structural observations fail.

Arithmetic illustration, not a benchmark: 20 steps re-sending 10,000 input tokens consume 200,000 input tokens before output, audio, or images are counted. Cutting those observations to 2,000 tokens gives 40,000. Measure task quality after any compression; omitted context can hide important choices.

## 6. Three scoped projects

Estimates assume a small experienced team, existing models, and participant recruitment running alongside engineering. They are prototype estimates, not promises of production readiness.

### A. Voice browsing companion — recommended first

**Outcome:** answer questions and compare options on user-selected websites without wading through repeated navigation.

**Scope:** one desktop browser; public pages; short orientation; grounded Q&A; exact reading; links and search; table comparison; pause/repeat/back. Test across 3–5 sites chosen from interviews, including inaccessible examples. Add one bounded filter/form workflow only after the reading experience works.

**Example:** “Find evening classes on this community centre's website. Compare the times and prices. Read the cancellation policy exactly.”

**Exclusions:** payments, identity verification, arbitrary desktop control, promises to support every website.

**Prototype:** roughly 4–6 weeks after an initial discovery round.

**Evaluation:** users' own information-finding tasks; factual accuracy and omitted critical details; independent completion; time; ability to find source evidence; recovery after deliberately introduced errors. Include exploratory browsing, where the user does not know the options in advance.

### B. Assistant for one blocked workflow

**Outcome:** complete a recurring task that participants currently abandon or ask another person to do.

**Scope:** choose one task after observation, such as selecting a library reservation or navigating a course-registration form. Prepare changes, read a concise review, and verify the result after user approval. Use test accounts/sandbox data for consequential flows during development.

**Prototype:** roughly 6–8 weeks, strongly dependent on the selected site and authentication.

**Evaluation:** correct choices, independently recoverable failures, exact submission review, and accessible handoff at the point of difficulty. A recoverable pause is better than falsely claiming success.

### C. Voice access to connected tools

**Outcome:** inspect an inbox or calendar without navigating the underlying app.

**Scope:** one provider, read-only first. Ask about upcoming events or selected messages; retrieve exact wording; make drafts as a subsequent stage. Add sending/booking only with understandable previews and verified outcomes.

**Prototype:** roughly 3–5 weeks for a bounded pilot including accessible onboarding.

**Evaluation:** account/scoping correctness, missing information, authentication completion, deletion/revocation of connections, and usefulness compared with the participant's current tools.

This is potentially easier to make reliable than arbitrary browser automation, but usefulness must be demonstrated against existing accessible apps and voice assistants.

## 7. Co-design and evaluation plan

Start with 6–8 paid discovery participants, sampled across screen-reader experience, blindness/low vision, device use, and communication preferences. This is qualitative discovery, not a representative sample or a statistical validation study. Include ongoing paid blind collaborators in product decisions. Broaden the pilot as patterns emerge.

Potential recruitment/research route: [CNIB Access Labs' accessibility testing work](https://www.cnib.ca/en/accessibility-design) and [CNIB Research](https://www.cnib.ca/en/resources/research). These are leads, not existing partnerships; no outreach has been sent.

Interview by observing actual tasks:

1. Show a web task you recently abandoned or needed help with.
2. Show a task your present tools handle very well.
3. Which information do you skip, and which must never be skipped?
4. When should an assistant act, explain, or stop for a choice?
5. How would you detect that it chose the wrong item or misunderstood you?
6. Where is speaking inconvenient, tiring, unsafe, or impossible?
7. What device and connection constraints should we design around?

Compare each participant's usual setup, a generic agent with voice, and the prototype. Counterbalance task order and use comparable task variants to reduce learning effects. Do not compare expert screen-reader users only against an unfamiliar or poorly configured baseline.

Measure verified task completion, assistance required, consequential errors, omitted details, time, interruption response, recovery, workload, and user preference. Report these separately. Do not combine correctness and pleasant speech into one success score.

Suggested engineering targets for a pilot, to negotiate with users: immediate local acknowledgement/stop, explicit errors instead of silence, no consequential action without the agreed review, and zero false “completed” claims in the evaluated set. Zero observed failures is not proof of zero risk.

## 8. What OpenClicky contributes

Static inspection at commit `e9eb06a`; the app was not built or tested because Xcode is absent.

- `CodexProcessManager.swift` launches a Codex app-server subprocess.
- `CodexVoiceSession.swift` submits transcribed prompts with screenshot attachments and supports turn interruption.
- `OpenClickyParakeetTranscriptionProvider.swift` implements local FluidAudio/Parakeet transcription on supported Apple Silicon setups.
- `OpenClickyComputerUseRuntime.swift` includes app/window observation, captures, keyboard input, and computer-use plumbing.
- `ClickyCodexConfigTemplate.swift` configures optional Composio and computer-use MCP services.
- UI files contain accessibility labels, but labels alone do not establish usable focus, speech coordination, onboarding, or task recovery.

Source: [OpenClicky repository](https://github.com/jasonkneen/openclicky/tree/e9eb06a).

One material design issue: the shared config template renders unrestricted access and no approvals, while the voice-turn path explicitly narrows its sandbox. These are different execution paths. Any adaptation must replace broad agent permissions with task-scoped actions and accessible review rather than assuming voice input supplies adequate control.

Recommendation: use OpenClicky as a reference and potentially reuse selected components. Choose the prototype platform based on participants' devices. Its macOS-specific overlays should not determine the target population.

## Decision

Proceed with paid discovery and Project A's small browser companion. The central research question is whether selective narration plus inspectable, interruptible actions produces greater independence on tasks users actually value. A generic agent with a microphone is the baseline to beat.
