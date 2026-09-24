# Natural Control: current project context

Updated September 23, 2026 after the user interview and explicit authorization to prepare drafts. Natural Control is a working name. This record supersedes earlier brainstorming.

## Decisions confirmed by Aaron

- Build a general-purpose accessible conversational interface to an existing agent, primarily for blind people with screen-reader experience. Do not restrict the product to events, a site allowlist, or scripted workflows.
- Initial evaluated environment: Mac, Chrome, English. Browser tasks are representative tests; connected tools and local computer use are also in the POC. Safari and broader platform support remain extensions.
- General agents decide how to use available tools. The capstone's principal contribution is accessible delegation, feedback, clarification, approval, correction, and recovery, not training a new foundation model.
- Main harness candidate: Hermes. Browser Use supplies browser capabilities; it is not interchangeable with the whole Hermes agent. OpenClaw is excluded from the proposed stack at Aaron's request. Codex/OpenClicky are comparison/reference material, not a subscription requirement.
- Expected client: accessible TypeScript/React web interface plus a local service. Python for voice/agent integration; LiveKit expected. ElevenLabs is a speech-output candidate, Jev an optional structured-decision component. Exact model/provider choices require evaluation.
- Compare phone calls and on-Mac voice access. Start explicitly initiated conversations. The initial client is web-based; the second voice channel is the leading stretch goal. iMessage is an idea, not a committed feature.
- Hybrid deployment direction: always-available Mac/Mac mini or hosted service, with a local component for local tasks. A VPS cannot provide access to an offline Mac. Having an always-on computer is an option, not a claim about all blind users.
- Use connected-account tools, hosted/local browsers, or Mac control as appropriate. Gmail and Google Calendar anchor the first connector tests. Connections and credentials are separately authorized by users.
- Navigate and prepare autonomously; obtain explicit approval before consequential actions. Ordinary barge-in pauses speech only; explicit stop cancels execution. Disconnection pauses new actions unless background continuation was authorized.
- Give meaningful progress updates and on-request detail, rather than narrating every click. Preserve VoiceOver/keyboard compatibility and accessible task history. No raw microphone-audio retention by default; explain independent cloud-provider policies.
- Assisted initial setup is acceptable; everyday task use should be independent. Support one tested default configuration with documented extensions and user-provided credentials. Cloud services permitted; fully local inference is not a requirement.
- Aim for a useful open-source contribution and prototype, plus a strong course result. MIT is the proposed license. No known external confidentiality/IP agreement; confirmation by other contributors pending.
- Team budget ceiling: CAD 500, subject to course rules and agreed allocation, not authorization for purchases.

## Evaluation proposals accepted for the draft

- Main POC risk: whether live conversation can supervise a general agent across account tools, an unfamiliar website, and a local Mac task.
- Include clarification, approval, correction, meaningful progress, explicit execution stop, and reconnection. Use synthetic data and test accounts.
- Provisional targets: at least 80% correct independent task completion on a declared suite; explicit stop acknowledged within two seconds; all consequential actions in test cases approved. Acknowledgment is not proof of cancellation; no new actions may be issued after confirmed stop.
- Seek four to six blind collaborators for repeated discovery/evaluation. Recruitment and availability are unconfirmed. A personal connection may facilitate a CNIB introduction; no partnership is claimed. Personal contact details are deliberately absent here.
- If remote telephony or native control fails, preserve local voice with general browser/account tools and defer the failed capability. Document changed evaluation scope honestly.
- Propose fall Interview Report and winter Usability Report for instructor approval.

## Team-process proposals requiring whole-team ratification

Four members; Aaron Loh is the only supplied name. Weekly sync plus asynchronous updates in Discord; tasks/decisions/meeting agendas and attendance in GitHub. Plan weekly output commitments, not hour or commit quotas. Primary owners with cross-review and revisitable assignments. One non-author reviewer and relevant automated checks per pull request. Internal draft deadline 48 hours before course deadlines.

Acknowledge actionable messages within one working day. Flexible attendance is acceptable with a written update and necessary input before the meeting; emergencies communicated as soon as practical. Two unexplained missed commitments within a month trigger a team recovery discussion; unresolved non-participation goes to the TA. Decide using evidence/experiments, then vote; the responsible owner breaks technical ties, and the TA advises on course-policy disputes. Brief demos, informal check-ins, and recognition of useful contributions support cohesion.

Broad AI use is allowed in development with source/behavior verification, human ownership, cross-review, and accurate disclosure.

## Pending facts; authorized placeholders in drafts

Other three names, exact meeting day/time and mode, named technical/process owners, GitHub Projects URL, team/project registration and instructor approval, TA collaborator access, individual/team reflections, ratification of process and license, participant recruitment, final model/tool selections.

## Evidence and state

See [milestone brief](milestone-1.md), [rubric map](rubric-map.md), [TA guidance](ta-meeting-2026-09-23.md), and [technology evidence](../research/agent-foundations-2026-09-23.md). No working Natural Control application or user study exists yet. Source review is not runtime verification. Draft PDFs and local knowledge edits are not published submissions.
