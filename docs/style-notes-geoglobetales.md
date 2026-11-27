# Lessons from GeoGlobeTales (@GeoGlobeTales, 2.1M subs, Shorts 12–61M views)

Studied: titles/views of the top 48 Shorts, transcripts of 2, and cover + 3 internal frames of the top 12
(`docs/research/geoglobetales/sheet0.jpg`, `sheet1.jpg`).
**Full 4 fps shot-by-shot study of their Diomede Short: [`frame-study-geoglobetales-diomede.md`](frame-study-geoglobetales-diomede.md).** Take the techniques, build our own look. Never copy their art or characters.

## Writing
- One "Why …?" / "How …?" story per Short, 60–105 s (ours: 2 facts in ~40 s). Titles: "Why X …? 🤯 Thing 📍".
- Line 1 = the surprise + a promise: "…just 2 miles apart, and they're even connected sometimes, and here is why."
- Human detail per beat (82 residents, military only, a man walking 27 years). Escalate obstacles in journeys.
- End on a payoff/twist line ("you'd become a kind of time traveler"). No outro CTA.
- Top themes: journeys & routes, "why borders look like that", "difference between X and Y", invisible lines (Wallace Line, jet stream, time zones), dangerous places.

## Visual grammar
1. **An icon for every sentence**: skull (danger), crowds of person pictograms, animals, planes, warning triangles, "no" circles, viruses, flags, cartoon narrator with a speech bubble.
2. **Flags clipped inside country/island shapes.**
3. **Flat, saturated fills + glowing outlines** (red, orange, neon green, cyan); bold white labels inside shapes.
4. **Fake 3D**: extruded islands with drop shadow; huge text laid along a line ("160 km"); giant letters standing on the map.
5. **Numbers as pictograms**: "80%" over a row of people; live counters ("≈26,875").
6. **Routes**: thick yellow animated paths, glowing dashed borders, time-zone stripe bands, an icon travelling along the path.
7. **Close regional camera**, satellite basemap slightly desaturated; globe only for world-scale beats.
8. **Captions small and plain** (white, lower-middle, sentence fragments); visuals carry the meaning.
9. History beats switch to an old-map palette or illustrated scenes.

## Our build plan (style kit v2)
- Icons: OpenMoji (CC BY-SA 4.0) or Twemoji (CC BY 4.0) via npm, credited in descriptions. Flags: `flag-icons` (MIT).
- Renderer components: `iconAt(ll, name, t0)` pop-in/bob, `crowd(ll, n)`, `flagFill(feature, iso)`, `extrude(feature, depth)`,
  `bigLineText(a, b, text)`, `routeWithTraveller(coords, icon)`, `glowBorder(line, color)`, `stat(number, pictogram)`, caption style "small".
- Keep: sharp NASA terrain, overlap scan, −14 LUFS, calm 3 s camera moves.
