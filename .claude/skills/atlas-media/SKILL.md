---
name: atlas-media
description: Source visuals and sound for Atlas Unbelievable videos legally and sharply - NASA GIBS satellite+terrain textures, free-to-reuse NASA and Wikimedia Commons photos/clips via yt-dlp with credits, Earshot sound effects and an original music bed. Use when a video needs footage, photos, sharper maps, sound effects or music.
---

# Atlas Unbelievable media

## Rules
- Only public domain / CC0 / CC BY / CC BY-SA. Never NC or ND (the channel is monetized), never other creators' YouTube videos.
  "Fair use" does not stop Content ID claims or strikes.
- Every downloaded file gets a credit line (`credits.json` / `CREDITS.txt`); paste credits into the video description.

## Sharp maps (NASA GIBS, public domain)
`.venv/bin/python -I tools/gibs_mosaic.py LON0 LAT0 LON1 LAT1 OUT.jpg --level L --relief-level RL`
- Blue Marble NG colour (500 m, level ≤ 7) × ASTER GDEM shaded relief (31 m, level ≤ 11), dark water recoloured to our ocean blue, max 4096 px wide.
- Pick the bbox ≥ 2× the camera view; ~0.1–0.8 km/px is plenty. Writes OUT.json with the bbox for the renderer.

## Photos and clips
`.venv/bin/python -I tools/fetch_media.py nasa "QUERY" --type image|video --n 3 --out media/`
`.venv/bin/python -I tools/fetch_media.py commons "QUERY" --type image|video --n 3 --out media/`
- Videos download with yt-dlp. Wikimedia requires a contact in the User-Agent: the owner saves it themselves in `~/.atlas_contact`
  (or `$ATLAS_CONTACT`). Never write the address into code. Without it Wikimedia returns 429.

## Sound
- SFX kit already in `sfx/` (fly-over whoosh, short whoosh, marker pop, counter tick, reveal boom, riser, line swish, title hit).
  New ones: `.venv/bin/earshot make "a soft glassy notification" -o file.wav`, or a set via `--spec kit.json` (see `sfx/kit.json`).
- Music: `tools/music_bed.py bed.wav SECONDS`, original pads with seamless crossfaded loops (no silent seams).
