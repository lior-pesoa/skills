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

Use a simulator of your own so you don't disturb devices other sessions or the user rely on, and delete it at the end.

**1. Build.** A Release build runs without a dev server (Metro), which keeps the capture simple.
```sh
xcodebuild -workspace ios/<App>.xcworkspace -scheme <Scheme> -configuration Release \
  -sdk iphonesimulator -derivedDataPath <scratchpad>/dd CODE_SIGNING_ALLOWED=NO build
```
- Find the bundle id in `app.json`/`app.config.*` or the Xcode project.
- Build fails on files missing from `node_modules`: the dependencies are out of sync. Restore them with the project's install command and check that no tracked file changed (`git status`). Don't run `pod install` unless asked; it can change tracked files.
- React Native/Expo, JS bundle step fails because the working tree has someone's unfinished change: don't touch their work. Review the last commit instead: finish the native build with `SKIP_BUNDLING=1`, then bundle the committed JS from a scratch copy and put it in the app:
  ```sh
  git archive HEAD | tar -x -C <scratchpad>/head && cp .env.local <scratchpad>/head/ 2>/dev/null
  ln -s "$PWD/node_modules" <scratchpad>/head/node_modules
  (cd <scratchpad>/head && npx expo export:embed --platform ios --dev false --entry-file index.js \
     --bundle-output <app>/main.jsbundle --assets-dest <app>)
  ```
  Say in the brief which commit was reviewed and that uncommitted work wasn't.

**2. Boot and install** on a dedicated device, with a clean status bar:
```sh
U=$(xcrun simctl create "design-crit iPhone" com.apple.CoreSimulator.SimDeviceType.iPhone-17 <runtime-id>)
xcrun simctl boot $U && xcrun simctl bootstatus $U -b
xcrun simctl status_bar $U override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
xcrun simctl install $U <scratchpad>/dd/Build/Products/Release-iphonesimulator/<App>.app
xcrun simctl launch $U <bundle-id>
```
(`xcrun simctl list runtimes` and `list devicetypes` give the ids.)

**3. Reach each screen.** Prefer deep links: `xcrun simctl openurl $U <scheme>://<route>`. Recent iOS asks "Open in <App>?" first; confirm it with Return:
`osascript -e 'tell application "Simulator" to activate' -e 'delay 0.5' -e 'tell application "System Events" to key code 36'` (the terminal needs Accessibility permission). Otherwise navigate with computer-use tools or a UI test that taps through. Note any screen you couldn't reach.

**4. Screenshots.** Wait for entrance animations to finish (6–9 s after launch is typical; typing or rotating content needs the full cycle), then check each shot for mid-animation frames.
```sh
xcrun simctl ui $U appearance light ; xcrun simctl io $U screenshot shots/home-iphone-light.png
xcrun simctl ui $U appearance dark  ; xcrun simctl io $U screenshot shots/home-iphone-dark.png
```
- Rotating or crossfading content (hero carousels, typing captions): take a burst of 12–16 shots about 0.6 s apart and keep a frame from the longest run of identical brightness — that's the scene at rest. One mid-fade frame makes everything look dimmed and produces false contrast notes. Quick brightness per frame: `ffmpeg -loglevel error -i f.png -vf "crop=W:H:X:Y,scale=1:1" -f rawvideo -pix_fmt rgb24 - | od -An -tu1`.
- Largest Dynamic Type: set it, **relaunch the app**, navigate back, then capture. A live switch catches half-updated layouts.
  `xcrun simctl ui $U content_size accessibility-extra-extra-extra-large` … `content_size large` to reset.
- `medium`: light, dark, and the largest Dynamic Type size on the main screens. If light and dark render the same, note it (often intentional for always-dark screens).
- `high`: add `xcrun simctl ui $U increase_contrast enabled` and states (empty, loading, error, long text).
- Screenshots are device pixels (1206×2622 on iPhone 17, scale 3). Long screens: capture each scroll position as its own screen.

**5. Measure.** iOS has no DOM. Use what exists:
- If the project has a UI test target (or you can add a throwaway one in the scratchpad), `XCUIApplication().performAccessibilityAudit()` (iOS 17+) reports contrast, hit regions, Dynamic Type clipping and missing labels.
- Otherwise measure from the screenshot: sample text and background colors from the image and compute the WCAG ratio; measure tap targets in points (pixels ÷ scale). Mark these notes `measured: "from screenshot"`.

**6. Clean up.** `xcrun simctl shutdown $U && xcrun simctl delete $U`, and delete `<scratchpad>/dd` and any scratch copy of the source.

## Static input (images, Figma frames)

No live page or app: review the images as given, skip measurement except colors sampled from the image, and set `degraded: "static images only: no states, no live measurement"`.
