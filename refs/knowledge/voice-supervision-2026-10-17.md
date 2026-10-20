# Voice supervision decisions and proposed requirements

Source: Aaron's October 17, 2026 discussion in Codex. These are Aaron's decisions and assistant wording proposals, not whole-team ratification or tested capabilities. This record supersedes conflicting earlier discussion notes. Aaron authorized the coordinated revision. These decisions are reflected in the SRS. Aaron subsequently excluded Hazard Analysis edits. Its source and PDF were restored to the pulled branch version. Team review and runtime validation remain pending.

## Decisions from Aaron

- An explicit request to stop working pauses the task and preserves it for possible resumption. Prevent further execution; an external operation that cannot safely be interrupted may settle. Explain completed work, paused work, work not performed, and uncertain outcomes. Do not promise that every external operation will complete or become verifiable.
- Ordinary conversational interruption stops spoken output without automatically pausing the underlying task. Resuming the conversation does not by itself authorize resuming paused work. Determine the intended request from context and clarify ambiguity before acting.
- The initial permission policy requires approval for writes and consequential decisions. Ordinary navigation does not need approval just because a click changes the displayed page. A later mode with fewer approval prompts is an idea, not an initial requirement.
- Users may speak one-time authentication codes. An accessible private typed-input route is a candidate alternative; no implementation or provider isolation is established. Do not claim spoken codes stay out of speech/model processing.
- Speech should be natural and relevant. Do not mandate a fixed cadence of status announcements. Exact timing and model settings are implementation choices to evaluate.
- Verification can use the connector's result, the relevant account state, or a browser confirmation. Match the evidence to the task rather than insisting on a separate API read for every action.

## Proposed wording for the coordinated SRS/HA revision

### Pause, cancel, and resume

The system shall interpret an explicit request to stop working as a request to pause the current task. It shall promptly acknowledge the request and prevent additional task actions from starting. It shall cancel or suspend ongoing work where supported and safe. An already-issued operation that cannot safely be interrupted may settle; any checks performed while paused shall be limited to reconciling that operation, not advancing the task. The system shall report what completed, what remains paused or unperformed, and any unknown outcome. It shall preserve task context and resume execution only on a clear user request. A request to cancel or abandon the task shall end it rather than merely pause it.

Suggested spoken example: "Paused. The first invitation was sent. The second was already being sent, so I am checking its result. The other three have not been sent."

Recheck target details and external state on resumption. Do not automatically reuse an approval when its action details or relevant state changed. Pending approval handling across pauses needs a consistent policy in FR9, FR20, the state machine, and safety requirements.

### Approval

The system shall request explicit approval before actions that write or delete user/account data, submit information, communicate externally, grant permissions, accept terms, or otherwise make a consequential commitment. Navigation and temporary preparation may proceed without approval only when they do not trigger such an effect. Classify by the effect of the action, not whether its tool is called "click" or "read". Ask when the effect cannot be classified reliably.

Applied clarification: the existing automatic rejection of non-essential cookies is retained as the sole consent exception. Both documents state it explicitly. Unclear prompts need user input. Temporary preparation is distinguished from autosaved drafts and settings writes. A reduced-prompt mode remains deferred.

### Natural conversation

The system shall support spoken requests, corrections, and interruptions during an active voice session using the selected voice framework's turn-taking facilities. It shall provide concise, task-relevant feedback when user input is needed, the task pauses or encounters a blocker, or a result is available, and shall answer requests for current status. Routine progress updates shall reflect the task and conversational context rather than a fixed announcement interval. The user shall be able to interrupt spoken output without restarting the task.

Implementation note: VAD detects speech activity; end-of-turn detection estimates whether the user has finished; interruption handling decides whether the agent should yield speech; application logic decides whether there is something useful to say. See the [public research note](../research/livekit-turn-taking-2026-10-17.md). Audio interruption and external-tool cancellation must be implemented and tested separately.

Do not interpret short listener acknowledgments as action approval outside a pending approval question. Keep explicit stop acknowledgment and failure/disconnection handling testable even though routine speech timing is flexible.

### Authentication

The system shall allow the user to provide a one-time authentication code by voice. A private accessible typed-input route is proposed as an alternative. Explain that speaking a code exposes it to the configured speech/conversation processing path and nearby listeners. Avoid retaining codes in application task history or logs; verify what can actually be excluded from provider processing and retention before making stronger claims. Password input remains a separate decision and is not authorized through voice by this discussion.

### Verification

The system shall evaluate the outcome of a consequential action using evidence appropriate to that action, such as a successful connector response that confirms completion, a matching account record, or a website confirmation. It shall check that the evidence corresponds to the intended action and relevant details. It shall report a completed, partial, failed, or uncertain result without claiming more than the evidence supports.

Examples: an event-create response containing the expected event details may be enough to confirm event creation; a matching saved event or browser confirmation can also suffice. A response that only confirms queuing does not establish sending or delivery. A button click, tool invocation, or absence of an error alone does not necessarily establish that the intended action succeeded. Use another check when the initial evidence is ambiguous; if no adequate check is available, report uncertainty and avoid blindly repeating the action.

## Evaluation implications

Use representative conversations with natural pauses, short acknowledgments, corrections, and interruption of long output. Verify the user can ask for status, pause work, and resume without losing context. Check an external operation that settles after pause and one whose outcome remains unknown. Test meaningful action-result evidence and prevent duplicate writes after ambiguous outcomes. Tune framework timing during the POC and participant evaluation; do not claim naturalness has been established by source review.

## Applied document changes

- Replace stop-as-cancellation with pause semantics in FR3/FR8, scenarios, safety requirements, diagrams, transitions, and properties. Distinguish user cancellation from pausing; include Stopping in the one-active-task constraint while operations settle.
- Replace the fixed announcement cadence in FR5/NFR.Sa.3 and remove or repurpose IDLE_PROMPT_TIME. Keep execution step/time limits separate from spoken-update policy.
- Revise E.3/FR23 and privacy claims for the spoken-code decision.
- Align FR9/FR10/FR24 and FR.Sa.13 around writes, commitments, navigation, and explicit exceptions.
- Revise FR12/FR.Sa.10 so evidence can be a meaningful tool result or a targeted check; remove an unconditional separate re-read after every operation.
- Update acceptance criteria and traceability after the wording and remaining decisions are settled.

Implementation policy chosen in this drafting pass: pause withdraws unused approvals. Resume requires fresh approval for remaining writes. Already-submitted external operations are tracked separately from task control state. This is a conservative draft policy for team review.
