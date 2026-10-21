#!/usr/bin/env python3
"""Render a design-crit crit.json into a single crit.html.

Usage: python3 render.py <path/to/crit.json> [-o crit.html] [--inline]

Stdlib only. Every string from the JSON is treated as untrusted and escaped.
Format contract: ../references/crit-format.md
"""
import argparse
import base64
import html
import json
import os
import re
import struct
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(HERE, "..", "assets", "crit.css")

REQUIRED_KEYS = ("target", "date", "screens", "notes")
TIERS = (("must", "Must fix"), ("should", "Should fix"), ("polish", "Polish"))
EVIDENCE = {
    "S": "Strong evidence",
    "M": "Moderate evidence",
    "W": "Weak evidence",
    "rule": "Standard or platform rule",
}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".gif": "image/gif"}
INLINE_LIMIT = 15 * 1024 * 1024


def warn(msg):
    print("warning: " + msg, file=sys.stderr)


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def anchor_id(value):
    return re.sub(r"[^A-Za-z0-9_-]", "-", str(value))


def num(value, default=0.0):
    try:
        f = float(value)
    except (TypeError, ValueError):
        return default
    return f if f == f else default  # NaN guard


def pct(value):
    return ("%.3f" % value).rstrip("0").rstrip(".") + "%"


def safe_url(url):
    if not isinstance(url, str):
        return None
    try:
        parts = urllib.parse.urlsplit(url.strip())
    except ValueError:
        return None
    if parts.scheme.lower() in ("http", "https") and parts.netloc:
        return url.strip()
    return None


def png_size(path):
    """Natural size from a PNG's IHDR chunk, or None."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
    except OSError:
        return None
    if len(head) == 24 and head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
        return struct.unpack(">II", head[16:24])
    return None


def pad_for(width, height, scale=None):
    """About 24 CSS px of context: uses the screen's scale, else guesses it."""
    if isinstance(scale, (int, float)) and 0 < scale <= 4:
        return round(24 * scale)
    if width >= 2000:
        dpr = 2
    elif height > width:
        dpr = 3 if width >= 1000 else 2 if width >= 700 else 1
    else:
        dpr = 1
    return 24 * dpr


class Images:
    """One CSS class per unique image so --inline embeds each file once."""

    def __init__(self, base, inline):
        self.base = base
        self.inline = inline
        self.items = {}
        self.missing_warned = set()

    def get(self, rel):
        rel = "" if rel is None else str(rel)
        if rel in self.items:
            return self.items[rel]
        full = os.path.normpath(os.path.join(self.base, rel)) if rel else ""
        exists = bool(rel) and os.path.isfile(full)
        item = {"rel": rel, "exists": exists, "cls": "img-%d" % len(self.items),
                "size": png_size(full) if exists else None, "url": None}
        if exists:
            if self.inline:
                mime = MIME.get(os.path.splitext(full)[1].lower(), "application/octet-stream")
                with open(full, "rb") as fh:
                    item["url"] = "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))
            else:
                item["url"] = urllib.parse.quote(rel.replace(os.sep, "/"), safe="/._-~")
        elif rel not in self.missing_warned:
            self.missing_warned.add(rel)
            warn("missing screenshot: %s" % (rel or "(no path)"))
        self.items[rel] = item
        return item

    def css(self):
        return "\n".join('.%s{background-image:url("%s")}' % (i["cls"], i["url"])
                         for i in self.items.values() if i["exists"])


def clamp_region(region, width, height):
    if not isinstance(region, dict):
        return None
    x = min(max(num(region.get("x")), 0), width - 1)
    y = min(max(num(region.get("y")), 0), height - 1)
    w = min(max(num(region.get("w")), 1), width - x)
    h = min(max(num(region.get("h")), 1), height - y)
    return x, y, w, h


def missing_box(rel, ratio=None):
    style = ' style="aspect-ratio:%s"' % ratio if ratio else ""
    return '<div class="missing" role="img"%s><span>missing screenshot: %s</span></div>' % (
        style, esc(rel or "(no path)"))


