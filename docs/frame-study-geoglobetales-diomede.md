# Frame study: GeoGlobeTales "The Distance Between the US and Russia…" (Diomede Islands)

Source: youtube.com/shorts/kBR3Wi-fmns · 60 s · 1080×1920 @ 30 fps. Studied at 4 fps (240 frames).
Private style study only: the video and frames are kept outside the repo and nothing from them goes into our renders
(CLAUDE.md rule 2). We take techniques, not art.

## Shot list (t = seconds)
| t | Caption | Visual / motion |
|---|---|---|
| 0–2 | Not all Americans know | Continental view, satellite basemap. USA filled with a **waving flag texture** clipped to its shape; camera slowly pulls back + pans up. |
| 2–4 | that the US and Russia | **Glowing magenta beam** draws from the US across the Atlantic to Russia (also flag-filled). Camera pans east following the beam. |
| 4–5 | are actually much closer / to each other | Whip pan across the Pacific; map rotated so Russia and Alaska sit side-by-side (Alaska gets its own flag fill). |
| 5–6 | just two miles apart | "2 miles" **types in letter-by-letter with a cyan glow**, laid on a slight arc above the gap. |
| 6–9 | …and more than that / they are even connected… | Hard cut to a **flat cartoon map**: mint/aqua water, Russia = flat coral red, Alaska = flat periwinkle blue, soft glow edges. Dashed white rays converge on the strait. |
| 9–11 | sometimes / and here is why | Rays meet in a **white lens-flare burst** at the Bering Strait. Exit with a **dark vignette wipe** from the right. |
| 11–14 | The countries are separated / by the Bering Strait | Back to satellite but desaturated teal; Russia tinted **neon red**, US **neon cyan**, both with outer glow. Zoom in; "Bering Strait" label writes on along an arc, white **wind/current streaks** in the strait. |
| 15–17 | and if we look closer here | Continued push-in; mainland slides off-frame, background darkens to near-black teal. |
| 17–19 | we can see two tiny Diomede Islands | Islands get a glowing white outline; label "Diomede Islands" pops in **blurred → sharp** with leader lines to both islands. |
| 19–22 | which are 2.4 miles apart | Double-headed arrow between islands with **rolling counter** "1.3 → 2.2 → 2.4 mi (3.8 km)", text rotated parallel to the arrow. Islands get **fake-3D extrusion + soft drop shadow** on the sea. |
| 22–24 | and divide the mainland of the US… | Zoom out; label flies up and fades. |
| 24–26 | and the mainland of Russia | **Split-screen tint**: Russia side muted plum, USA side blue, separated by a dashed white border; huge "RUSSIA / USA" words slide in and settle. |
| 26–29 | Little Diomede belongs to the USA | Push in on the border (now thick white dashes); Little Diomede becomes a **3D waving flag** with a label above. |
| 29–31 | and it is home to one of the most isolated towns | Flag dissolves into real high-res satellite of the island; camera **rotates and zooms** to the village. |
| 31–35 | in the USA called Diomede / with a population of 82 people | "Diomede" label writes on with a pin line; yellow **person-icon counter badge** counts 24 → 53 → 72 → 80 → 82. |
| 35–38 | Big Diomede belongs to Russia | Pull back, rotate; "Big Diomede" label laid diagonally along the island's long axis. |
| 38–40 | and it is uninhabited / only military personnel are present | Big Diomede filled with Russian flag (texture shows terrain through it), extruded. |
| 40–42 | (cont.) | Three teal **soldier avatar circles** pop in; a black speech bubble "COMRADE!" pops with overshoot. Humour beat. |
| 42–45 | Therefore Diomede is the closest American town to Russia | Fast whip rotation to the gap between islands; arrow counter again (1.6 → 2.2 → 2.4 mi). |
| 45–47 | separated by two miles of water / and the point is that | Flags reappear on both islands, then zoom out quickly. |
| 47–49 | in the winter the water freezes | **Snow particles**; sea freezes as a growing ice texture (patchy cellular reveal). Red dashed border line drawn across. |
| 49–52 | and creates an ice bridge… making it possible to cross the border by land | Full ice texture; a black **hiker pictogram** scales in and "walks" (bobbing) across the border. |
| 52–53 | interesting that there is | Whitish fade transition. |
| 53–56 | an international date line between these two islands | Regional satellite; white glowing line draws on, "International Date Line" label written vertically along it. |
| 56–57 | the difference between them is 21 hours | Zoom in; "Monday 09:00 pm / Sunday 12:00 am" labels either side of the line, scaling up. |
| 57–60 | and if you cross the border from the US side you will be in the future / and become a kind of time traveler | Glowing curved arrow draws across the line; **cartoon sticker characters** pop in (pop-culture time-travel reference) as the punchline. |

## Style takeaways
1. **Pace**: a new visual event every ~1–2 s; the camera never stops (slow push/rotate between beats, whip moves on scene changes). Faster than our "calm 3 s fly-over" rule; mostly it's the *overlays* that change each line, while the camera drifts.
2. **Every caption line gets one overlay** that literally illustrates it (beam = "closer", counter = "82 people", ice = "freezes", hiker = "cross by land", arrow = "future").
3. **Three map looks, switched by meaning**: realistic satellite (place), flat cartoon map (concept/"connected"), neon-tinted dark satellite (focus/drama). Changes are hard cuts or vignette wipes.
4. **Label grammar**: bold white sans with soft glow; write-on/blur-to-sharp entrances; labels follow the geometry (along arcs, along island axes, vertical along lines); leader lines from label to feature.
5. **Numbers animate**: rolling counters on distance arrows and population badges; units in two systems ("2.4 mi (3.8 km)").
6. **Depth tricks**: extruded islands with drop shadow, flag textures that wave and let terrain show through, vignette darkening around the subject.
7. **Captions**: small, plain white, one phrase, fixed lower-middle position, quick fade-in. They never compete with the big labels.
8. **Humour/payoff beats**: icon + speech bubble ("COMRADE!"), sticker characters at the end. No outro or CTA; ends right on the punchline.

## Ideas for our kit (our own build, no copying)
- `counterArrow(a, b, toValue, units)`: double arrow with a rolling number set parallel to it.
- `iconBadge(ll, icon, count)`: pictogram + rolling count in a badge (OpenMoji/Twemoji icons, credited).
- `splitTint(borderLine, colorA, colorB, labelA, labelB)`: two-side country tint with big words.
- `freezeReveal(region)`: animated ice mask + snow particles (procedural, no stock).
- Look presets: `satellite`, `flatConcept`, `neonFocus`, with a vignette wipe between them.
- Keep our own rules: text labels pass `tools/soverlap.js`; consider loosening the 3 s motion rule for Shorts overlays (camera stays calm, overlays change per line).
