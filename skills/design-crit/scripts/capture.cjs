// Full-page web capture for design-crit, with lazy content loaded and optional measurement.
//
//   NODE_PATH=<dir>/node_modules node capture.cjs <url> <out.png> <width> <height> <light|dark> [measure.json]
//
// Needs the `playwright` package (npm i playwright@1.56.1 in a scratch dir) and installed Chrome.
// The Playwright CLI's `screenshot --full-page` never scrolls, so lazy images and in-view
// animations stay blank; this script scrolls the whole page first.
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const [, , url, out, w, h, scheme = "light", measureOut] = process.argv;
  if (!url || !out || !w || !h) {
    console.error("usage: capture.cjs <url> <out.png> <width> <height> <light|dark> [measure.json]");
    process.exit(2);
  }
  const browser = await chromium.launch({ channel: "chrome" });
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, colorScheme: scheme });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) {
      scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 150));
    }
    scrollTo(0, 0);
  });
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(800);
  await page.screenshot({ path: out, fullPage: true });
  if (measureOut) {
    const src = fs.readFileSync(path.join(__dirname, "measure.js"), "utf8");
    fs.writeFileSync(measureOut, await page.evaluate(src));
  }
  await browser.close();
  console.log(out);
})().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