def view(img, width, height, region=None, tier=None, label="", marker=None, cap=480, scale=None):
    """A cropped (or full) view of an image as a CSS-scaled background.

    region is in image pixels; the view shows it plus ~24px-equivalent padding,
    outlined, with an optional numbered marker at its top-left corner.
    """
    if not img["exists"]:
        return missing_box(img["rel"])
    if region:
        x, y, w, h = region
        pad = pad_for(width, height, scale)
        cx, cy = max(0, x - pad), max(0, y - pad)
        cw, ch = min(width, x + w + pad) - cx, min(height, y + h + pad) - cy
    else:
        cx, cy, cw, ch = 0, 0, width, height
    pos_x = cx / (width - cw) * 100 if width > cw else 0
    pos_y = cy / (height - ch) * 100 if height > ch else 0
    cwi, chi = int(round(cw)), int(round(ch))
    out = ['<div class="crop" style="aspect-ratio:%d/%d;width:min(100%%,calc(%dpx*%d/%d))">'
           % (cwi, chi, cap, cwi, chi),
           '<div class="shot %s" role="img" aria-label="%s" style="background-size:%s auto;'
           'background-position:%s %s"></div>'
           % (img["cls"], esc(label), pct(width / cw * 100), pct(pos_x), pct(pos_y))]
    if region and tier:
        out.append('<span class="region region-%s" style="left:%s;top:%s;width:%s;height:%s"></span>'
                   % (tier, pct((x - cx) / cw * 100), pct((y - cy) / ch * 100),
                      pct(w / cw * 100), pct(h / ch * 100)))
        if marker is not None:
            out.append('<span class="marker marker-%s" aria-hidden="true" style="left:clamp(14px,%s,'
                       'calc(100%% - 14px));top:clamp(14px,%s,calc(100%% - 14px))">%s</span>'
                       % (tier, pct((x - cx) / cw * 100), pct((y - cy) / ch * 100), esc(marker)))
    out.append("</div>")
    return "".join(out)


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        fail("no such file: %s" % path)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail("%s is not valid JSON: %s" % (path, exc))
    if not isinstance(data, dict):
        fail("%s must contain a JSON object" % path)
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        fail("%s is missing required keys: %s (see references/crit-format.md)"
             % (path, ", ".join(missing)))
    for key in ("screens", "notes"):
        if not isinstance(data[key], list):
            fail("'%s' must be a list" % key)
    return data


def as_list(value):
    return value if isinstance(value, list) else []


