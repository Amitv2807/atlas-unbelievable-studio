# Atlas Unbelievable Studio: rules for Claude

Channel: **Atlas Unbelievable** (@AtlasUnbelievable), geography facts that sound fake but are true.
Formats: long episodes (~10 min, landscape) and Shorts (36–50 s, vertical) cut from them. Layouts use 1920×1080 / 1080×1920 units;
both are rendered at 1440p (2560×1440 / 1440×2560).

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
6b. **Render at 1440p, encode at 24 Mbps** (H.264, AAC 320k) for every upload, episodes and Shorts: `tools/render_upload.sh`
   (chunked capture → encode, so 1440p frames never fill the disk). Owner decisions (Nov 2026): 2 Mbps looked blurry, 9 Mbps was a stopgap,
   1440p/24 Mbps from Episode 3 on (YouTube gives 1440p uploads its better codec, also for 1080p viewers). Files are ~180 MB per minute,
   too big for chat: deliver via Google Drive with `tools/drive_upload.sh` (needs a fresh OAuth Playground token in the environment's network secrets).
7. Upload settings: Education · Not made for kids · Altered/synthetic content = Yes (AI voice).
8. Don't upload or publish anything without the owner's explicit go-ahead.

## Network hosts this workflow needs (cloud sessions)
gibs.earthdata.nasa.gov, images-api.nasa.gov, images-assets.nasa.gov, commons.wikimedia.org, upload.wikimedia.org,
huggingface.co + us.aws.cdn.hf.co + cdn-lfs.hf.co (Whisper/Kokoro models), raw.githubusercontent.com (Natural Earth data).

## Workflow skills
- `atlas-episode`: script → voiceover → transcript → plan → scenes → preview → overlap scan → render → mix → checks.
- `atlas-shorts`: Shorts + Shorts thumbnails from a finished episode.
- `atlas-media`: sharp maps, NASA/Wikimedia media with credits, Earshot SFX, music bed.
