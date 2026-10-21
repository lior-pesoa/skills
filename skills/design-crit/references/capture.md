# Capture

Screenshots are the evidence. Get them clean, name them `<screen>-<size>-<theme>[-<state>].png`, and put them in `<run>/shots/`. Record every capture in `coverage.captured` and every gap in `coverage.not_captured`.

## Web

**1. Get a URL.** Use the one given. Otherwise find the dev command in `package.json` (`dev`, `start`), check whether a server is already listening (`lsof -iTCP -sTCP:LISTEN -n -P | grep node`) and reuse it. If you must start one, run it in the background, note how to stop it, and stop it before you finish.

**2. Screenshots.** Use `scripts/capture.cjs`. It scrolls the whole page before the full-page shot, so lazy-loaded images and scroll-triggered content render (the Playwright CLI's `screenshot --full-page` doesn't scroll, and leaves holes where lazy images should be). It can also run the measurement in the same page load.

```sh
mkdir -p <scratchpad>/pw && (cd <scratchpad>/pw && npm i -s playwright@1.56.1)   # once per session
export NODE_PATH=<scratchpad>/pw/node_modules
node <skill-dir>/scripts/capture.cjs <url> shots/home-390-light.png 390 844 light measure-390.json
node <skill-dir>/scripts/capture.cjs <url> shots/home-390-dark.png  390 844 dark
node <skill-dir>/scripts/capture.cjs <url> shots/home-1440-light.png 1440 900 light measure-1440.json
node <skill-dir>/scripts/capture.cjs <url> shots/home-1440-dark.png  1440 900 dark
```

- `medium` set: 390 and 1440, light and dark. `high`: add 768.
- It uses the installed Chrome (`channel: "chrome"`); without Chrome, run `npx playwright install chromium` and remove the channel.
- Captures are at device pixel ratio 1, so `scale` is 1 and measurement rects map 1:1 onto the image.
- No Node? Use the browser tools available (e.g. Claude in Chrome: resize the window, scroll, take screenshots), and note the method.
- To look closely, crop: `ffmpeg -loglevel error -y -i in.png -vf "crop=W:H:X:Y" out.png` (more reliable than `sips --cropOffset`).

**3. Look at it live.** With a browser tool, open the page and do what a user does:
- Tab through the page from the top. Note where focus is invisible, lost or in the wrong order.
- Hover and press the main actions. Note missing feedback.
- Force states when you can reach them: empty (new account, cleared data), loading (throttle the network), error (bad input, offline), long text (paste a 300-character name). Capture each one you reach as `-<state>`.
- At `high`: 200% zoom and 320px width (reflow).

**4. Measure.** `capture.cjs` writes the measurement when given a JSON path. Otherwise run `scripts/measure.js` in the page at each width (via the browser tool's run-JavaScript, or Playwright `page.evaluate`). It returns contrast failures, small targets, unnamed controls, images without alt, small text, headings and horizontal overflow, each with a document rect in CSS px. To place a finding on a full-page screenshot: region = rect × (image width ÷ viewport width).

## iOS (SwiftUI, UIKit, Expo)

Build output goes in the session scratchpad (`<scratchpad>/dd`) and is deleted when you're done. Never create build folders in the repo or the home directory.

**1. Build and boot.**
```sh
xcrun simctl list devices available | grep -E "iPhone (1[5-9]|2[0-9])"   # pick a current iPhone
xcrun simctl boot "<device>" ; open -a Simulator
xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=<device>' \
  -derivedDataPath <scratchpad>/dd build
xcrun simctl install booted <scratchpad>/dd/Build/Products/Debug-iphonesimulator/<App>.app
xcrun simctl launch booted <bundle-id>
```
Expo: `npx expo run:ios --device "<device>"` (or use a dev build already installed). Find the bundle id in `app.json`/`app.config.*` or the Xcode project.

**2. Clean status bar** (so screenshots don't carry noise):
```sh
xcrun simctl status_bar booted override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
```

**3. Reach each screen.** Prefer deep links (`xcrun simctl openurl booted <scheme>://path`). Otherwise navigate with the computer-use or simulator tools available, or a UI test that taps through. Note any screen you couldn't reach.

**4. Screenshots.**
```sh
xcrun simctl ui booted appearance light
xcrun simctl io booted screenshot shots/home-iphone-light.png
xcrun simctl ui booted appearance dark
xcrun simctl io booted screenshot shots/home-iphone-dark.png
xcrun simctl ui booted content_size accessibility-extra-extra-extra-large   # largest Dynamic Type
xcrun simctl io booted screenshot shots/home-iphone-light-ax5.png
xcrun simctl ui booted content_size large                                   # reset to default
```
- `medium`: light, dark, and the largest Dynamic Type size on the main screens.
- `high`: add `xcrun simctl ui booted increase_contrast enabled` and states (empty, loading, error, long text).
- Screenshots are at device pixels (e.g. 1179×2556). Long screens: capture each scroll position as its own screen.

**5. Measure.** iOS has no DOM. Use what exists:
- If the project has a UI test target (or you can add a throwaway one in the scratchpad), `XCUIApplication().performAccessibilityAudit()` (iOS 17+) reports contrast, hit regions, Dynamic Type clipping and missing labels.
- Otherwise measure from the screenshot: sample text and background colors from the image and compute the WCAG ratio; measure tap targets in points (pixels ÷ scale; 3× on current iPhones). Mark these notes `measured: "from screenshot"`.

**6. Clean up.** `xcrun simctl status_bar booted clear`, reset appearance and content size, delete `<scratchpad>/dd`.

## Static input (images, Figma frames)

No live page or app: review the images as given, skip measurement except colors sampled from the image, and set `degraded: "static images only: no states, no live measurement"`.