def render(data, base, inline):
    images = Images(base, inline)
    screens = {}
    for s in as_list(data.get("screens")):
        if not isinstance(s, dict):
            continue
        img = images.get(s.get("image"))
        w, h = num(s.get("width")), num(s.get("height"))
        if (w <= 0 or h <= 0) and img["size"]:
            w, h = img["size"]
        if w <= 0 or h <= 0:
            w, h = 1000, 1000
            if img["exists"]:
                warn("screen %s has no usable width/height" % s.get("id"))
        screens[str(s.get("id"))] = {"id": s.get("id"), "label": s.get("label") or s.get("id"),
                                     "img": img, "w": w, "h": h, "scale": s.get("scale")}

    notes = []
    for n in as_list(data.get("notes")):
        if not isinstance(n, dict):
            continue
        tier = n.get("tier") if n.get("tier") in ("must", "should", "polish") else "polish"
        if tier != n.get("tier"):
            warn("note %s has unknown tier %r, shown under Polish" % (n.get("id"), n.get("tier")))
        scr = screens.get(str(n.get("screen")))
        region = clamp_region(n.get("region"), scr["w"], scr["h"]) if scr else None
        if scr is None:
            warn("note %s refers to unknown screen %r" % (n.get("id"), n.get("screen")))
        elif region is None:
            warn("note %s has no region" % n.get("id"))
        notes.append({"n": n, "tier": tier, "scr": scr, "region": region,
                      "aid": anchor_id(n.get("id"))})
    known_ids = {str(x["n"].get("id")) for x in notes}

    parts = []
    add = parts.append

    # 1. Header
    degraded = data.get("degraded")
    if degraded:
        add('<div class="degraded" role="note"><strong>Degraded run.</strong> %s</div>' % esc(degraded))
    add('<header class="head">')
    add('<h1>%s</h1>' % esc(data.get("target")))
    meta = [("Date", data.get("date")), ("Effort", data.get("effort")),
            ("Surface", data.get("surface")), ("Method", data.get("method"))]
    add('<dl class="meta">%s</dl>' % "".join(
        '<div><dt>%s</dt><dd>%s</dd></div>' % (k, esc(v)) for k, v in meta if v))
    cov = data.get("coverage") if isinstance(data.get("coverage"), dict) else {}
    captured, not_captured = as_list(cov.get("captured")), as_list(cov.get("not_captured"))
    if captured or not_captured:
        add('<p class="coverage"><span class="label">Captured</span> %s'
            '<span class="sep" aria-hidden="true">·</span>'
            '<span class="label">Not captured</span> %s</p>'
            % (esc(", ".join(map(str, captured))) or "nothing",
               esc(", ".join(map(str, not_captured))) or "nothing"))
    counts = {t: sum(1 for x in notes if x["tier"] == t) for t, _ in TIERS}
    add('<p class="summary">%d %s: %s.</p>' % (
        len(notes), "note" if len(notes) == 1 else "notes",
        ", ".join("%d %s" % (counts[t], name.lower()) for t, name in TIERS)))
    if data.get("brief"):
        src = data.get("brief_source")
        src_html = ('<span class="brief-src">Inferred: no product docs were found.</span>'
                    if not src or str(src).strip().lower() == "inferred"
                    else '<span class="brief-src">From <code>%s</code></span>' % esc(src))
        add('<div class="brief"><h2>Brief</h2><p>%s</p>%s</div>' % (esc(data["brief"]), src_html))
    add('</header>')

    # 2. Direction
    if data.get("direction"):
        add('<section class="direction" aria-label="Direction"><h2>Direction</h2><p>%s</p></section>'
            % esc(data["direction"]))

    # 3. What's working
    working = [w for w in as_list(data.get("working")) if isinstance(w, dict)]
    if working:
        add('<section class="block"><h2>What&#8217;s working</h2><ul class="working">')
        for w in working:
            scr = screens.get(str(w.get("screen")))
            media = ""
            if scr and isinstance(w.get("region"), dict):
                media = '<div class="working-media">%s</div>' % view(
                    scr["img"], scr["w"], scr["h"], clamp_region(w["region"], scr["w"], scr["h"]),
                    label="%s, %s" % (scr["label"], w.get("title") or ""), cap=200, scale=scr["scale"])
            add('<li class="%s">%s<div><h3>%s</h3><p>%s</p></div></li>' % (
                "has-media" if media else "", media, esc(w.get("title")), esc(w.get("why"))))
        add('</ul></section>')

    # 4. Notes by tier
    marker_ids = {x["aid"] for x in notes if x["scr"] and x["region"] and x["scr"]["img"]["exists"]}
    for tier, name in TIERS:
        group = [x for x in notes if x["tier"] == tier]
        if not group:
            continue
        add('<section class="block tier"><h2><span class="tier-label tier-%s">%s</span> '
            '<span class="count">%d</span></h2>' % (tier, name, len(group)))
        for x in group:
            add(note_card(x, images, marker_ids))
        add('</section>')

    # 5. Screens
    shown = [s for s in screens.values()]
    if shown:
        add('<section class="block"><h2>Screens</h2>')
        for s in shown:
            add(screen_figure(s, [x for x in notes if x["scr"] is s and x["region"]]))
        add('</section>')

    # 6. Since last run
    prev = data.get("previous")
    if isinstance(prev, dict):
        bits = []
        for key in ("fixed", "partial", "open"):
            ids = as_list(prev.get(key))
            label = "%d %s" % (len(ids), key)
            if ids:
                label += ' <span class="ids">(%s)</span>' % esc(", ".join("#%s" % i for i in ids))
            bits.append(label)
        add('<section class="block since"><h2>Since last run</h2><p>%s%s.</p></section>' % (
            ("Compared with %s: " % esc(prev["date"])) if prev.get("date") else "", ", ".join(bits)))

    # 7. Questions
    questions = [q for q in as_list(data.get("questions")) if isinstance(q, dict)]
    if questions:
        add('<section class="block"><h2>Questions</h2><ol class="questions">')
        for q in questions:
            ref = ""
            if q.get("note") is not None:
                nid = str(q["note"])
                ref = (' <a class="ref" href="#note-%s">Note %s</a>' % (anchor_id(nid), esc(nid))
                       if nid in known_ids else ' <span class="ref">Note %s</span>' % esc(nid))
            opts = "".join("<li>%s</li>" % esc(o) for o in as_list(q.get("options")))
            add('<li><p>%s%s</p>%s</li>' % (esc(q.get("q")), ref,
                                           '<ul class="options">%s</ul>' % opts if opts else ""))
        add('</ol></section>')

    add('<footer class="foot">Rendered by design-crit from crit.json version %s.</footer>'
        % esc(data.get("version", "?")))

    with open(CSS_PATH, "r", encoding="utf-8") as fh:
        css = fh.read()
    title = "Design crit: %s" % (data.get("target") or "")
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="color-scheme" content="light dark">\n'
            '<title>%s</title>\n<style>\n%s\n%s\n</style>\n</head>\n<body>\n<main class="page">\n%s\n'
            '</main>\n</body>\n</html>\n') % (esc(title), css, images.css(), "\n".join(parts))


