# Milestone draft verification — September 23, 2026

## Artifacts

| Artifact | Pages | SHA-256 |
|---|---:|---|
| `pdfs/ProblemStatementAndGoals/ProblemStatement.pdf` | 5 | `44a9ecdceb16dece6a8b639af02b590ad55184ab0a192282b344fc4fa6f336ea` |
| `pdfs/DevelopmentPlan/DevelopmentPlan.pdf` | 11 | `badedbdd83ddb79913c1eeee6f663edb7019d1b6e1310a1751fa9be1bd3ea337` |

Both are **review drafts**, not submissions or evidence of team ratification.

## Checks actually performed

- Compiled both LaTeX sources with Tectonic 0.17.0 and BibTeX. Final builds completed without TeX/BibTeX warnings. Logs copied into ignored `refs/course/local/milestone-build-2026-09-23/`.
- Rendered and visually inspected all 16 final pages. Corrected detached table captions and awkward page breaks; checked text, tables, margins, pending labels and bibliography readability. No clipping/overlap observed.
- Extracted PDF text and checked missing-reference markers and inherited instruction strings. No `??`, `Date1`, `Student 1`, or template instruction comments in either output. Deliberate pending-human-input text remains.
- Inspected embedded PDF link destinations, including the escaped calendar address. Source facts were checked against the course outline, saved calendar, Avenue rubrics, TA source, and primary documentation listed in the research register. Documentation evidence is not runtime verification.
- Compared the documents to both Avenue rubrics and applicable repository checklists; gaps are explicit in the rubric map.
- Confirmed raw course PDF, Avenue material and TA JSON are gitignored. No raw meeting material is intended for publication.
- `git diff --check` passed. Build intermediates stayed outside tracked artifact directories.

## Reproduction

From the repository root, with Tectonic installed:

```sh
tectonic --outdir pdfs/ProblemStatementAndGoals docs/ProblemStatementAndGoals/ProblemStatement.tex
tectonic --outdir pdfs/DevelopmentPlan docs/DevelopmentPlan/DevelopmentPlan.tex
```

The existing GitHub workflow uses TeX Live/pdflatex. That remote workflow was not run by this local drafting task; the source retains standard LaTeX packages supported by its configured distribution. A different TeX engine may produce different pagination/hashes. Reinspect after human edits or a remote rebuild.

## Limits and handoff

Human proofreading and factual sign-off remain pending, as do reflections, assignments, meeting details, board URL, charter/license ratification, and proposed custom-document approval. Root LICENSE remains the inherited sample pending the recorded MIT proposal; that known template placeholder is outside the two PDF drafts. Product accessibility, independent completion, actual latency, safe cancellation, recruitment and user results have not been tested or claimed. These PDFs have selectable text but PDF tagging/VoiceOver reading order was not audited.

Initial preparation did not commit or publish. At Aaron’s subsequent request, the updated disclosures and draft package are being saved in separate local commits. No push, submission, or Pages publication is part of this step. Use the completion checklist before the September 28 deadline.

## Disclosure revision

Updated both disclosures with Aaron’s reported GPT-6 Astra Medium/High settings and his decision-making/review role. Rebuilt both PDFs without warnings and visually checked the changed disclosure/reflection/charter pages (PS page 4; DP pages 9–10). Other content is unchanged; page counts remain 5 and 11. Artifact hashes above reflect this revision.
