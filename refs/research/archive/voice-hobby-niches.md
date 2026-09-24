# Hobby and cultural niches for voice agents

Research snapshot: 23 September 2026. These are project hypotheses, not evidence of demand or claims of novelty. “Katan” is interpreted as CATAN. Estimates assume a small capstone team and access to willing participants.

## Best three to investigate first

1. **Trading-card intake assistant**: strongest physical reason to use voice; measurable throughput and error rates; can work with CSV instead of requiring seller API access.
2. **Local fighting-game tournament desk**: very specific user, noisy real-world research challenge, and a documented API for actual actions.
3. **Hands-busy livestream producer**: strongest reliable demo, especially cooking, miniature painting, or instrument instruction; must beat existing voice macros rather than merely reproduce them.

## 1. Trading-card intake assistant for a small shop

**Interaction:** Holding a card under a camera: “Two copies, lightly played, nonfoil; put those in box B. Actually, only the first copy is lightly played.”

**What exists:** TCGplayer offers card scanning, catalogue matching, correction, and inventory staging. Its own mobile-app instructions explicitly require checking quantity, set, foiling, condition, and language after scanning. This makes a narrow correction-and-cataloguing workflow more defensible than building another card scanner. [TCGplayer scanning workflow](https://help.tcgplayer.com/hc/en-us/articles/23531246396183-How-to-Setup-and-Use-the-TCGplayer-App-for-Card-Scanning), [Scan & Identify](https://help.tcgplayer.com/hc/en-us/articles/27303403772823-How-To-Use-Scan-Identify)

**Why voice:** Hands are sorting cards; keyboard interaction interrupts the physical workflow. This is a design hypothesis to test directly.

**Four-week MVP:** One game, a small known catalogue or imported scan CSV, voice edits to quantity/condition/printing/storage location, spoken confirmation only for ambiguity, undo, and reviewed CSV export. Tools: find candidate record, set field, split lot, assign location, undo, export. No autonomous pricing, publishing, or condition grading; those are separate research problems.

**Data-access constraint:** TCGplayer's getting-started page currently says it is not granting new API access. A September 15, 2026 announcement also says existing access is being reviewed and some users face changes. CSV-first avoids making this capstone depend on receiving marketplace credentials. [API access notice](https://docs.tcgplayer.com/docs/getting-started), [September API program update](https://seller.tcgplayer.com/blog/building-a-more-scalable-and-secure-api-program-at-tcgplayer)

**Hardest problem:** Correctly binding “that one,” “the previous two,” and corrections to individual physical cards. Maintain an explicit recent-item queue and inspectable history.

**Evaluation:** Same 50–100 cards using existing scan workflow versus voice-assisted correction; compare cards/minute, wrong-printing errors, correction time, and total hand-to-keyboard switches. Benchmark against existing batch defaults, which may already be faster than speech.

## 2. Voice operations desk for local fighting-game tournaments

**Interaction:** “Report table three: Alex beat Jordan two–one. Who is waiting for a station?”

**What exists:** start.gg has documented GraphQL queries for entrants and a mutation for reporting bracket results, including game-level information. Its developer portal also showcases an offline-first reporting client. Voice is therefore an interaction experiment around an existing operations system, not a new bracket platform. [Report Set API](https://developer.start.gg/docs/examples/mutations/report-set/), [start.gg developer portal](https://developer.start.gg/)

**Why voice:** An organizer can keep moving around the venue while consulting a headset or phone; whether this beats taps in a loud room is the key question.

**Four-to-six-week MVP:** One organizer, one game, one test bracket. Read pending matches; resolve spoken aliases against event entrants; stage a result; read back players and score; explicitly commit; maintain a local pending queue. Confirm API permissions and station data coverage before promising automatic station assignment. Do not build all tournament-management features.

**Hardest problem:** Gamer-tag recognition, venue noise, duplicate names, stale bracket state, and retransmission without duplicate or conflicting reports.

**Evaluation:** Simulated 16-player event with background noise; wrong-match reports, successful reports/minute, correction latency, and recovery after loss of connectivity. Compare against the existing mobile UI.

## 3. Voice producer for hands-busy niche livestreams

**Interaction:** A miniature painter says, “Show the overhead, crop in a little, lower the music while I explain this, and mark this as the dry-brushing section.”

**What exists:** OBS includes a WebSocket endpoint for external control. Streamer.bot already provides voice-command triggers using configurable phrases. A project consisting only of “say a phrase to change a scene” has a strong existing baseline. [OBS developer guide](https://obsproject.com/kb/developer-guide), [Streamer.bot voice control](https://docs.streamer.bot/guide/core/voice-control)

**Why voice:** The presenter’s hands are occupied and their attention is on the craft. Use a dedicated command cue or push-to-talk pedal to avoid interpreting audience-facing narration as instructions.

**Four-week MVP:** One creator type; three scenes; bounded camera crop; music level; recording markers in a local sidecar file; scene-state readback; undo. The agent interprets a compound request into validated OBS calls. Local command acknowledgement goes to headphones, not the broadcast mix.

**Hardest problem:** Distinguishing an intentional instruction from ordinary speech, and doing the right thing quickly without an accidental live change.

**Evaluation:** Complete a ten-minute craft demo with buttons/macros, Streamer.bot fixed phrases, and the agent. Compare interruptions, false activations, time to correct, action latency, and whether compound language actually reduces effort.

## 4. CATAN public-state announcer and game log

**Interaction:** “Blue builds a settlement at the coast by the six-wheat tile.” Then: “What changed since my last turn?”

**What exists:** CATAN Assistant already teaches the rules through voice output and animations. A generic narrated tutorial or rules chatbot is not a persuasive differentiation. [Official CATAN Assistant](https://www.catan.com/understand-catan/how-do-i-learn-catan)

**Why voice:** Keep the group focused on the physical board. There is also a possible accessibility direction for players who cannot easily inspect the shared board, but it requires co-design rather than assuming narration solves accessibility.

**Four-to-six-week MVP:** Base game only; manually initialized board with numbered intersections; explicitly declared public actions; deterministic public-state ledger; queries about board ownership, turn order, and recent actions. Add a camera later for reconciling visible pieces. No inferred secret hands or covert coaching.

**Hardest problem:** Multi-speaker overlap, jokes versus actions, spatial references, and forgotten declarations. If the bookkeeping becomes more work than the game, the project fails.

**Evaluation:** State agreement with a human observer, correction burden per turn, missed public events, and interruptions to the social experience. Compare voice-only logging to a simple shared keypad before adding computer vision.

## 5. Voice assistant for a human tabletop RPG game master

**Interaction:** “Goblin two takes seven damage; move to the next turn; remind me about the bridge when combat ends.”

**What exists:** Friends & Fables already offers an AI game master and automatic stat/note tracking. Foundry exposes combat state and turn-advancement methods, creating a route to a human-GM assistant rather than generating an entire replacement game master. Version-specific integration must be verified against the installed Foundry version; the linked combat reference is v11. [Friends & Fables](https://fables.gg/about), [Foundry combat API](https://foundryvtt.com/api/v11/classes/client.Combat.html)

**Why voice:** The GM is simultaneously narrating, listening, and operating the virtual tabletop. Start with deliberate commands rather than recording every conversation.

**Four-to-six-week MVP:** One game system and Foundry version; initiative queries, next-turn controls, GM-approved health changes, private reminders, and reversible journal notes. Explicitly separate GM-only data from player-visible responses.

**Hardest problem:** Character-name disambiguation and accidental disclosure of GM secrets. The model should propose structured updates; the game engine remains authoritative for state and rules.

**Evaluation:** Compare a fixed encounter with the ordinary interface against voice support; count incorrect state updates, corrections, and lost narration time. Include deliberate near-miss commands and player chatter.

## Cross-project technical lesson

The valuable capstone question is not whether speech can invoke a tool. It is whether a narrow voice workflow reduces effort while handling ambiguity, interruptions, corrections, and real state changes. Use deterministic tools with typed arguments, an action log, read-after-write checks, and undo wherever the domain allows it. A generic coding-agent harness is optional; these first prototypes can be smaller, faster, and easier to evaluate with a domain-specific tool set.

For all five, test against the simplest existing interaction. A fluent voice demo is not evidence that the product improves the task.
