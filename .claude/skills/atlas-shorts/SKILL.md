---
name: atlas-shorts
description: Cut vertical YouTube Shorts (1080x1920, 36-50 s) and their thumbnails from a finished Atlas Unbelievable episode, with word-by-word captions, hook title, sharp terrain and an end card. Use when asked for Shorts, reels, vertical clips or Shorts thumbnails.
---

# Atlas Unbelievable Shorts

Needs a finished episode: its composition (`engine/epN/`), `vo/words.json`, `assets/plan.json` and the final mix WAV.

## 1. Plan
- 2 facts per Short (~40–46 s), grouped by theme, each with a 2–4 word hook ("BORDERS THAT MAKE NO SENSE").
- Segments start on the word after "Number N." and end 0.35 s after the fact's last word (see `episodes/ep1/shorts/plan.json`).
- Competitor Shorts that perform best are one question or journey ("Can you walk from …?"): consider that format for Shorts made from scratch.

## 2. Generate
`.venv/bin/python -I tools/make_shorts.py SHORTS_PLAN.json EP_DIR OUT_DIR WORDS.json MIX.wav`
- Builds one HyperFrames project per Short: vertical layout (fact card top, map centre, panels below the map, captions above the YouTube UI),
  wider framing for zooms, sharp `assets/hires` textures with feathered edges, captions from the transcript (fix mishearings in `FIX`),
  hook for 2.8 s, "FULL 10-MIN VIDEO ON THE CHANNEL" end card, audio cut from the episode mix at −14 LUFS.
- Vertical-only label fixes live at the end of `template()` in `make_shorts.py`.

## 3. Check
- Serve OUT_DIR on port 8766 → `node tools/sstills.js s01,s02 1,10,30,-2 OUT` for contact sheets.
- `node tools/soverlap.js s01,...,s10` → must print nothing (0 overlaps).
- Render all: loop `npx hyperframes render --workers 4` per Short (≈ 2–5 min each), then `look.py --expect-audio` on each.

## 4. Thumbnails (1080×1920)
- `node tools/sclean.js '[["s01",12],...]' THUMBS_DIR` captures clean frames (overlays hidden).
- Fill `thumbs.html` (headline line 1 white, line 2 yellow, yellow sticker; see `episodes/ep1/shorts/thumbs/thumbs.html`) →
  `node tools/sthumbs.js THUMBS_DIR`.
- Avoid frames where in-video big text sits behind the headline.

## 5. Upload text
Per Short: question-style title with emoji + #shorts, 1–2 sentence description, 5 tags, the matching thumbnail, **Related video = the episode**,
Altered content = Yes, Not made for kids, credit line. One Short per day.
