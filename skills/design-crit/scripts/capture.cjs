// Web capture for design-crit, with lazy content loaded and optional measurement.
//
//   NODE_PATH=<dir>/node_modules node capture.cjs <url> <out.png> <width> <height> <light|dark> [measure.json]
//       [--stitch] [--at=<y>] [--settle=<ms>] [--step=<ms>] [--no-hide-fixed]
//
// Modes:
//   default    Scroll through the page, back to the top, then one full-page screenshot.
//   --stitch   For pages whose full-page shot comes out blank (scroll-reveal content): take
//              viewport screenshots one frame at a time (120 px overlap, the newer frame wins), then
//              stitch them with ffmpeg into one PNG of the full document height. Fixed/sticky
//              elements are hidden after the first frame (unless --no-hide-fixed), so they show
//              at most once, in the top frame; use --at for fixed UI that appears on scroll.
//              Without ffmpeg on PATH the frames are kept as <out>-01.png, <out>-02.png, ...
//   --at=<y>   Scroll to y, wait, take a viewport-only screenshot. Fixed/sticky UI stays visible
//              (evidence for sticky headers, bottom CTA bars, chat bubbles).
// Options:
//   --settle=<ms>  wait before each screenshot (default 800)
//   --step=<ms>    wait between scroll steps in the default mode's scroll-through (default 150)
//
// Needs the `playwright` package (npm i playwright@1.56.1 in a scratch dir) and installed Chrome.
// The Playwright CLI's `screenshot --full-page` never scrolls, so lazy images and in-view
// animations stay blank; this script scrolls the whole page first.
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const USAGE =
  "usage: capture.cjs <url> <out.png> <width> <height> <light|dark> [measure.json]\n" +
  "                   [--stitch] [--at=<y>] [--settle=<ms>] [--step=<ms>] [--no-hide-fixed]";
const OVERLAP = 120;
const MAX_FRAMES = 80;
const HIDE_ATTR = "data-design-crit-hidden";

function die(msg) {
  console.error("error: " + msg + "\n" + USAGE);
  process.exit(2);
}

