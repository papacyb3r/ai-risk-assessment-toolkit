# AI Risk Assessment Toolkit

A lightweight self-assessment for AI governance. It scores an organisation's AI controls against the four functions of the **NIST AI Risk Management Framework** (Govern, Map, Measure, Manage) and shows where each gap sits in **ISO/IEC 42001** (Annex A areas) and the **OWASP Top 10 for LLM Applications**.

Built for the question security and risk leaders are now being asked: *"Are we using AI safely, and can we prove it?"*

## What it does

1. Reads a question bank of 20 weighted controls (`ai_risk_questions.csv`).
2. Reads your answers (`yes`, `partial`, `no`).
3. Produces a Markdown report with an overall maturity score, a score per NIST AI RMF function, and a prioritised gap list.

## Quick start

```bash
python assess.py ai_risk_questions.csv sample_answers.csv report.md
```

No dependencies beyond Python 3. Copy `sample_answers.csv`, change the answers, and re-run.

## Sample output

| Function | Score | Rating |
|---|---|---|
| GOVERN | 50% | Weak |
| MAP | 27% | Critical gap |
| MEASURE | 14% | Critical gap |
| MANAGE | 33% | Critical gap |

The sample answers describe a fictional organisation. No real data is used.

## Question coverage

| Area | Examples |
|---|---|
| Governance | AI policy, accountable owners, legal requirements |
| Inventory and data | AI inventory, data classification, data poisoning |
| Third parties | Vendor due diligence, training on customer data |
| Shadow AI | Approved tools, detection of unapproved use |
| Security testing | Prompt injection, output handling, excessive agency |
| Operations | Logging, incident response, change control |

## Scoring

- `yes` = full weight, `partial` = half, `no` = zero. Weights run from 1 to 3 by impact.
- Ratings: 80%+ Strong, 60-79% Developing, 40-59% Weak, below 40% Critical gap.

## Limitations

- This is an **indicative self-assessment**, not an audit or certification.
- The mapping to ISO/IEC 42001 is at Annex A topic level and is a guide only. Check the standard text before using it in formal work.
- The question bank is a starting point. Adapt weights and wording to your context.

## Author

E.O. Acheampong. GRC, risk and cybersecurity compliance.