def note_card(x, images, marker_ids):
    n, tier, scr, region, aid = x["n"], x["tier"], x["scr"], x["region"], x["aid"]
    nid = esc(n.get("id"))
    has_marker = aid in marker_ids
    label = "%s, note %s" % (scr["label"] if scr else "", n.get("id"))
    if scr and region:
        before = view(scr["img"], scr["w"], scr["h"], region, tier, label, n.get("id"), scale=scr["scale"])
    elif scr:
        before = view(scr["img"], scr["w"], scr["h"], label=label, cap=320)
    else:
        before = missing_box(n.get("screen"))
    after_rel = n.get("after_image")
    if after_rel:
        aimg = images.get(after_rel)
        if scr and aimg["exists"]:
            size = aimg["size"]
            if size and region and abs(size[0] - scr["w"]) < 1 and abs(size[1] - scr["h"]) < 1:
                after = view(aimg, scr["w"], scr["h"], region, tier, label + " after", n.get("id"), scale=scr["scale"])
            elif size:
                after = view(aimg, size[0], size[1], label=label + " after", cap=320)
            else:
                after = view(aimg, scr["w"], scr["h"], label=label + " after", cap=320)
        else:
            after = missing_box(after_rel)
        media = ('<div class="note-media pair"><figure><figcaption>Before</figcaption>%s</figure>'
                 '<figure><figcaption>After</figcaption>%s</figure></div>' % (before, after))
    else:
        media = '<div class="note-media">%s</div>' % before

    num_html = ('<a class="num marker-%s" href="#marker-%s" aria-label="Note %s, show on screen">%s</a>'
                % (tier, aid, nid, nid) if has_marker
                else '<span class="num marker-%s">%s</span>' % (tier, nid))
    fields = "".join('<dt>%s</dt><dd>%s</dd>' % (k, esc(n.get(f)))
                     for k, f in (("What", "what"), ("Effect", "effect"), ("Fix", "fix")) if n.get(f))

    pr = n.get("principle") if isinstance(n.get("principle"), dict) else {}
    pname = pr.get("name") or pr.get("rule_id") or "Principle"
    url = safe_url(pr.get("url"))
    if url:
        plink = '<a href="%s" rel="noopener noreferrer">%s</a>' % (esc(url), esc(pname))
    else:
        plink = '<span>%s</span>' % esc(pname)
        if pr.get("url"):
            plink += ' <span class="raw-url">%s</span>' % esc(pr.get("url"))
    ev = pr.get("evidence")
    ev_html = ('<span class="ev" title="%s"><span class="vh">Evidence: </span>%s</span>'
               % (esc(EVIDENCE.get(str(ev), "Evidence")), esc(ev)) if ev else "")
    src_html = '<span class="src">%s</span>' % esc(pr.get("source")) if pr.get("source") else ""
    rule_html = '<code>%s</code>' % esc(pr.get("rule_id")) if pr.get("rule_id") else ""
    principle = '<p class="principle">%s</p>' % " ".join(
        p for p in (plink, ev_html, src_html, rule_html) if p)

    measured = ('<p class="measured"><span class="label">Measured</span> <code>%s</code></p>'
                % esc(n.get("measured")) if n.get("measured") else "")
    verdict = n.get("verdict")
    verdict_html = ('<span class="plausible">Plausible, not confirmed</span>' if verdict == "plausible"
                    else "Confirmed" if verdict == "confirmed" else esc(verdict))
    meta_bits = [b for b in (esc(n.get("specialist")), verdict_html) if b]
    if has_marker:
        meta_bits.append('<a href="#marker-%s">Show on %s</a>' % (aid, esc(scr["label"])))
    meta = '<p class="note-meta">%s</p>' % '<span class="sep" aria-hidden="true">·</span>'.join(meta_bits)

    cls = "note has-pair" if after_rel else "note"
    return ('<article class="%s" id="note-%s">%s<div class="note-body"><h3>%s<span class="title">%s</span></h3>'
            '<dl class="fields">%s</dl>%s%s%s</div></article>'
            % (cls, aid, media, num_html, esc(n.get("title")), fields, principle, measured, meta))