function parseArgs(argv) {
  const pos = [];
  const opt = { stitch: false, at: null, settle: 800, step: 150, hideFixed: true };
  const intOpt = (name, v, min) => {
    if (!/^\d+$/.test(v || "")) die(`--${name} needs a whole number, got "${v || ""}"`);
    const n = parseInt(v, 10);
    if (n < min) die(`--${name} must be >= ${min}`);
    return n;
  };
  for (const a of argv) {
    if (!a.startsWith("--")) { pos.push(a); continue; }
    const [k, v] = a.slice(2).split(/=(.*)/s);
    if (k === "stitch" && v === undefined) opt.stitch = true;
    else if (k === "no-hide-fixed" && v === undefined) opt.hideFixed = false;
    else if (k === "at") opt.at = intOpt("at", v, 0);
    else if (k === "settle") opt.settle = intOpt("settle", v, 0);
    else if (k === "step") opt.step = intOpt("step", v, 0);
    else die(`unknown option ${a}`);
  }
  if (pos.length < 4) die("missing arguments");
  if (pos.length > 6) die(`too many arguments: ${pos.slice(6).join(" ")}`);
  const [url, out, w, h, scheme = "light", measureOut] = pos;
  if (!/^(https?|file):\/\//i.test(url)) die(`url must start with http://, https:// or file://, got "${url}"`);
  if (!/\.png$/i.test(out)) die(`output must be a .png path, got "${out}"`);
  if (!/^\d+$/.test(w) || +w < 1) die(`width must be a positive whole number, got "${w}"`);
  if (!/^\d+$/.test(h) || +h <= OVERLAP) die(`height must be a whole number > ${OVERLAP}, got "${h}"`);
  if (scheme !== "light" && scheme !== "dark") die(`color scheme must be light or dark, got "${scheme}"`);
  if (measureOut && !/\.json$/i.test(measureOut)) die(`measurement output must be a .json path, got "${measureOut}"`);
  if (opt.stitch && opt.at !== null) die("--stitch and --at can't be combined");
  return { url, out, width: +w, height: +h, scheme, measureOut, ...opt };
}

const sleep = (page, ms) => (ms > 0 ? page.waitForTimeout(ms) : Promise.resolve());

// Scroll and report where the page actually is (the last scroll clamps at the bottom).
async function scrollTo(page, y) {
  return page.evaluate((y) => {
    scrollTo(0, y);
    return { y: Math.round(scrollY), doc: document.documentElement.scrollHeight, vh: innerHeight };
  }, y);
}

async function hideFixed(page) {
  // Re-run before every frame: some headers only turn fixed after scrolling.
  await page.evaluate((attr) => {
    if (!document.getElementById(attr)) {
      const st = document.createElement("style");
      st.id = attr;
      st.textContent = `[${attr}], [${attr}] * { visibility: hidden !important; }`;
      document.documentElement.appendChild(st);
    }
    for (const el of document.querySelectorAll("body *")) {
      const p = getComputedStyle(el).position;
      if (p === "fixed" || p === "sticky") el.setAttribute(attr, "");
    }
  }, HIDE_ATTR);
}

async function unhideFixed(page) {
  await page.evaluate((attr) => {
    const st = document.getElementById(attr);
    if (st) st.remove();
    for (const el of document.querySelectorAll(`[${attr}]`)) el.removeAttribute(attr);
  }, HIDE_ATTR);
}

function hasFfmpeg() {
  const r = spawnSync("ffmpeg", ["-version"], { stdio: "ignore" });
  return !r.error && r.status === 0;
}

async function stitch(page, a) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "design-crit-"));
  try {
    const frames = []; // { file, y }
    let pos = await scrollTo(page, 0);
    for (let i = 0; i < MAX_FRAMES; i++) {
      if (i > 0) {
        const next = await scrollTo(page, pos.y + a.height - OVERLAP);
        if (next.y <= pos.y) break; // the page can't scroll further
        if (a.hideFixed) await hideFixed(page);
      }
      await sleep(page, a.settle);
      // Read again after the wait: lazy content can grow the page or nudge the scroll.
      pos = await page.evaluate(() => ({
        y: Math.round(scrollY), doc: document.documentElement.scrollHeight, vh: innerHeight }));
      const file = path.join(tmp, `f${String(i + 1).padStart(2, "0")}.png`);
      await page.screenshot({ path: file });
      frames.push({ file, y: pos.y });
      if (pos.y + pos.vh >= pos.doc) break;
      if (i === MAX_FRAMES - 1) console.error(`warning: stopped after ${MAX_FRAMES} frames; the page is longer`);
    }
    if (a.hideFixed) await unhideFixed(page);

    // Rows of each frame to keep, from its top. Where frames overlap, the newer frame wins: content
    // near the bottom edge often hasn't revealed yet, and has by the next frame. Computed from the
    // real scroll positions, since the last scroll usually clamps and overlaps more than OVERLAP.
    const keeps = frames.map((f, i) =>
      i === frames.length - 1 ? a.height : Math.max(1, Math.min(a.height, frames[i + 1].y - f.y)));

    if (frames.length === 1) {
      fs.copyFileSync(frames[0].file, a.out);
      return [a.out];
    }
    if (!hasFfmpeg()) {
      const base = a.out.replace(/\.png$/i, "");
      const outs = frames.map((f, i) => {
        const dest = `${base}-${String(i + 1).padStart(2, "0")}.png`;
        fs.copyFileSync(f.file, dest);
        return dest;
      });
      console.error(
        `warning: ffmpeg is not on PATH, so the frames were not stitched. Saved ${outs.length} ` +
        `viewport frames instead; each overlaps the next (rows to keep from the top of each: ${keeps.join(", ")}).`);
      return outs;
    }
    const args = ["-loglevel", "error", "-y"];
    for (const f of frames) args.push("-i", f.file);
    const filter = keeps.map((k, i) => `[${i}:v]crop=iw:${k}:0:0[v${i}]`).join(";") + ";" +
      keeps.map((_, i) => `[v${i}]`).join("") + `vstack=inputs=${frames.length}[out]`;
    args.push("-filter_complex", filter, "-map", "[out]", "-frames:v", "1", a.out);
    const r = spawnSync("ffmpeg", args, { encoding: "utf8" });
    if (r.status !== 0) throw new Error("ffmpeg failed to stitch the frames: " + String(r.stderr || r.error || "").trim());
    return [a.out];
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

(async () => {
  const a = parseArgs(process.argv.slice(2));
  let chromium;
  try {
    ({ chromium } = require("playwright"));
  } catch (e) {
    console.error("error: can't load the playwright package. Install it (npm i playwright@1.56.1) and set NODE_PATH to its node_modules.");
    process.exit(2);
  }
  fs.mkdirSync(path.dirname(path.resolve(a.out)), { recursive: true });
  const browser = await chromium.launch({ channel: "chrome" });
  try {
    const page = await browser.newPage({ viewport: { width: a.width, height: a.height }, colorScheme: a.scheme });
    await page.goto(a.url, { waitUntil: "networkidle" });
    let outs;
    if (a.stitch) {
      outs = await stitch(page, a);
    } else if (a.at !== null) {
      const pos = await scrollTo(page, a.at);
      await sleep(page, a.settle);
      await page.screenshot({ path: a.out });
      if (pos.y !== a.at) console.error(`warning: asked for y=${a.at}; the page stopped at y=${pos.y} (end of page)`);
      outs = [a.out];
    } else {
      await page.evaluate(async (step) => {
        for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) {
          scrollTo(0, y);
          await new Promise((r) => setTimeout(r, step));
        }
        scrollTo(0, 0);
      }, a.step);
      await page.waitForLoadState("networkidle");
      await sleep(page, a.settle);
      await page.screenshot({ path: a.out, fullPage: true });
      outs = [a.out];
    }
    if (a.measureOut) {
      if (a.stitch || a.at !== null) {
        // Default mode is already back at the top.
        await page.evaluate(() => scrollTo(0, 0));
        await sleep(page, a.settle);
      }
      const src = fs.readFileSync(path.join(__dirname, "measure.js"), "utf8");
      fs.writeFileSync(a.measureOut, await page.evaluate(src));
      outs.push(a.measureOut);
    }
    for (const o of outs) console.log(o);
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error("error: " + e.message);
  process.exit(1);
});
