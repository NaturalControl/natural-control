# Screen readers and AI accessibility: research brief

Checked September 14, 2026. Product documentation establishes availability and advertised capabilities; research results below establish performance only within the stated study. Recommendations are synthesis, not proven outcomes.

## What the existing tools already do

There is no universally best screen reader. Platform, existing expertise, applications, braille needs and budget determine fit. Build alongside the tools participants already use.

| Tool | Useful baseline | Product boundary |
|---|---|---|
| NVDA | Free, open-source Windows screen reader supporting Windows and third-party apps. Strong candidate for an extensible desktop research baseline. | Screen-reader navigation and output; do not assume an autonomous agent is included. [NV Access](https://www.nvaccess.org/product/nvda-/) |
| JAWS | Commercial Windows screen reader; speech/braille, browser navigation, forms, OCR, Office and browser support. | Picture Smart AI adds visual descriptions. [JAWS](https://www.freedomscientific.com/products/software/jaws/?frame=0) |
| Apple VoiceOver | Integrated screen reading with gestures/keyboard, speech, braille, adjustable verbosity and speed. | These controls already allow selective navigation; it does not simply read every pixel sequentially. [Apple features](https://www.apple.com/accessibility/features/) |
| Android TalkBack | Android screen reader with navigation, braille and keyboard support. TalkBack 16 adds screen summaries and Gemini follow-up questions by voice or typing. | Documentation lists the new screen/question features as English-only. Q&A is not equivalent to arbitrary autonomous app control. [TalkBack 16](https://support.google.com/accessibility/android/answer/16294093?hl=en) |

**The "works even when developers omit accessibility" direction already has shipped precedents.** VoiceOver Recognition recognizes images, text and interface controls where alt text/labels are absent. It can announce inferred controls as uncertain. Apple's research explains that Screen Recognition is an on-device model deployed in iOS 14, using computer vision, grouping and clickable-element inference. This is relevant precedent for locally repairing a missing semantic interface, not evidence that every app is solved. [Apple support](https://support.apple.com/en-us/111799), [Apple ML research](https://machinelearning.apple.com/research/mobile-applications-accessible).

**Local AI is already real in accessibility.** Google documents Gemini Nano running automatic image descriptions on eligible devices offline, with a larger Gemini Flash path for additional details. Device eligibility and feature-specific cloud use matter: “local” need not describe the whole assistant. [Android developer account](https://android-developers.googleblog.com/2024/09/talkback-uses-gemini-nano-to-increase-low-vision-accessibility.html).

## AI visual assistance is deployed; dependable action is the frontier

- **JAWS Picture Smart AI:** Describes an image, focused control, screen, window, clipboard or context-selected visual. Uses services including OpenAI and Anthropic. Vendor documentation says submitted images/prompts/answers are neither stored nor used for training by its partners. This is a strong existing visual-description baseline. [Picture Smart AI](https://www.freedomscientific.com/training/jaws/picture-smart-ai/).
- **Be My Eyes / Be My AI:** Free personal-use desktop offering now lists Windows **and macOS**. Describes screens, files, clipboard images and webcam pictures; users ask follow-up questions. July 2026 help documents internet dependence and one image per desktop chat. This is deployed, but those capabilities do not establish autonomous clicking, browsing or transaction execution. Older Windows-only descriptions are stale. [Desktop product](https://www.bemyeyes.com/be-my-eyes-for-desktop/), [July 2026 desktop help](https://support.bemyeyes.com/hc/en-us/articles/48284651305489-Using-Be-My-AI-on-desktop).
- **Seeing AI:** Microsoft's free mobile visual assistant supports reading text/documents, identifying products and currency, and scene descriptions. Its Android launch included richer generative descriptions and document Q&A, following iOS. This addresses task-specific visual information rather than generalized browser control. The founder is blind and explicitly describes community collaboration. [Microsoft launch and capabilities](https://blogs.microsoft.com/accessibility/seeing-ai-app-launches-on-android-including-new-and-updated-features-and-new-languages/).

## What users and experiments actually tell us

### Do not start from “blind people want screen readers gone”

WebAIM survey #10 had 1,539 responses in 2023–24, using an uncontrolled sample—not market-share measurement. Primary desktop tools: JAWS 40.5%, NVDA 37.7%, VoiceOver 9.7%; 71.6% used multiple desktop readers. When finding information on lengthy pages, 71.6% began with headings, versus 6.4% reading through the page. 85.9% expected better websites to improve accessibility more than better assistive technology. Leading barriers included CAPTCHA, unexpected interactive controls, unclear links/buttons and unexpected changes. This supports selective navigation and repair, and challenges the assumption that screen readers force everyone to consume filler. [Survey results](https://webaim.org/projects/screenreadersurvey10/).

Survey #11 is closed, but its official page currently says results are forthcoming. Do not label #10 statistics as 2026 data. [Survey #11 status](https://webaim.org/projects/screenreadersurvey11/).

### Morae: preserve decisions, not just task completion

UIST 2025 research is unusually close to this proposed project. A four-person BLV field study found arbitrary agent choices and poor awareness of actions. Morae pauses at ambiguous decisions and provides accessible preference input and feedback. Example: several equally cheap sparkling waters differ in flavor and ratings; “buy cheapest” does not authorize silently erasing those differences. A comparison with 10 BLV participants reported better preference alignment and task completion than baseline automation and Operator. This is a research prototype, not proof of unrestricted production reliability. The actionable lesson is to optimize **informed user control**, including what choices exist, rather than maximize silent automation. [Morae paper](https://www.cs.cmu.edu/~jbigham/pubs/pdfs/2025/morae-pausing-ui-agents.pdf).

### A11y-CUA: a capable agent can still be hard to collaborate with

CHI 2026 research compares human and agent trajectories across 60 everyday tasks. Its default agent succeeded at 78.3%; keyboard-only with assistive technology fell to 41.67%, magnification to 28.3%. The study shows a gap between mouse/vision-oriented agent behavior and how blind users navigate and monitor work. These are specific models/conditions, not a current universal agent score. Avoid saying “turning on any screen reader halves all agents' accuracy”: the keyboard-only action restriction matters. [A11y-CUA paper](https://arxiv.org/abs/2602.09310).

### ConWeb: direct evidence for voice-mediated information browsing

A May 2026 peer-reviewed study involved 30 blind/low-vision participants doing four information tasks on the Bari municipality website. Reported completion was 115/120 (about 96%) with its conversational assistant versus 96/120 (80%) with familiar assistive software. Participants valued summaries, repeat/back commands and loading feedback; speech recognition failures and delays caused frustration and disorientation. Scope is narrow: one website, information finding, mixed BLV participants and heterogeneous comparison software including ZoomText. It does not prove replacement of expert screen-reader use or safe transactional browsing. [ConWeb study](https://doi.org/10.1080/10447318.2026.2659951).

## Best project wedges — synthesis

1. **Intent-driven reading of real pages.** Browser extension: “What are the eligibility rules?”, “Read the exact sentence”, “What else is on this page?”, “Go back.” Use page text/structure as source, vision for inaccessible gaps, summaries linked to exact passages. Initially public information pages only. Differentiation: reliable answers with easy access to omitted context, not another screenshot describer.
2. **An assistant for getting unstuck.** User invokes help on an unlabeled control, broken menu, inaccessible document or confusing page transition. Explain current state, suggest or perform one bounded action, then return focus. Measure successful recovery and whether the person can continue independently.
3. **Guided forms in one domain.** Start with a small family of forms and synthetic data: explain required fields, gather answers conversationally, fill, read back the actual entered values and errors. User explicitly submits. This tests action grounding and verification without claiming universal browsing.
4. **Accessible agent supervision.** Make another agent's activity perceivable through concise spoken state changes, interruption, available choices, and independently inspectable results. Morae/A11y-CUA suggest this is a distinct unsolved product problem, beyond voice transcription.

For all four, voice should be the primary option without being mandatory. Preserve keyboard/text/braille access, rapid stop, adjustable speech speed, verbatim reading and a persistent action history. A summary must be expandable; “important” depends on the person's goal and preferences.

## Co-design and evaluation proposal

Recruit and pay 6–10 blind/low-vision collaborators with varied screen-reader experience, devices and onset of vision loss. Observe their own recently frustrating tasks before choosing a wedge. Include people who prefer braille, have additional disabilities, or cannot/will not speak in public. Collaborators should help choose tasks and success criteria, not only test a finished idea.

Compare **their usual workflow**, **usual workflow plus assistant**, and voice-only where desired. Track independently verified completion, time, uncorrected mistakes, requests for human help, recovery after failure, ability to explain what the agent did, and perceived control. Separately test recognition of exact dates/numbers and recall of omitted alternatives. Small formative studies guide a prototype; they do not establish population-wide benefit.

Recommended first experiment: a read-and-navigate browser companion with three commands—answer my question, read the source, show my options—tested on participants' own public-information tasks. Expand into writes only after users can understand, interrupt and verify its actions.
