# Atlas Unbelievable Studio: rules for Claude

Channel: **Atlas Unbelievable** (@AtlasUnbelievable), geography facts that sound fake but are true.
Formats: long episodes (~10 min, landscape 1920×1080) and Shorts (36–50 s, 1080×1920) cut from them.

## Non-negotiables
1. **Facts must be checked.** Every number in a script gets a row in a fact-check table. No guessing.
2. **Only reusable media.** NASA (public domain), Natural Earth, Wikimedia Commons PD/CC0/CC BY/CC BY-SA, our own Earshot sounds.
   **Music = YouTube Audio Library tracks** ("attribution not required") from `music/`, chosen by mood (mysterious, epic, fun, dark);
   the Earshot pad bed is only a fallback.
   Never use other creators' YouTube clips (Content ID, strikes, YouTube ToS). Log credits; paste them in descriptions.
   **Owner decision (Nov 2026): photos found through Google Images are allowed.** Prefer a free-licensed copy when one is
   just as good, skip watermarked/agency photos (Getty, AP, Reuters, AFP), and log every image's source URL in the credits.
3. **No text overlaps.** Run `tools/overlap.js` (episodes) or `tools/soverlap.js` (Shorts) over the whole video before every render: target 0.
4. **Loudness −14 LUFS**, true peak ≤ −1 dB. Check with `ext/motionmaxxing/scripts/look.py --expect-audio`.
5. **Calm, readable motion.** Fly-overs ~3 s with easing, one new element at a time, labels never off-frame.
6. **Sharp maps.** Zoomed scenes use NASA GIBS textures built by `tools/gibs_mosaic.py` (bbox much larger than the view).
6b. **Encode at 22–25 Mbps** (target 24 Mbps H.264, AAC 320k) for every upload file, episodes and Shorts: `tools/encode_upload.sh`.
   Owner decisions (Nov 2026): 2 Mbps looked blurry; 9 Mbps was the stopgap; 22–25 Mbps from Episode 3 on. Capture frames at JPEG quality 95. These files are too big to send in chat (~400 MB limit), so deliver them via Google Drive.
7. Upload settings: Education · Not made for kids · Altered/synthetic content = Yes (AI voice).
8. Don't upload or publish anything without the owner's explicit go-ahead.

## Network hosts this workflow needs (cloud sessions)
gibs.earthdata.nasa.gov, images-api.nasa.gov, images-assets.nasa.gov, commons.wikimedia.org, upload.wikimedia.org,
huggingface.co + us.aws.cdn.hf.co + cdn-lfs.hf.co (Whisper/Kokoro models), raw.githubusercontent.com (Natural Earth data).

## Workflow skills
- `atlas-episode`: script → voiceover → transcript → plan → scenes → preview → overlap scan → render → mix → checks.
- `atlas-shorts`: Shorts + Shorts thumbnails from a finished episode.
- `atlas-media`: sharp maps, NASA/Wikimedia media with credits, Earshot SFX, music bed.
