# V&V plan draft: November 2, 2026

Kevin requested a draft of all seven Plan subsections based on the Development Plan and the Section 2 planning discussion. Activities are planned, not completed.

- V&V is shared. Curtis is proposed as overall coordinator and Lucas as end-to-end testing coordinator, subject to team confirmation. Kevin covers CI and reliability; Aaron covers agent and tool integration.
- Track task completion, assistance, retries, corrections, and feedback without an arbitrary usability pass percentage. Critical safety tests for the evaluated configuration must all pass before participant use.
- Source conflict: the Development Plan has a provisional 80% completion target; SRS NFR2 uses the unset TARGET_COMPLETION constant and references that target. The team must reconcile these with the measurement approach before finalizing acceptance criteria. Neither source is changed by this draft.
- Use current SRS and Hazard Analysis control semantics when deriving tests. Their pause, reconnection, and approval rules supersede older Development Plan wording.
- Application CI and framework choices remain planned. Main currently has a LaTeX workflow, but no application implementation or test configuration.
- Store anonymized feedback and sanitized evidence in the repository; exclude participant identities, credentials, personal task data, and raw recordings.

## Assistance and review

OpenAI Codex assisted with drafting the Plan subsections and this note. Checks covered the Development Plan, SRS, Hazard Analysis, repository configuration, the earlier discussion, LaTeX compilation, preservation of content outside Plan, and the absence of em dashes in added content. No testing results or team approval are claimed. Review by another team member and completion of the document's existing disclosure appendix are pending.
