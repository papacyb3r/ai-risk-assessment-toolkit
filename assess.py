#!/usr/bin/env python3
"""Score an AI governance self-assessment against NIST AI RMF functions.

Usage: python assess.py ai_risk_questions.csv sample_answers.csv [report.md]
Answers: yes = 1.0, partial = 0.5, no = 0.0 (weighted by question weight).
"""
import csv
import sys
from collections import defaultdict

POINTS = {"yes": 1.0, "partial": 0.5, "no": 0.0}


def rating(pct):
    if pct >= 80:
        return "Strong"
    if pct >= 60:
        return "Developing"
    if pct >= 40:
        return "Weak"
    return "Critical gap"


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    questions = load(sys.argv[1])
    answers = {r["id"]: r["answer"].strip().lower() for r in load(sys.argv[2])}
    missing = [q["id"] for q in questions if q["id"] not in answers]
    if missing:
        sys.exit("Missing answers for: " + ", ".join(missing))
    bad = [k for k, v in answers.items() if v not in POINTS]
    if bad:
        sys.exit("Answer must be yes, partial or no. Check: " + ", ".join(bad))

    earned, possible = defaultdict(float), defaultdict(float)
    gaps = []
    for q in questions:
        w = int(q["weight"])
        a = answers[q["id"]]
        fn = q["nist_ai_rmf"]
        earned[fn] += POINTS[a] * w
        possible[fn] += w
        if a != "yes":
            gaps.append((w, a, q))

    total_e, total_p = sum(earned.values()), sum(possible.values())
    overall = 100 * total_e / total_p
    out = ["# AI Governance Self-Assessment", "",
           f"**Overall maturity:** {overall:.0f}% ({rating(overall)})", "",
           "## Score by NIST AI RMF function", "",
           "| Function | Score | Rating |", "|---|---|---|"]
    for fn in ("GOVERN", "MAP", "MEASURE", "MANAGE"):
        if possible[fn]:
            p = 100 * earned[fn] / possible[fn]
            out.append(f"| {fn} | {p:.0f}% | {rating(p)} |")
    out += ["", "## Priority gaps (highest weight first)", "",
            "| ID | Status | Gap | ISO/IEC 42001 Annex A area | OWASP LLM |",
            "|---|---|---|---|---|"]
    for w, a, q in sorted(gaps, key=lambda g: (-g[0], g[1] != "no", g[2]["id"])):
        out.append(f"| {q['id']} | {a} | {q['question']} | "
                   f"{q['iso_42001_annex_a']} | {q['owasp_llm']} |")
    out += ["", "_Indicative self-assessment. Not a certification audit._"]
    text = "\n".join(out) + "\n"
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ == "__main__":
    main()
