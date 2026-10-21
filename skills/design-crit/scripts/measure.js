(() => {
  // design-crit / measure.js
  // Read-only in-page accessibility measurements. Single expression; returns a JSON string.
  // Run via a browser tool's "run JavaScript in page" or Playwright page.evaluate(src).
  // Rects are CSS px relative to the DOCUMENT (multiply by dpr for full-page screenshots).
  //
  // Approximations (documented on purpose):
  //  - Contrast: effective background = ancestors' background-color composited down to the first
  //    opaque one (white if none). ANY background-image on that path -> contrastUnknown. Elements
  //    painted underneath via positioning (video/img/canvas siblings) are NOT detected.
  //    Ancestor opacity is folded into the foreground alpha only.
  //  - Accessible name is a simplified accname: aria-labelledby > aria-label > (form controls:
  //    <label>/value/alt) > content (text, child img alt, child svg aria-label/<title>) > title >
  //    placeholder (placeholder-only is flagged, not trusted). CSS-hidden descendants are not
  //    excluded from content text; pseudo-element content is ignored.
  //  - Visibility ignores clipping by overflow/clip-path; rects <=1x1 are treated as visually hidden.
  const MAX_EL = 5000, LIMIT = 30;
  const doc = document, win = window;
  const sx = win.scrollX || win.pageXOffset || 0;
  const sy = win.scrollY || win.pageYOffset || 0;
  const INTERACTIVE = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=link], [role=checkbox], [role=switch], [role=tab], [role=menuitem], [tabindex]:not([tabindex="-1"])';
  const hasCV = typeof Element.prototype.checkVisibility === 'function';

  const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const clip = (s, n) => { s = norm(s); return s.length > n ? s.slice(0, n - 1) + '…' : s; };
  const rectOf = (r) => ({ x: Math.round(r.left + sx), y: Math.round(r.top + sy), w: Math.round(r.width), h: Math.round(r.height) });
  const parentOf = (el) => el.parentElement || (el.parentNode && el.parentNode.host) || null;
  const esc = (s) => (win.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/[^\w-]/g, '\\$&'));

  // ---------- visibility ----------
  const opCache = new Map();
  const effOpacity = (el) => {
    if (!el) return 1;
    let v = opCache.get(el);
    if (v !== undefined) return v;
    const o = parseFloat(getComputedStyle(el).opacity);
    v = (isNaN(o) ? 1 : o) * effOpacity(parentOf(el));
    opCache.set(el, v);
    return v;
  };
  const dnCache = new Map();
  const hiddenByDisplay = (el) => {
    if (!el) return false;
    let v = dnCache.get(el);
    if (v !== undefined) return v;
    v = getComputedStyle(el).display === 'none' || hiddenByDisplay(parentOf(el));
    dnCache.set(el, v);
    return v;
  };
  const isVisible = (el, r) => {
    if (!(r.width > 0 && r.height > 0)) return false;
    if (r.width <= 1 && r.height <= 1) return false;
    if (r.right + sx <= 0 || r.bottom + sy <= 0) return false;
    if (hasCV) {
      if (!el.checkVisibility({ checkVisibilityCSS: true, visibilityProperty: true })) return false;
    } else {
      if (hiddenByDisplay(el)) return false;
      const vis = getComputedStyle(el).visibility;
      if (vis === 'hidden' || vis === 'collapse') return false;
    }
    return effOpacity(el) > 0.05;
  };

  // ---------- colors ----------
  const colorCache = new Map();
  let ctx2d = null;
  const parseColor = (str) => {
    if (colorCache.has(str)) return colorCache.get(str);
    let out = null, m;
    const num = (s) => (s === 'none' ? 0 : parseFloat(s));
    const clamp = (v) => Math.max(0, Math.min(255, v));
    if ((m = /^rgba?\((.*)\)$/i.exec(str))) {
      const p = m[1].split(/[\s,\/]+/).filter(Boolean);
      const c = (s) => (s.endsWith('%') ? parseFloat(s) * 2.55 : num(s));
      const a = p[3] === undefined ? 1 : (p[3].endsWith('%') ? parseFloat(p[3]) / 100 : num(p[3]));
      const v = [c(p[0]), c(p[1]), c(p[2]), a];
      if (v.every((x) => isFinite(x))) out = [clamp(v[0]), clamp(v[1]), clamp(v[2]), Math.max(0, Math.min(1, a))];
    } else if ((m = /^color\(\s*srgb\s+(.*)\)$/i.exec(str))) {
      const p = m[1].split(/[\s\/]+/).filter(Boolean);
      const v = [num(p[0]) * 255, num(p[1]) * 255, num(p[2]) * 255, p[3] === undefined ? 1 : (p[3].endsWith('%') ? parseFloat(p[3]) / 100 : num(p[3]))];
      if (v.every((x) => isFinite(x))) out = [clamp(v[0]), clamp(v[1]), clamp(v[2]), Math.max(0, Math.min(1, v[3]))];
    }
    if (!out) {
      // oklch/lab/color(display-p3)/named etc.: rasterize on a detached 1x1 canvas (never inserted).
      try {
        if (!ctx2d) {
          const cv = doc.createElement('canvas');
          cv.width = cv.height = 1;
          ctx2d = cv.getContext('2d', { willReadFrequently: true });
        }
        ctx2d.clearRect(0, 0, 1, 1);
        ctx2d.fillStyle = '#000';
        ctx2d.fillStyle = str;
        ctx2d.fillRect(0, 0, 1, 1);
        const d = ctx2d.getImageData(0, 0, 1, 1).data;
        out = [d[0], d[1], d[2], d[3] / 255];
      } catch (e) { out = null; }
    }
    colorCache.set(str, out);
    return out;
  };
  const over = (fg, bg) => [0, 1, 2].map((i) => fg[i] * fg[3] + bg[i] * (1 - fg[3]));
  const lin = (c) => { const s = c / 255; return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const ratioOf = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const hex = (c) => '#' + c.map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');

  const bgCache = new Map();
  const effBg = (el) => {
    if (!el) return { rgb: [255, 255, 255], reason: null };
    const hit = bgCache.get(el);
    if (hit) return hit;
    const s = getComputedStyle(el);
    const c = parseColor(s.backgroundColor) || [0, 0, 0, 0];
    const img = s.backgroundImage;
    const hasImg = !!img && img !== 'none';
    let base;
    if (c[3] >= 0.999) base = { rgb: c.slice(0, 3), reason: null };
    else {
      const p = effBg(parentOf(el));
      base = c[3] > 0 ? { rgb: over(c, p.rgb), reason: p.reason } : p;
    }
    const res = {
      rgb: base.rgb,
      reason: base.reason || (hasImg ? (img.indexOf('gradient') >= 0 ? 'gradient' : 'image') + ' background on <' + el.localName + '>' : null),
    };
    bgCache.set(el, res);
    return res;
  };

  // ---------- skipping ----------
  const SKIP_TAGS = { script: 1, style: 1, noscript: 1, template: 1, svg: 1 };
  const skipCache = new Map();
  const skipped = (el) => {
    if (!el) return false;
    let v = skipCache.get(el);
    if (v !== undefined) return v;
    v = !!SKIP_TAGS[el.localName] || el.namespaceURI === 'http://www.w3.org/2000/svg' ||
      el.getAttribute('aria-hidden') === 'true' || skipped(parentOf(el));
    skipCache.set(el, v);
    return v;
  };
  const isDisabled = (el) => {
    try { return !!el.closest('[aria-disabled="true"], :disabled'); } catch (e) { return false; }
  };
  const directText = (el) => {
    let t = '';
    for (let n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3) t += n.nodeValue;
    return norm(t);
  };

  // ---------- accessible name ----------
  const contentName = (el, d) => {
    let out = '';
    for (let n = el.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3) { out += n.nodeValue; continue; }
      if (n.nodeType !== 1 || d > 6) continue;
      const ln = n.localName;
      if (ln === 'script' || ln === 'style' || ln === 'noscript') continue;
      if (n.getAttribute('aria-hidden') === 'true' || n.hasAttribute('hidden')) continue;
      const al = norm(n.getAttribute('aria-label'));
      if (al) { out += ' ' + al + ' '; continue; }
      if (ln === 'img') { out += ' ' + (n.getAttribute('alt') || '') + ' '; continue; }
      if (ln === 'svg') {
        const t = Array.prototype.find.call(n.children, (c) => c.localName === 'title');
        out += ' ' + (t ? t.textContent : (n.getAttribute('title') || '')) + ' ';
        continue;
      }
      out += contentName(n, d + 1);
    }
    return norm(out);
  };
  const BTN_INPUT = { button: 1, submit: 1, reset: 1, image: 1 };
  const accName = (el) => {
    const lb = el.getAttribute('aria-labelledby');
    if (lb) {
      const t = norm(lb.split(/\s+/).map((id) => doc.getElementById(id)).filter(Boolean)
        .map((n) => norm(n.getAttribute('aria-label')) || contentName(n, 0)).join(' '));
      if (t) return { name: t };
    }
    const al = norm(el.getAttribute('aria-label'));
    if (al) return { name: al };
    const ln = el.localName;
    if (ln === 'input' || ln === 'select' || ln === 'textarea') {
      const type = (el.getAttribute('type') || 'text').toLowerCase();
      if (ln === 'input' && BTN_INPUT[type]) {
        const v = norm(el.getAttribute('value')) || norm(el.getAttribute('alt')) ||
          (type === 'submit' ? 'Submit' : type === 'reset' ? 'Reset' : '');
        if (v) return { name: v };
      } else if (el.labels && el.labels.length) {
        const t = norm(Array.prototype.map.call(el.labels, (l) => contentName(l, 0)).join(' '));
        if (t) return { name: t };
      }
      const ti = norm(el.getAttribute('title'));
      if (ti) return { name: ti };
      const ph = norm(el.getAttribute('placeholder'));
      if (ph) return { name: ph, placeholderOnly: true };
      return { name: '' };
    }
    const c = contentName(el, 0);
    if (c) return { name: c };
    return { name: norm(el.getAttribute('title')) };
  };
  const roleOf = (el) => {
    const r = el.getAttribute('role');
    if (r) return r.split(/\s+/)[0];
    const t = el.localName;
    if (t === 'a') return el.hasAttribute('href') ? 'link' : 'generic';
    if (t === 'button' || t === 'summary') return 'button';
    if (t === 'select') return 'combobox';
    if (t === 'textarea') return 'textbox';
    if (t === 'input') {
      const ty = (el.getAttribute('type') || 'text').toLowerCase();
      if (ty === 'checkbox' || ty === 'radio') return ty;
      if (ty === 'range') return 'slider';
      if (ty === 'number') return 'spinbutton';
      if (ty === 'search') return 'searchbox';
      if (BTN_INPUT[ty]) return 'button';
      return 'textbox';
    }
    return 'generic';
  };

  // ---------- selector ----------
  const selOf = (el) => {
    const parts = [];
    for (let n = el, i = 0; n && n.nodeType === 1 && i < 4; i++) {
      const t = n.localName;
      let p = t;
      if (n.id) { parts.unshift(p + '#' + esc(n.id)); break; }
      const cls = Array.prototype.filter.call(n.classList || [], (c) => c.length <= 30).slice(0, 2);
      if (cls.length) p += cls.map((c) => '.' + esc(c)).join('');
      const par = n.parentElement;
      if (par) {
        const same = Array.prototype.filter.call(par.children, (c) => c.localName === t);
        if (same.length > 1) p += ':nth-of-type(' + (same.indexOf(n) + 1) + ')';
      }
      parts.unshift(p);
      if (t === 'body' || t === 'html') break;
      n = par;
    }
    return parts.join(' > ');
  };

  // ---------- scan ----------
  const all = Array.from(doc.querySelectorAll('*'));
  const truncatedScan = all.length > MAX_EL;
  if (truncatedScan) all.length = MAX_EL;

  const contrast = [], contrastUnknown = [], targets = [], unnamed = [], imagesNoAlt = [], smallText = [], headings = [];
  const TEXT_OK = { script: 1, style: 1, noscript: 1, template: 1, head: 1, title: 1, meta: 1, link: 1 };

  for (const el of all) {
    const ln = el.localName;
    if (TEXT_OK[ln]) continue;
    const isSvgNs = el.namespaceURI === 'http://www.w3.org/2000/svg';
    const text = isSvgNs ? '' : directText(el);
    const isInter = el.matches(INTERACTIVE);
    const isImg = ln === 'img' && !el.hasAttribute('alt');
    const isHead = /^h[1-6]$/.test(ln) || el.getAttribute('role') === 'heading';
    if (!text && !isInter && !isImg && !isHead) continue;

    const r = el.getBoundingClientRect();
    if (!isVisible(el, r)) continue;
    const rect = rectOf(r);
    const skip = skipped(el);

    // text: contrast + small text
    if (text && !skip) {
      const s = getComputedStyle(el);
      const fs = parseFloat(s.fontSize);
      if (fs < 12) smallText.push({ el, text: clip(text, 60), fontSize: Math.round(fs * 100) / 100, rect });
      const fw = parseInt(s.fontWeight, 10) || (s.fontWeight === 'bold' ? 700 : 400);
      const large = fs >= 24 || (fs >= 18.66 && fw >= 700);
      const bg = effBg(el);
      const c = parseColor(s.color);
      let unk = null;
      if (!c) unk = 'unparseable text color';
      else if (c[3] === 0) unk = 'transparent text color (possible background-clip:text)';
      else if (bg.reason) unk = bg.reason;
      if (unk) {
        if (!isDisabled(el)) contrastUnknown.push({ el, text: clip(text, 60), reason: unk, rect });
      } else {
        const fgc = over([c[0], c[1], c[2], c[3] * effOpacity(el)], bg.rgb);
        const ratio = ratioOf(fgc, bg.rgb);
        const required = large ? 3 : 4.5;
        if (ratio < required && !isDisabled(el)) {
          contrast.push({ el, text: clip(text, 60), fg: hex(fgc), bg: hex(bg.rgb), ratio: (Math.round(ratio * 100) / 100 >= required ? Math.floor(ratio * 100) : Math.round(ratio * 100)) / 100, required, large, rect });
        }
      }
    }

    // interactive: target size + accessible name
    if (isInter) {
      const par = el.parentElement;
      const inlineLink = ln === 'a' && par && /^(p|li|span)$/.test(par.localName) && !!directText(par);
      const w = r.width, h = r.height;
      const nm = accName(el);
      if (!inlineLink) {
        const level = (w < 24 || h < 24) ? 'fail-24' : (w < 44 || h < 44) ? 'below-44' : null;
        if (level) targets.push({ el, name: clip(nm.name, 60), w: Math.round(w), h: Math.round(h), rect, level });
      }
      const role = roleOf(el);
      if (role !== 'generic' && !skip && !nm.name) {
        unnamed.push({ el, role, rect });
      } else if (role !== 'generic' && !skip && nm.placeholderOnly) {
        unnamed.push({ el, role, rect, placeholderOnly: true });
      }
    }

    if (isImg && !skip && !/^(presentation|none)$/.test(el.getAttribute('role') || '')) {
      imagesNoAlt.push({ el, src: (el.currentSrc || el.getAttribute('src') || '').slice(0, 80), rect });
    }
    if (isHead && !skip) {
      const lv = /^h([1-6])$/.test(ln) ? +ln[1] : (parseInt(el.getAttribute('aria-level'), 10) || 2);
      headings.push({ level: lv, text: clip(el.textContent, 60), rect });
    }
  }

  const fin = (arr, fn) => arr.map((o) => { const out = Object.assign({ selector: selOf(o.el) }, o); delete out.el; return fn ? fn(out) : out; });
  // placeholderOnly items: keep key order readable (selector, role, placeholderOnly, rect)
  contrast.sort((a, b) => a.ratio - b.ratio);
  targets.sort((a, b) => (a.level === b.level ? 0 : a.level === 'fail-24' ? -1 : 1) || (a.w * a.h - b.w * b.h));
  smallText.sort((a, b) => a.fontSize - b.fontSize);

  const result = {
    url: location.href,
    viewport: { w: win.innerWidth, h: win.innerHeight },
    dpr: win.devicePixelRatio || 1,
    scrollY: Math.round(sy),
    docWidth: doc.documentElement.scrollWidth,
    horizontalOverflow: doc.documentElement.scrollWidth > win.innerWidth + 1,
    truncatedScan,
    contrast: fin(contrast.slice(0, LIMIT)),
    contrastUnknown: fin(contrastUnknown.slice(0, LIMIT)),
    targets: fin(targets.slice(0, LIMIT)),
    unnamed: fin(unnamed.slice(0, LIMIT)),
    imagesNoAlt: fin(imagesNoAlt.slice(0, LIMIT)),
    smallText: fin(smallText.slice(0, LIMIT)),
    headings: headings.slice(0, LIMIT),
    counts: {
      contrast: contrast.length,
      contrastUnknown: contrastUnknown.length,
      targets: targets.length,
      targetsFail24: targets.filter((t) => t.level === 'fail-24').length,
      targetsBelow44: targets.filter((t) => t.level === 'below-44').length,
      unnamed: unnamed.length,
      imagesNoAlt: imagesNoAlt.length,
      smallText: smallText.length,
      headings: headings.length,
      scanned: all.length,
    },
  };
  return JSON.stringify(result);
})()
