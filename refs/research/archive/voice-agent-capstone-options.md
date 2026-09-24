# Narrow voice-agent capstone opportunities

Research date: September 23, 2026. “Katan” is provisionally interpreted as CATAN. This brief broadens beyond accessibility; it does not assume the earlier browser-companion project is selected.

## Summary

The strongest opportunities attach voice to a specific activity where speaking is already natural or hands/eyes are occupied. Scope the product as **one community, one recurring moment, a few meaningful actions, and a measurable result**.

Initial recommendations, conditional on access to participants:

1. **CATAN table companion:** strongest playful capstone and multi-person interaction research opportunity.
2. **Trading-card sorting assistant:** strong physical-object workflow with measurable transcription, identification, and inventory outcomes.
3. **Trade-show follow-up or independent-brand wholesale orders:** strongest go-to-market direction to validate with real sellers.
4. **Voice workflow correction testbed:** strongest research-oriented alternative if evaluating agent architectures is more interesting than building a vertical application.

These are hypotheses, not validated market gaps. Documentation supports feasibility and existing competition; it does not prove demand, willingness to pay, or novelty. No participants have been interviewed and no integrations have been run.

## What the market already covers

- Clay's [Sculptor](https://university.clay.com/docs/sculptor) provides natural-language assistance for GTM workflows and analysis. Its [Claygent Builder](https://university.clay.com/docs/claygent-builder) supports conversational research-agent creation. A microphone alone would be weak differentiation. Some details on the Sculptor page are internally inconsistent; rely on its broad documented positioning, and test any exact integration before selecting it.
- [Jobber AI Voice and Chat](https://help.getjobber.com/en/articles/jobber-ai-voice-and-chat-beta/) already documents voice-driven business tasks. Salesforce [Voice to Form](https://www.salesforce.com/blog/voice-to-form/) addresses field data capture. Generic “voice for trades” is therefore an established direction.
- [HubSpot Mobile Notetaker](https://knowledge.hubspot.com/meetings-tool/use-mobile-notetaker-in-the-hubspot-mobile-app) already records and summarizes conversations. A generic sales note summarizer is also a weak distinction.
- [CATAN Assistant](https://www.catan.com/understand-catan/how-do-i-learn-catan) already offers narrated tutorials. A rules chatbot needs a more specific contribution to make a compelling capstone.

## Where the frontier remains interesting

### Correcting actions while speaking

“Add twelve—actually six—and use the blue one” is a state-management problem. Cancelling speech output does not undo a tool call. [IHBench](https://arxiv.org/abs/2606.19595) studies post-interruption workflow recovery. A project can make a contribution through provisional commands, explicit commits, cancellation, and verified state changes.

### Knowing who is addressing the agent

A table has jokes, side conversations, negotiations, and actual instructions. [MSI-Bench](https://arxiv.org/abs/2609.24812), submitted September 21, 2026, examines multi-speaker memory, instructions, and reasoning. It reports failures in speaker-scoped decisions and restraint. This very recent preprint motivates a research question; it does not establish a universal score for current products.

### Finishing tasks under real audio conditions

[Tau-Voice](https://arxiv.org/abs/2603.13686) evaluates voice agents on tool-grounded tasks with noise and varied accents, finding substantial gaps from its text baseline in the tested setup. Thus a fluent demo is insufficient. Measure correct end state and recovery on real recordings, separately from speech quality.

### Staying responsive while tools run

[LiveKit async tools](https://docs.livekit.io/agents/logic/tools/async/) support progress updates and cancellation during long operations. This lets a voice interface remain responsive while a slower worker researches, exports, or operates a browser. The framework capability still requires correct application-level action semantics.

## Project cards

### 1. CATAN table companion

**Who / moment:** friends at a physical CATAN game, especially a mixed-experience group.

**Example:** “Table, we rolled eight. Who collects?” “Mark that city at junction twelve.” “Undo that; it was orange, not red.”

**Actions:** record a declared roll; query board production; update public board state; retrieve an edition-specific rule; undo a mistaken event; export a game timeline.

**Why voice:** preserves attention on the table and allows shared questions without passing around a phone.

**First scope:** one base-game edition, an explicitly entered starting board, numbered locations, a designated recorder or push-to-talk button, and public state only. Production answers must account for recorded robber position; report uncertainty when state is incomplete. No hidden-card inference, autonomous player, strategy optimizer, or general camera recognition in version one.

**Engineering contribution:** a deterministic game-state engine validates actions; the model interprets language and retrieves explanations. Keep event history so corrections are auditable. Later investigate multiple speakers and camera-assisted state proposals that users confirm.

**Competition / evidence:** [official rules](https://www.catan.com/understand-catan/game-rules) and the existing narrated tutorial establish source material and a baseline. They do not grant unrestricted rights to redistribute art or imply official endorsement. Measure the improvement over an ordinary rule lookup and paper/manual tracking.

**Evaluation:** public-state accuracy after a game, missed corrections, accidental commands from normal conversation, time spent managing the assistant, and enjoyment. Abandon tracking features if logging is more disruptive than the original activity.

### 2. Trading-card sorting and inventory assistant

**Who / moment:** a Magic: The Gathering collector or small seller sorting a stack of physical cards.

**Example:** “Two copies, this printing, nonfoil. Put them in binder three.” “Actually one is lightly played.”

**Actions:** resolve card/printing; ask a targeted clarification; record count and owner-declared condition; assign a storage location; export an inventory file; retrieve source-labelled indicative prices if supported.

**Why voice:** both hands are handling cards; continuous correction is more natural than repeated form entry.

**First scope:** Magic only, a small set of supported printings, explicit printing/collector-number confirmation, local inventory, and CSV export. Optional camera input should propose identity rather than silently deciding variant or condition. Start without marketplace publishing.

**Contribution:** combine object identification, spoken corrections, and exact inventory state. Condition remains a user judgement. Quote timestamped reference data without promising sale proceeds.

**Evaluation:** verified cards entered per minute, exact-printing error rate, count corrections, and burden compared with an existing scanner app. [TCGplayer currently says it is not granting new API access](https://docs.tcgplayer.com/docs/getting-started). Use imported scan data and reviewed CSV exports instead of making marketplace credentials a dependency; see [hobby research](voice-hobby-niches.md).

### 3. Trade-show follow-up for small B2B teams

**Who / moment:** an exhibitor immediately after a short booth conversation.

**Example:** “Maya at Northstar wants a pilot for three branches. Send the integration overview, not pricing. Remind me Thursday.”

**Actions:** match the contact and company; distinguish stated facts from missing details; append a structured note; find the promised document; create a follow-up draft and task.

**Why voice:** the conversation is fresh and another visitor may be arriving. Use an intentional post-conversation debrief rather than recording everyone at the booth.

**First scope:** one CRM or test database, 20–50 seeded contacts, one event, three document types, draft-only outbound messages. A business card/photo or explicit identifier can anchor the record; do not require access to proprietary event badge data.

**Competition / evidence:** [Cvent LeadCapture](https://www.cvent.com/en/event-marketing-management/lead-capture) already captures contacts, notes, and lead ratings. HubSpot already supports meeting notes. The hypothesis is that a short clarification dialogue can accurately turn a specific promise into a prepared follow-up, beyond transcription.

**Evaluation:** wrong-person errors, promise capture, correctly selected attachments, required corrections, and time to review-ready follow-up. Compare with a voice memo plus existing CRM notes.

### 4. Wholesale order assistant for an independent brand

**Who / moment:** a ceramicist, clothing brand, or coffee roaster showing samples to a shop buyer.

**Example:** “Twelve blue mugs, six cream; delivery in October. Check the minimum and prepare the order.”

**Actions:** resolve product variants; check catalogue and availability; apply configured minimum quantities and pricing rules; create a draft order; summarize exceptions; make a follow-up task.

**Why voice:** seller and buyer are looking at physical samples. The hard information is a negotiated, frequently corrected order rather than a long written query.

**First scope:** one brand, 20–50 SKUs, one currency and price list, fixed business rules, draft orders only. No payment capture or binding delivery commitments. Read back exact quantities and variants.

**Feasibility:** [Shopify DraftOrder](https://shopify.dev/docs/api/admin-graphql/latest/objects/draftorder) provides a relevant integration surface. Alternatively, [Square Catalog](https://developer.squareup.com/docs/catalog-api/what-it-does) and [Orders](https://developer.squareup.com/docs/orders-api/what-it-does) provide commerce primitives. Choose one provider and validate permissions with a development account.

**Contribution / evaluation:** interruption-safe order capture and correct calculations. Compare with the seller's current order sheet; measure exact-order accuracy and completion time. This is a sales operations project with a natural voice setting, not a claim that order software is missing.

### 5. Voice producer for tabletop or hobby livestreams

**Who / moment:** a solo creator demonstrating cards, miniatures, coffee equipment, or a board game.

**Example:** “Producer, show the overhead shot, hide the price overlay, and mark that explanation for later.”

**Actions:** change an approved scene; toggle an approved overlay; save a replay or timestamp; check recording state.

**Why voice:** hands and eyes are occupied by the demonstration.

**First scope:** local OBS, three known scenes, one overlay, push-to-talk/private control channel, recording rather than public broadcasting during evaluation. Commands such as going live should remain deliberately separate.

**Contribution:** control that understands the current scene and lets a creator revise an instruction. [Streamer.bot already supports voice commands](https://docs.streamer.bot/guide/core/voice-control), while [OBS provides WebSocket control](https://obsproject.com/kb/developer-guide). The capstone must compare against that existing baseline. See [hobby research](voice-hobby-niches.md) for more detail.

**Evaluation:** accidental activations from programme speech, scene accuracy, correction latency, and distraction versus hotkeys or a control pad.

### 6. Repair-bench procedure companion

**Who / moment:** a student or repair-café volunteer performing a known low-risk repair while handling small parts.

**Example:** “I removed the bracket. Save this photo with step four. Which screw goes back here?”

**Actions:** retrieve a vetted model-specific guide; advance/check procedure state; attach a photo or note; maintain a parts/screw log; create a repair summary.

**Why voice:** reduces touching a phone with occupied hands.

**First scope:** one supervised procedure, one device model, source-grounded instructions, and documentation support. Do not add open-ended diagnosis or invent steps when the device differs. Avoid hazardous procedures as the initial evaluation task.

**Feasibility:** [iFixit's guide API](https://www.ifixit.com/api/2.0/doc/Guides) exposes structured repair information. Content reuse terms and edition/model matching still need implementation review.

**Evaluation:** procedure-state accuracy, lost-place events, screen touches, omitted required steps, and recovery after a mid-task question. Documentation that records what happened is a more bounded first contribution than unrestricted repair advice.

### 7. Espresso experiment assistant

**Who / moment:** an enthusiast dialing in a new bag of beans.

**Example:** “Eighteen in, thirty-eight out, twenty-seven seconds. A little sour. Compare with yesterday and log the finer grind.”

**Actions:** record exact parameters; link bean/grinder settings; compare prior shots; start a timer; optionally attach scale measurements; schedule a one-variable experiment.

**Why voice:** hands are busy and logging every trial can interrupt the ritual.

**First scope:** manual voice logging and one recipe history; no machine control, universal Bluetooth integration, or claims to infer flavour from sound. Taste is supplied by the user.

**Competition:** [Beanconqueror](https://beanconqueror.com/) already tracks brewing, including [Bluetooth integrations](https://beanconqueror.com/blog/bluetooth-device-features/). The contribution to test is a lower-friction experimental conversation; another coffee log alone is insufficient. Integration with Beanconqueror itself is unverified.

**Evaluation:** parameter transcription, logging burden, corrected records, and sustained use over a week. Keep causal language modest: one uncontrolled shot does not establish why taste changed.

### 8. Sponsorship assistant for one community organizer

**Who / moment:** a run-club, gaming-event, or student-festival organizer planning a local partnership.

**Example:** “We have sixty regular runners. Find five nearby businesses that fit, check whom we already contacted, and draft an offer for refreshments.”

**Actions:** search public business information; retrieve the organizer's actual audience facts; deduplicate contact history; draft a tailored offer; create a follow-up task.

**First scope:** one city, one event type, one spreadsheet, sourced evidence, and reviewed drafts. Never manufacture audience figures, budgets, or existing sponsorships.

**Competition:** [SponsorUnited](https://www.sponsorunited.com/) already provides sponsorship intelligence; Clay can support research and outreach workflows. The hypothesis is a workflow adapted to a small community's actual inventory and relationships.

**Voice fit:** weaker than hands-busy ideas. A conversation may clarify the offer, but a form or chat may work just as well. Select only if organizer interviews support it; no need to force voice into the product.

**Evaluation:** fit judged by the organizer, verifiable claims, duplicate-contact errors, and time to a useful shortlist. Sponsor response rates are a longer-term measure and should not be claimed from a short capstone demo.

### 9. Correction-safe voice tool benchmark and reference agent

**Who / moment:** developers building voice agents with persistent state changes.

**Example:** test “Move twelve units—sorry, two—to shelf B; no, leave them in A” against a simulated inventory system.

**Deliverable:** a small benchmark of real, consented utterances plus a reference agent that separates tentative interpretation from committed actions. Compare a simple tool caller, a schema-constrained state machine, and a version with correction-aware action staging.

**First scope:** one toy inventory/order domain, around 50–100 authored scenarios, 5–8 tools, fixed seeded state, and no real transactions. Report speaker/session-separated results if training or tuning on recordings.

**Contribution:** accurate state after corrections, rather than a new generic speech benchmark. Existing IHBench, Tau-Voice, and MSI-Bench are baselines and precedents, so any novelty claim requires a closer literature comparison.

**Evaluation:** final state, premature writes, duplicate actions after retries, cancellation handling, and recovery time. Compare against typed transcripts of the same utterances to separate speech-recognition errors from decision errors. Automated text tests do not replace microphone tests.

### 10. Voice desk for a local fighting-game tournament

**Who / moment:** a tournament organizer moving among players and stations.

**Example:** “Alex beat Jordan two–one. Read that back before reporting it. Who is still waiting?”

**Actions:** retrieve entrants and pending sets; resolve aliases; stage a score; read back the exact match; report the confirmed result; query updated bracket state.

**Why voice:** the organizer can keep attending to the venue. Noise and gamer tags make this an empirical question rather than an assumed improvement.

**First scope:** one organizer, one game, one test bracket, explicit activation, result readback, and a local pending queue. No autonomous station assignment until station data and write access are verified.

**Feasibility:** [start.gg documents bracket-result reporting](https://developer.start.gg/docs/examples/mutations/report-set/). Actual permissions and rate limits must be tested with an authorized event. The capstone adapts an established tournament platform; it does not rebuild brackets.

**Evaluation:** simulate a 16-player event, including similar aliases, noise, corrected scores, stale results, and network retries. Measure wrong-match submissions, completion time, and recovery against the ordinary mobile interface. Duplicate requests must not create conflicting reports.

## Architecture suited to a capstone

Use a responsive voice session with a small domain-specific tool set. Keep the authoritative state in ordinary application code/database, not conversation memory alone.

`microphone → speech/voice session → intent + explicit task state → narrow tools → verified result → short spoken response`

A slow browser/research worker can be called as a tool. It should emit status and accept cancellation; the voice interface should not wait silently for it. Codex can be one worker if it fits the selected task, but a whole coding harness is unnecessary for fixed inventory or game-state operations. This is an architecture recommendation, not a newly verified product integration.

MCP standardizes how a tool is exposed. It does not remove the need for account access, validation, or cancellation semantics. A few typed functions may be simpler for the first prototype. Add Composio only when a selected integration saves meaningful implementation work.

Start with push-to-talk or an explicit command prefix. Add continuous listening only if the project studies selective attention and has a clear consent/recording design. Keep no-op, pending, completed, failed, and cancelled states distinct. A tool acknowledgement is not proof of the intended final outcome; verify the domain record.

## How to select and validate

For a roughly 6–8 week capstone prototype, choose one of the cards, not a platform supporting all ten. Suggested schedule:

- Week 1: talk to five accessible participants in the chosen community; observe the actual task; select one recurring failure or inconvenience.
- Week 2: build a tool-only workflow and collect baseline time/error data.
- Weeks 3–4: add voice, narrow clarification, and correction handling.
- Week 5: test real microphones, background speech, failures, and reconnects.
- Weeks 6–8: participant comparison, fixes, and a reproducible evaluation/demo.

This is a planning estimate, not a delivery guarantee; recruitment and integrations can dominate schedule.

Use [LiveKit's evaluation tools](https://docs.livekit.io/agents/start/testing/) where useful for tool assertions, and separately test real audio. Measure task correctness, action errors, effort, correction latency, and total cost per completed task. For a hobby project, also measure whether the assistant interrupts enjoyment.

The decisive question is: **Can the team reach people who do this task, and does speaking improve that task enough to justify an assistant?** A narrow and well-evaluated answer is a stronger capstone than a wide demo with many integrations.
