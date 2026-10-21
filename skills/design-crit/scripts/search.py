#!/usr/bin/env python3
"""BM25 search over references/rules.csv (stdlib only)."""
import argparse, csv, json, math, re, sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "references" / "rules.csv"
K1, B = 1.5, 0.75


def tokenize(text):
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if len(t) > 1]


def doc_text(r):
    return " ".join([r["id"].replace("-", " "), r["category"], r["principle"],
                     r["test"], r["bad"], r["good"]])


def trunc(s, n=300):
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    p = argparse.ArgumentParser(description="Search design-crit rules.")
    p.add_argument("query")
    p.add_argument("-n", type=int, default=5)
    p.add_argument("--category")
    p.add_argument("--platform", choices=["web", "ios", "all"])
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if not CSV_PATH.is_file():
        print(f"rules.csv not found at {CSV_PATH}", file=sys.stderr)
        return 2
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if a.category:
        rows = [r for r in rows if r["category"] == a.category]
    if a.platform and a.platform != "all":
        rows = [r for r in rows if r["platform"] in (a.platform, "all")]

    q = set(tokenize(a.query))
    docs = [tokenize(doc_text(r)) for r in rows]
    N = len(docs)
    hits = []
    if N and q:
        avgdl = sum(len(d) for d in docs) / N or 1
        df = {t: sum(1 for d in docs if t in d) for t in q}
        for r, d in zip(rows, docs):
            score = 0.0
            for t in q:
                tf = d.count(t)
                if not tf:
                    continue
                idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                score += idf * tf * (K1 + 1) / (tf + K1 * (1 - B + B * len(d) / avgdl))
            if score > 0:
                hits.append((score, r))
        hits.sort(key=lambda x: -x[0])
        hits = hits[: a.n]

    if not hits:
        print("no matching rules")
        return 0
    if a.json:
        print(json.dumps([dict(r, score=round(s, 4)) for s, r in hits], indent=2))
        return 0
    for s, r in hits:
        print(f"[{r['id']}] {trunc(r['principle'])} — evidence: {r['evidence']} · {r['platform']} · default: {r['default_tier']}")
        print(f"  test: {trunc(r['test'])}")
        print(f"  source: {trunc(r['source'])} — {trunc(r['source_url'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
