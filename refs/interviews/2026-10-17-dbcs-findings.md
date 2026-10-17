# Findings: DBCS interview (October 17, 2026)

Source: [transcript](2026-10-17-dbcs-transcript.md). Participant: P1, a former special events coordinator at CNIB Deafblind Community Services (DBCS). P1 is not blind or deaf and reports what they saw working with clients. This is one proxy interview, so treat each finding as an observation to check with blind users, not as proof.

Each finding below keeps three things separate: what P1 said, what published sources say, and what we think it means for the project.

## 1. The people DBCS serves are mostly older adults with acquired loss

**What P1 said:** Clients were mostly older people newly diagnosed with acquired deafblindness, often on low or no income, using free government-funded services. Devices may be older rather than new MacBooks.

**Related research:** In the Canadian Longitudinal Study on Aging (ages 45 to 85), about 6% of adults had at least mild dual sensory loss, and about 20 to 24% had at least mild vision loss ([Mick et al., 2020](https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/EEAB27765E0BCA26AAD0C7AC56F048E0/S0714980820000070a.pdf/the-prevalence-of-hearing-vision-and-dual-sensory-loss-in-older-canadians-an-analysis-of-data-from-the-canadian-longitudinal-study-on-aging.pdf)); dual sensory loss rises with age and is much more common in home care and long-term care ([Guthrie et al., 2022](https://link.springer.com/doi/10.1186/s12877-022-03671-7); [Guthrie et al., 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4858206)). Ontario recognizes that deafblindness can be present from birth or acquired later in life ([Ontario](https://www.ontario.ca/page/services-people-who-are-deaf-or-deafblind)).

**What it means for us:** A large group who could benefit are older, newer to vision loss, and less confident with technology, not only experienced screen-reader users. Our Mac and recent-Chrome requirement may exclude people on older or cheaper devices.

## 2. Existing screen readers are hard to learn and read too much

**What P1 said:** Screen readers are complicated for this population and should be much simpler; people struggle to navigate them, and most software isn't built with blind or deaf users in mind. A screen reader can read the whole screen, including irrelevant things, instead of what is needed. P1's advice: keep it as simple as possible, "detailed but simple," detailed only in the ways that matter.

**Related research:** Screen-reader users mostly navigate by headings rather than reading pages in order (71.6% use headings first), and long-standing problems include links or buttons with unclear meaning, screens changing unexpectedly, complex forms, and too many links or navigation items ([WebAIM Screen Reader Survey #10](https://webaim.org/blog/screen-reader-user-survey-10-results/); summary by [University of Rochester](https://www.rochester.edu/digital-accessibility/?p=7992)).

**What it means for us:** This directly supports our main benefit (delegate instead of navigate) and the decision to speak only meaningful progress, not every element. It argues for a requirement that spoken output stays focused on the current task, with more detail on request.

## 3. Common tasks: scheduling, email, appointments; often done with a friend's help

**What P1 said:** All of the listed tasks matter, especially scheduling and writing emails. Booking appointments is something people often need a friend to do.

**Related research:** Blind users interviewed about voice assistants valued them most at home and described them as part of daily life ([Abdolrahmani, Kuber and Branham, ASSETS 2018](https://userpages.umbc.edu/~rkuber/pubs/assets2018.pdf)).

**What it means for us:** It confirms Gmail and Google Calendar as the right first scope, and suggests appointment booking on websites as a realistic test task.

## 4. Privacy: health and banking

**What P1 said:** People may not want to tell an AI about health problems (they might just want to book the appointment without explaining why), or give it banking information and ask it to move money.

**Related research:** In a survey of 155 visually impaired people, concern about sharing information through assistive services varied by the kind of information and who received it ([Akter et al., USENIX Security 2020](https://www.usenix.org/conference/usenixsecurity20/presentation/akter)). Blind users also avoid using voice assistants in public for privacy and social reasons ([Abdolrahmani et al., 2018](https://userpages.umbc.edu/~rkuber/pubs/assets2018.pdf)).

**What it means for us:** Users should be able to keep some topics or accounts off-limits, and the system should only use the details a task needs. It also supports keeping banking out of the initial scope.

## 5. Read-back before sending is good, but fixing a mistake means starting over

**What P1 said:** Siri reading back a message before sending is helpful, but if it got something wrong, you have to cancel the whole message. Reading back sentence by sentence, with confirmation that it heard you, would help.

**Related research:** In a study of blind people using speech input on phones, participants spent about 80% of their time finding and correcting errors, even though speech was about five times faster than the keyboard ([Azenkot and Lee, ASSETS 2013](https://unpaywall.org/10.1145%2F2513383.2513440)).

**What it means for us:** Read-back before consequential actions (FR.Sa.3) is supported, but correction has to be cheap: the user should be able to fix one part ("change the second sentence") without redoing the whole request.

## 6. Setup is done by family or intervenors, with limited time

**What P1 said:** Family usually sets up technology, but intervenors also help, and clients sometimes spend intervenor time on setup. Intervenor time is typically 1 to 1.5 hours a day, but varies; for some it is weekly.

**Related research:** DBCS intervenors help deafblind people get accurate information, communicate, and move around more independently, including at appointments and for errands; DBCS also runs a 24-hour emergency intervenor line ([DBCS Ottawa listing](https://champlainhealthline.ca/displayService.aspx?id=211322); [Toronto listing](https://www.torontocentralhealthline.ca/(X(1))/printService.aspx?id=225003)).

**What it means for us:** Intervenors are a real stakeholder and a likely setup helper. Because help may only come weekly, anything that breaks (an expired login, a disconnected account) must be fixable by voice, or the user loses independence until their next visit.

## 7. Use is mostly at home, in a quiet private place

**What P1 said:** People mostly use computers at home, for comfort, usually somewhere quiet and private, possibly on an older device.

**Related research:** Blind voice-assistant users describe home as their comfort zone and avoid using them on public transit ([Abdolrahmani et al., 2018](https://userpages.umbc.edu/~rkuber/pubs/assets2018.pdf)).

**What it means for us:** It supports our one-speaker assumption and lowers the risk of private content being overheard, though it doesn't remove it.

## 8. Voice-only output excludes deafblind users

**What P1 said:** Not asked directly, but P1's whole client group has combined vision and hearing loss, and intervenors communicate with them through ASL, hand-touch, and other methods.

**Related research:** DBCS intervenors use ASL, braille, large print, print on palm, two-hand manual, and voice-over ([DBCS listing](https://www.torontocentralhealthline.ca/(X(1))/printService.aspx?id=225003)). VoiceOver on Mac can send output to a refreshable braille display and accept braille input ([Apple](https://support.apple.com/guide/voiceover/vo15607/mac)).

**What it means for us:** Our hazard analysis assumes users can hear spoken output. That assumption excludes the population DBCS serves, so it should be stated as a limitation, with braille output through VoiceOver as a possible future extension.

## Gaps

- P1 deferred on how much spoken feedback is right, and the mistake-recovery question was skipped. Ask blind participants both.
- P1 said they could "probably" introduce two or three people. Follow up in writing.
- Confirm whether P1 is comfortable being named, and confirm "ASL" (transcribed as "ALS").

---

# Proposed updates (for team review)

## SRS

| Section | Proposed change | Evidence |
|---|---|---|
| G.2 Current situation | Add: screen readers are hard for older, newly diagnosed users to learn, read irrelevant content, and everyday tasks like appointments often need a friend's help. | Findings 1 to 3 |
| G.6 Limitations | Add: users who cannot hear spoken output (for example, many deafblind users) are not supported by the initial voice-only design; braille output through VoiceOver is a possible extension. | Finding 8 |
| G.7 Stakeholders | Add intervenors as a stakeholder (setup and support). Add the DBCS interview as a requirements source. | Finding 6 |
| G.8 User profiles | Make the "less experienced or recently blind user" profile more specific: often older, acquired loss, limited tech confidence, possibly an older device. | Finding 1 |
| E.4 Assumptions | Add "the user can hear spoken output," matching the hazard analysis, with this interview as the reason it is a limitation. | Finding 8 |
| S.2 new FR16 | The system shall let the user correct part of a read-back (for example, one sentence or one detail) by voice without restarting the request. | Finding 5 |
| S.2 new FR17 | The system shall let the user mark topics or accounts as off-limits; it shall not read, use, or act on them. | Finding 4 |
| S.2 new FR18 | Spoken updates and summaries shall include only information relevant to the current task, with more detail available on request. | Finding 2 |
| S.5 Prioritization | FR16 and FR18: must, before participant evaluation. FR17: should. | |
| P.7 Requirements process | Report the interview (date, participant role, method) and that FR16 to FR18, the G.8 change, and the intervenor stakeholder came from it. | All |

## Hazard analysis

| Section | Proposed change | Evidence |
|---|---|---|
| Critical assumptions | Keep "users can understand spoken output," but add the reason and limitation: this excludes many deafblind users, the group DBCS serves. | Finding 8 |
| Critical assumptions | Note that setup help may only be available weekly (intervenors), which is why recovery has to work by voice. | Finding 6 |
| FMEA, voice interface (H2-a) | Add to the recommended action: let the user correct one part of the read-back without restarting (links to new FR16). | Finding 5 |
| FMEA, new row under action tools and integrations | Sensitive health or banking details are sent to the AI provider when the task did not need them (loss: privacy leak). Action: off-limits topics and accounts; send only what the task needs. New FR.Sa.20 matching SRS FR17. | Finding 4 |
| FMEA, new row under accessible client | A broken state (expired login, disconnected account) can't be fixed without sighted help, so the user waits until their next intervenor visit (loss: loss of independence). Action: explain the problem and guide re-connection by voice. New FR.Sa.21. | Finding 6 |

These are proposals. The team decides which to adopt; none are in the documents yet.
