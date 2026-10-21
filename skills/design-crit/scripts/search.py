#!/usr/bin/env python3
"""BM25 search over references/rules.csv and references/biases.md (stdlib only)."""
import argparse, csv, json, math, re, sys
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "references"
CSV_PATH = REF / "rules.csv"
BIAS_PATH = REF / "biases.md"
K1, B = 1.5, 0.75


def tokenize(text):
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if len(t) > 1]


def doc_text(r):
    if r.get("kind") == "bias":
        return r["id"].replace("-", " ") + " " + r["text"]
    return " ".join([r["id"].replace("-", " "), r["category"], r["principle"],
                     r["test"], r["bad"], r["good"]])


def load_biases():
    """Parse biases.md '### `id` — grade' entries into records."""
    if not BIAS_PATH.is_file():
        return []
    recs, cur = [], None
    for line in BIAS_PATH.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"###\s+`([^`]+)`\s*[—-]\s*(.*)", line)
        if m:
            cur = {"kind": "bias", "id": m.group(1), "evidence": m.group(2).strip(),
                   "lines": [], "url": "", "what": ""}
            recs.append(cur)
            continue
        if line.startswith("## "):
            cur = None
        if cur is None:
            continue
        cur["lines"].append(line)
        if line.startswith("- Source:"):
            cur["url"] = line.split(":", 1)[1].strip()
        elif line.startswith("- What:") and not cur["what"]:
            cur["what"] = line[len("- What:"):].strip()
    for r in recs:
        r["text"] = "\n".join(r.pop("lines"))
    return recs


def trunc(s, n=300):
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    p = argparse.ArgumentParser(description="Search design-crit rules.")
    p.add_argument("query")
    p.add_argument("-n", type=int, default=5)
    p.add_argument("--category")
    p.add_argument("--platform", choices=["web", "ios", "all"])
    p.add_argument("--source", choices=["rules", "biases", "all"], default="all")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    rows = []
    if a.source in ("rules", "all"):
        if not CSV_PATH.is_file():
            print(f"rules.csv not found at {CSV_PATH}", file=sys.stderr)
            return 2
        with CSV_PATH.open(newline="", encoding="utf-8") as f:
            rows = [dict(r, kind="rule") for r in csv.DictReader(f)]
        if a.category:
            rows = [r for r in rows if r["category"] == a.category]
        if a.platform and a.platform != "all":
            rows = [r for r in rows if r["platform"] in (a.platform, "all")]
    if a.source in ("biases", "all") and not a.category:
        rows += load_biases()

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
        print("no matches")
        return 0
    if a.json:
        out = []
        for s, r in hits:
            d = dict(r, score=round(s, 4))
            if r["kind"] == "bias":
                d["source_url"] = d.pop("url")
            out.append(d)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    for s, r in hits:
        if r["kind"] == "bias":
            print(f"[{r['id']}] (bias, evidence {r['evidence']}) — {trunc(r['what'])}")
            print(f"  source: {r['url']}")
            continue
        print(f"[{r['id']}] {trunc(r['principle'])} — evidence: {r['evidence']} · {r['platform']} · default: {r['default_tier']}")
        print(f"  test: {trunc(r['test'])}")
        print(f"  source: {trunc(r['source'])} — {trunc(r['source_url'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
