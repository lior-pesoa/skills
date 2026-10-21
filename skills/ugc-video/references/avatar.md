# Making the avatar clips

Written from runs in OpenArt with the Seedance 2.5 model (text to video with a saved character), 2026-10. Other tools (HeyGen, Hedra, Kling and similar) have the same moving parts: a saved face, a prompt with the spoken line, clip length, and a voice. Map the steps; don't assume the menus.

## 1. The character

- **Face:** a photo-real, phone-selfie portrait of someone who plausibly works in the target trade. Unpolished: natural light, home or workplace background, glasses or no makeup look are fine. It must be AI-generated or used with written permission. A real person's face in a paid ad without consent is the one thing that gets the ad pulled.
- **Age:** match the voice to the face. A voice that sounds younger than the face is one of the fastest giveaways.
- **Background story** (the field that keeps the delivery consistent). Write it about how they talk, not their life story:

```
<Name> is <age> and <runs a small X business / works in X> in <city>. <One line of credibility: years in the trade, who they know.> <She/He/They> talk to the phone camera like sending a quick tip to other <trade>: relaxed, warm, a little fast, plain words, no sales voice. Smiles easily but doesn't overact. Small, natural head movements, hands mostly out of frame. <Clothes, glasses, hair.> Filmed selfie-style at <home/work> in soft daylight.
```

- **Additional angles** (optional): the same person, room and light with the head turned slightly left and slightly right. Helps keep the face stable across clips.

## 2. The prompt

```
@<character> films a selfie video on <her/his/their> phone held at arm's length. <Pronoun> is a <age>-year-old <trade>, at home in the same room as the reference, soft daylight. <Pronoun> looks straight into the camera and says in a warm, casual <accent> voice, a little fast, like a tip to a friend: "<LINE>" Small natural head movements, slight handheld motion, hands out of frame, face centered. No music, no subtitles, no text on screen.
```

- **Nothing may touch the tag.** `@monica,` breaks the reference; `@monica films` works. Type the `@` and pick the character from the popup so it links; pasted tags can turn into an internal id.
- One line per clip. Swap only the quoted line between clips; everything else stays identical.
- "No subtitles, no text on screen" matters: some models burn in captions.

## 3. Settings

| Setting | Value | Why |
|---|---|---|
| Aspect | 9:16 | Reels, TikTok, Shorts |
| Audio | On | The model voices the line |
| Auto polish / prompt rewrite | Off | It rewrites the spoken line |
| Resolution | 480p to test, 720p for keepers | The avatar shows small; 1080p only helps if you skip the cutout |
| Duration | 10s for full lines, about 8s for short ones, shortest for the CTA | Extra length is trimmed in the edit |

## 4. Voice consistency

Text-to-video picks a voice per clip, so the voice can drift between clips. In order of effort:

1. **Attach a voice to the character** (the character's voice field), then test: make clips 1 and 2 at 480p and play them back to back. Same person? Done.
2. **Clone from clip 1:** extract its audio (`ffmpeg -i clip1.mp4 -vn -ac 1 voice.wav`) and upload it as the character's own voice. Most cloning wants 10 to 30 seconds of speech; join two matching clips if one is too short.
3. **Audio first, then lip sync** (most reliable): make the whole voiceover once, then animate the face to it with an image-plus-audio or lip-sync model. The voice can't drift, and a bad mouth only costs a video regeneration.
   - A real person reading the lines sounds best (a friend, or a voice actor from a gig site, usually $20 to $50 for a script this short; get commercial rights in writing).
   - Speech-to-speech (a voice changer) keeps a real person's timing in a chosen voice.
   - Plain text-to-speech sounds the most synthetic. If used, write the way people talk: "Okay, caterers. Do this right now." with short sentences and a "..." pause.
   - Library voices tuned to sound "clean" read as AI. Pick conversational, middle-aged, regional voices.

Spending money (voice tools, voice actors, paid plans) needs the user's OK first.

## 5. What goes wrong (check every clip)

- **Extra or changed words.** Seen in practice: the model inserted "check bow tip with a friend" in the middle of a 9-word line. `scripts/clip-report.py --lines` flags it; cut the segment or regenerate.
- **Slow delivery and long pauses** even when the prompt says "a little fast". Fixed in the edit: pauses cut to a breath, then 1.10 to 1.15x speed with pitch kept.
- **Framing drift.** Later clips often come out wider. Crop them in to clip 1's framing in `cuts.json` (`"crop": "w:h:x:y"`), compared on the framing sheet.
- **Unclear words.** If the transcript mishears a word, viewers will too. Regenerate that clip.