def screen_figure(s, notes):
    img = s["img"]
    portrait = s["h"] > s["w"]
    cap = '<figcaption>%s <span class="dims">%d × %d</span></figcaption>' % (
        esc(s["label"]), int(s["w"]), int(s["h"]))
    if not img["exists"]:
        return '<figure class="screen">%s%s</figure>' % (
            missing_box(img["rel"], "%d/%d" % (int(s["w"]), int(s["h"]))), cap)
    markers = []
    for x in notes:
        rx, ry, _, _ = x["region"]
        n = x["n"]
        markers.append('<a class="marker marker-%s" id="marker-%s" href="#note-%s" style="left:clamp(12px,%s,calc(100%% - 12px));top:clamp(12px,%s,calc(100%% - 12px))" '
                       'aria-label="Note %s: %s">%s</a>'
                       % (x["tier"], x["aid"], x["aid"], pct(rx / s["w"] * 100), pct(ry / s["h"] * 100),
                          esc(n.get("id")), esc(n.get("title")), esc(n.get("id"))))
    return ('<figure class="screen%s"><div class="frame" style="aspect-ratio:%d/%d">'
            '<div class="shot %s" role="img" aria-label="%s" style="background-size:100%% auto"></div>%s</div>%s</figure>'
            % (" portrait" if portrait else "", int(s["w"]), int(s["h"]), img["cls"],
               esc(s["label"]), "".join(markers), cap))


def main():
    ap = argparse.ArgumentParser(description="Render crit.json into crit.html.")
    ap.add_argument("crit", help="path to crit.json")
    ap.add_argument("-o", "--output", help="output path (default: crit.html next to crit.json)")
    ap.add_argument("--inline", action="store_true", help="embed images as base64 data URIs")
    args = ap.parse_args()

    crit_path = os.path.abspath(args.crit)
    data = load(crit_path)
    base = os.path.dirname(crit_path)
    out_path = os.path.abspath(args.output) if args.output else os.path.join(base, "crit.html")
    if not os.path.isfile(CSS_PATH):
        fail("stylesheet not found: %s" % CSS_PATH)

    doc = render(data, base, args.inline).encode("utf-8")
    with open(out_path, "wb") as fh:
        fh.write(doc)
    if args.inline and len(doc) > INLINE_LIMIT:
        warn("%s is %.1f MB, over the 15 MB limit for a published page"
             % (out_path, len(doc) / 1024 / 1024))
    if not args.inline and args.output and os.path.dirname(out_path) != base:
        warn("output is not next to crit.json; relative image paths may not resolve")
    print(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
