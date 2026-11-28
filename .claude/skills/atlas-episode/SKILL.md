---
name: atlas-episode
description: Make an Atlas Unbelievable long-form geography episode (about 10 min, 1920x1080) with animated NASA satellite maps, fact cards, panels, Earshot sound and a -14 LUFS mix, from script to upload package. Use when asked for a new episode, a script, a long video, or to fix/re-render an episode.
---

# Atlas Unbelievable episode

Run `bash setup/setup.sh` first in a fresh session. Python tools use `.venv/bin/python -I`.
Reference implementation: `engine/ep1/` (Episode 1) and its files in `episodes/ep1/`.

## 1. Script (wait for the owner's topic)
- Current format (owner's choice after competitor research): **one country per episode**, "30 Insane Geography Facts About X", ~10 min.
- Write `episodes/epN/script.md`: cold open, chapters of 5 facts, each fact ~55 spoken words incl. one "why/bonus" line,
  `[Visual]` notes, a Shorts plan, voice-recording tips and a **fact-check table** for every number.
- ~140 spoken words per minute: 10 min ≈ 1,400–1,450 words. Count with the `> ` lines.
- Also write `voiceover.txt` (title + narration only, no notes) for the owner's AI voice tool.
- Owner records the voiceover and uploads it. Do not proceed until it arrives.

## 2. Timing
1. `tools/transcribe.py vo/voiceover.mp3 vo/words.json` (fix brand/place mishearings by hand later).
2. `tools/find_beats.py vo/words.json anchors.json vo/beats.json`: fact starts ("Number …"), chapter intros and keyword beats.
3. Copy `tools/plan.py` into the episode and edit the camera keys (`k(t, lon, lat, R, mode)`; `f` = fly with zoom-out dip, `z` = zoom, `l` = linear spin).
   Fly-overs 3 s; arrive 3 s after a fact starts; slow drift while talking. It also writes the SFX event list.

## 3. Scenes
- Copy `engine/ep1/` to `engine/epN/` and replace the per-fact scene blocks in `index.html` (`// ===== Fn ... =====`).
  Reusable pieces: `hl()` highlight, `gline()` drawing line, `marker()`, `lab()` geo label, `pill()`, `bigText()`, `panel()`,
  `moon()`, `moveFC()` (true-size country drag), cross-section/gauge/bar panels, territory pings, coastline sweep.
- Competitor-style look for country episodes: featured country in **red**, saturated teal sea, yellow stickers with arrows and rings.
- Map data: `tools/prep_long.py` (Natural Earth 110m/50m + detailed 10m crops + lakes). Add regions you zoom into.
- Sharp terrain: `tools/gibs_mosaic.py LON0 LAT0 LON1 LAT1 assets/hires/NAME.jpg --level 6-7 --relief-level 7-9`.
  The bbox must be **much larger than the camera view** (edges are feathered). The Shorts template already samples `assets/hires/*`; port that
  `drawSat()` into the episode when you build it (see `tools/make_shorts.py`).
- Known data traps: Natural Earth's Vatican outline is ~10× too small (hand-traced outline in ep1); markers/labels on the far side of the globe must be hidden (`vis()`).

## 4. Check before rendering (cheap)
- Serve the episode folder (`python3 -m http.server 8765`), then `node tools/stills.js t1,t2,... OUT_DIR` and look at contact sheets.
- `node tools/overlap.js` → must print `TOTAL ranges: 0`. Fix positions, re-scan.
- `npx hyperframes lint`.

## 5. Sound
- Music bed: `tools/music_bed.py bed.wav SECONDS` (original Earshot pads, no copyright risk).
- `tools/mix_episode.py vo.mp3 bed.wav assets/plan.json sfx/ mix.wav DURATION` → −14 LUFS. Copy to `assets/mix.mp3`.

## 6. Render and deliver
- `npx hyperframes render --workers 4 --quality standard --output renders/epN.mp4` (≈ 48 min for 10:38 on 4 cores; run in background).
- `tools/encode_upload.sh renders/epN.mp4|renders/frames mix.wav epN-upload.mp4`: always 8–10 Mbps (9 Mbps target). Never lower it to fit the chat;
  deliver the file through Google Drive.
- `ext/motionmaxxing/scripts/look.py FILE --expect SECONDS --expect-audio`: G0/G2 pass, loudness −14, no silent dropouts.
- Pull frames from every chapter and look at them before sending.
- Thumbnail (1280×720): black title bar with a red keyword, red country, yellow stickers, white arrows, yellow rings (`episodes/ep1/thumb/thumb2.html`).
- `youtube-upload.md`: title, description with chapter timestamps (YouTube chapters), tags < 500 chars, settings, credits.
