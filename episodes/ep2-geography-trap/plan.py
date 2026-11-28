"""Episode 2 timing plan: phrase anchors -> times, camera keys, headline segments, chapters, SFX.
python3 episodes/ep2-geography-trap/plan.py   (writes engine/ep2/assets/plan.js + plan.json)"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
W = json.load(open(os.path.join(HERE, "vo/words.json")))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
T = []  # (token, start)
for w, s, e in W:
    for p in re.split(r"[\s\-]+", w):
        if norm(p): T.append((norm(p), s))
END = 1342.0

ANCH = """c_line|the most important line
c_border|you won't find it
c_map|it's drawn by the map
c_xi|xi jinping and vladimir
c_40|than 40 times
c_deeper|but there's a deeper
c_share|russia and china share
c_locked|each locked inside
ch1|start with land
n14|14 countries
watched|every one of those borders
money|and that costs money
west|for moscow the most
six|six of russia's
nor|norway
fin|finland
est|estonia
lva|latvia
ltu|lithuania
pol|poland
fin23|when finland joined
k1300|1300
altog|altogether
k2500|2500
east|in the east the picture
y2008|2008
catch|but here's the catch
quarters|around three
urals1|ural mountains
moscow|moscow and st
fareast|far east
nervous|so russia's most valuable
nothing|almost nothing to protect
orbit|look at europe from orbit
alps|alps
carp|carpathians
pyr|pyrenees
urals2|urals lies
plain|european plain
narrow|it is narrow near poland
widen|keeps widening
thousands|spans thousands
road|for centuries that open plain
plc|polish
sweden|sweden marched
napoleon|napoleon
germany|germany came twice
again|again and again the danger
coldwar|during the cold war
soviet|the soviet union and its satellite
germanymid|middle of germany
gap|narrow gap in the west
y1991|then in 1991
buffer|lost a buffer
fellback|fell back hundreds
y2005|in 2005 vladimir
quote|the greatest geopolitical
logic|strategically
cushion|everything the empire
without|without mountains or rivers
spend34|around 3 to 4
nineties|hard years of the 1990s
cheaper|the cheaper option
friendly|friendly governments as far west
baltic|reaching the baltic
carp2|the carpathians in the south
belarus|belarus stayed close
ukraine1|ukraine for a time
moving|but the line kept moving
pol99|poland joined nato
balt04|estonia latvia and lithuania followed
ua14|and in 2014
defensive|nato is a defensive
reads|but moscow reads
push|push the frontier outward
mongol|after throwing off mongol
expanded|russia expanded east
peter|peter the great fought
cath|catherine the great
inv22|in 2022 putin
price|the price has been
million|well past a million
fifth|a fifth of ukraine
metres|meters per day
third|around a third
ch2|russia's closest partner
richest|for most of history china
silk|eastern end of the silk road
threat|its problem was protecting
direction|almost every direction
north|to the north there's no
steppe|eurasian steppe
horsemen|nomadic horsemen
wall|the great wall
weakness|hugely expensive
russianorth|later the threat from the north
ussuri|ussuri
quiet|today with beijing
sw|to the southwest stands
himal|the himalayas
neveragreed|never agreed
y1962|in 1962
galwan|galwan
water|because of water
tower|tibetan plateau is often
rivers|yangtze and yellow
heartland|china's heartland
basin|yangtze basin alone
rice|rice
india|the same plateau also feeds
indus|the indus
brahma|brahmaputra
sutlej|sutlej
highground|high ground
force|china keeps a large standing
south|to the south lies
jungle|jungle
y1979|1979
died|tens of thousands died
terrain|the war showed
redriver|red river
adversary|vietnam is no small
ranking|by one widely used
socialist|although both countries
scs|south china sea
supplied|washington has supplied
danang|da nang
avoids|vietnam still avoids
troops99|so china keeps troops
treaty|land border treaty
xinjiang|then there's the far northwest
gateway|gateway to central asia
silkroad2|revive the old silk road
contested|chinese rule has long
han|large scale han
urumqi|tensions with the
y2009|july 2009
detention|mass detention
genocide|the united states government
rejects|beijing rejects
frontiers|every one of these frontiers
fs1|steppe
fs2|mountains
fs3|jungle
fs4|desert
sea|that threat comes from the sea
ch3|for most of its history the pacific
opium|first opium war
navy1839|british royal navy
qing|forced the qing
gateway2|the sea had become
different|today the danger is different
oil93|imported oil since
crude70|70
gas40|of its natural gas
fourfifths|four
malacca|the strait of malacca
k900|the strait runs nearly
sumatra|sumatra
narrowest|at its narrowest point
k3|less than 3
andaman|andaman
changi|changi
dilemma|the malacca dilemma
choke|only one of several choke
miyako|miyako
luzon|luzon
lean|lean toward the united
build|beijing's first answer
bri|in 2013 in kazakhstan
web|a web of railways
cpec|its flagship is
idea|the idea tankers
gwadar|unload at gwadar
north2|cargo travels north
billions|china has poured
thin|results have been thin
tiny|gwadar handles
singapore|singapore alone moved
attacks|separatist militants
lastword|even if every problem
diego|diego garcia
bombers|long range bombers
wider|the wider belt and road
aid|researchers at
distress|financial distress
redrawn|the projects have built
lanes|so the old sea lanes
exports|exports of around
surplus|a trade surplus
naval|that's why beijing decided
ship200|us navy intelligence
navy370|china's navy is now
pent|the pentagon expects
ch4|but more ships can't
taiwan|only one permanent fix
chips|chip industry
key|the key in the lock
chain|first island chain
boxes|the string of islands
harbors|control taiwan
maneuver|room to maneuver
yet|yet even then
numbers|and numbers alone
heavier|the american fleet is far heavier
frigates|much of china's construction
subs|in submarines
catching|china is catching up
gamble|riskiest gamble
why|so why not build
landfront|it still has to pay
dividing|dividing line between
landpowers|some are forced
seapowers|others are free
ch5|russia shows just how
coast|it has one of the longest
arctic1|faces the arctic ocean
warm|ever since peter the great
murmansk|murmansk
gulf|gulf stream
blacksea1|in the south novorossiysk
blacksea2|sit inside the black sea
openocean|to reach the open ocean
bosph|bosphorus
turkey|both controlled by turkey
choice|then it faces a choice
suez|suez canal
bab|bab
gib|or west through the strait
nato2|both nato members
vlad|in the pacific vladivostok's
icebreak|needs icebreakers
seajapan|sea of japan
routes|russia tried other routes
greatgame|great game
portarthur|it leased port arthur
y1905|1905
never|even at the height
warming|a warming arctic
ice|sea ice is shrinking
y2050|before 2050
half|russia controls roughly half
nsr|northern sea route
pct40|by around 40
doors|but the arctic has only two doors
bering|in the pacific ships must pass
airbases|where the united states keeps
jber|joint base
putin25|putin saw that base
kitsap|further south naval base kitsap
subs2|ohio
giuk|in the atlantic the other door
giukgap|closely watched
rotterdam|any ship heading for rotterdam
svalbard|svalbard archipelago
treaty1920|a 1920 treaty
patrols|patrols those waters
finswe|with finland and sweden
coldresp|cold response
choice2|so russia faces a hard choice
afford|with a smaller economy
ch6|russia keeps drawing
warmer|a warmer arctic may
china2|china has become
ocean|no amount of money
usa|now compare the united states
twooceans|two oceans
borders2|it shares land borders
riogrande|one shielded
ally|the other a close
coasts|its coasts open
nofrozen|no frozen harbors
freedom|that freedom helped
landsea|a great land power
reshape|russia and china want
behind|but geography means
lastw|other side of the ocean"""

B = {}; pos = 0
for line in ANCH.splitlines():
    name, ph = line.split("|"); ws = [norm(x) for x in re.split(r"[\s\-]+", ph) if norm(x)]
    for i in range(pos, len(T)):
        if all(i + k < len(T) and T[i + k][0].startswith(ws[k]) for k in range(len(ws))):
            B[name] = T[i][1]; pos = i + 1; break
    else:
        raise SystemExit(f"anchor not found after {T[pos][1] if pos < len(T) else 'end'}: {name} '{ph}'")

# ---- camera shots: (anchor, offset, lon, lat, R, mode, dur) ; mode f=fly z=zoom l=linear spin
SH = [("c_line", 0, 62, 38, 430, "", 0),
      ("ch1", 0, 92, 47, 520, "l", 4),
      ("west", 0, 30, 58, 1250, "f", 3),
      ("east", 0, 100, 55, 780, "f", 3),
      ("catch", 0, 72, 57, 820, "f", 3),
      ("nervous", 0, 35, 55, 1250, "f", 3),
      ("orbit", 0, 25, 51, 1450, "f", 3),
      ("road", 0, 30, 53, 1450, "f", 3),
      ("coldwar", 0, 22, 51, 1250, "f", 3),
      ("without", 0, 36, 54, 1100, "f", 3),
      ("cheaper", 0, 27, 53, 1650, "f", 3),
      ("defensive", 0, 38, 55, 950, "f", 3),
      ("mongol", 0, 72, 58, 600, "f", 3),
      ("peter", 0, 29, 55.5, 1350, "f", 3),
      ("inv22", 0, 34, 49, 2300, "f", 3),
      ("ch2", 0, 98, 36, 680, "f", 4),
      ("north", 0, 108, 43, 1300, "f", 3),
      ("russianorth", 0, 128, 46, 1500, "f", 3),
      ("ussuri", -0.5, 133.6, 46.6, 4200, "z", 3),
      ("sw", 0, 84, 31, 1650, "f", 3.5),
      ("water", 0, 93, 32, 1250, "f", 3),
      ("india", 0, 84, 28, 1350, "f", 3),
      ("south", 0, 106, 21.5, 2900, "f", 3),
      ("socialist", 0, 112, 13, 1300, "f", 3),
      ("troops99", 0, 106, 22, 2500, "f", 3),
      ("xinjiang", 0, 84, 41, 1450, "f", 3),
      ("urumqi", 0, 87.6, 43.6, 2800, "z", 3),
      ("frontiers", 0, 100, 34, 620, "f", 3),
      ("sea", -1, 112, 28, 700, "", 3),
      ("different", 0, 85, 14, 560, "f", 3),
      ("malacca", -1, 100, 4, 2300, "f", 3),
      ("narrowest", 0, 103.82, 1.2, 22000, "z", 3),
      ("andaman", -0.8, 98, 6, 1650, "f", 3),
      ("changi", 0, 101.5, 3.5, 2100, "", 3),
      ("dilemma", 0, 110, 12, 1000, "f", 3),
      ("choke", 0, 123, 21, 1200, "f", 3),
      ("build", 0, 75, 42, 520, "f", 3),
      ("cpec", 0, 67, 30, 1750, "f", 3),
      ("attacks", 0, 70, 30, 2000, "", 3),
      ("lastword", 0, 66, 10, 760, "f", 3),
      ("wider", 0, 72, 30, 480, "f", 3),
      ("lanes", 0, 92, 15, 520, "f", 3),
      ("naval", 0, 120, 25, 860, "f", 3),
      ("ch4", 0, 124, 24, 1450, "f", 3.5),
      ("chain", 0, 126, 22, 1050, "f", 3),
      ("harbors", 0, 122.3, 24.1, 5200, "z", 3),
      ("yet", 0, 115, 10, 680, "f", 3),
      ("why", 0, 95, 40, 500, "f", 3),
      ("ch5", 0, 80, 77, 680, "f", 4),
      ("warm", 0, 38, 62, 820, "f", 3),
      ("blacksea1", 0, 35, 43.5, 2200, "f", 3),
      ("openocean", 0, 27.8, 40.6, 6500, "z", 3),
      ("choice", 0, 36, 24, 1400, "f", 3),
      ("gib", 0, -5.4, 36, 6500, "f", 3),
      ("vlad", 0, 132.5, 42.8, 6000, "f", 3.5),
      ("seajapan", 0, 136, 41, 1650, "f", 3),
      ("routes", 0, 75, 40, 640, "f", 3),
      ("portarthur", 0, 121.3, 38.8, 2200, "f", 3),
      ("warming", -1.5, 60, 80, 600, "f", 3),
      ("nsr", -0.5, 70, 62, 580, "f", 3),
      ("doors", 0, -172, 68, 900, "f", 3),
      ("bering", 0, -168, 64, 2300, "z", 3),
      ("airbases", 0, -160, 62, 1600, "", 3),
      ("kitsap", 0, -138, 56, 950, "f", 3),
      ("giuk", 0, -15, 62, 1350, "f", 3),
      ("rotterdam", 0, 15, 70, 1150, "f", 3),
      ("finswe", 0, 22, 65, 1250, "f", 3),
      ("choice2", 0, 80, 60, 540, "f", 3),
      ("ch6", 0, 90, 55, 520, "f", 3),
      ("china2", 0, 105, 35, 620, "f", 3),
      ("usa", 0, -98, 40, 560, "f", 3.5),
      ("reshape", 0, -176, 46, 380, "f", 3.5)]
K = []; prev = None
for name, off, lon, lat, R, mode, dur in SH:
    t = round(B[name] + off, 2)
    if prev is None:
        K.append([t, lon, lat, R, ""]); prev = (lon, lat, R); continue
    # drift: slow push-in while the narrator talks, then start the move
    K.append([t, prev[0] + (0.6 if prev[2] < 1200 else 0.15), prev[1], round(prev[2] * 1.05), ""])
    K.append([round(t + dur, 2), lon, lat, R, mode]); prev = (lon, lat, R)
K.append([END, prev[0] + 6, prev[1], prev[2] * 1.03, "l"])

HEAD = [("ch1", 3.4, "14 NEIGHBOURS EACH"), ("west", 0, "NATO ON THE DOORSTEP"), ("east", 0, "WHERE RUSSIANS LIVE"), ("orbit", 0, "THE EUROPEAN PLAIN"),
        ("road", 0, "THE INVASION ROAD"), ("coldwar", 0, "THE SOVIET BUFFER"), ("without", 0, "DEFENDED WITH MONEY"), ("cheaper", 0, "THE FIGHT FOR INFLUENCE"),
        ("defensive", 0, "PUSH THE FRONTIER OUT"), ("price", 0, "THE PRICE OF THE WAR"),
        ("ch2", 3.4, "A THREAT IN EVERY DIRECTION"), ("north", 0, "THE OPEN NORTH"), ("sw", 0, "THE HIMALAYAN WALL"), ("water", 0, "THE WATER TOWER OF ASIA"),
        ("south", 0, "THE JUNGLE FRONT"), ("socialist", 0, "VIETNAM AND THE SEA"), ("xinjiang", 0, "XINJIANG"), ("frontiers", 0, "FOUR FRONTIERS"),
        ("ch3", 3.4, ""), ("different", 0, "CHINA'S OIL LIFELINE"), ("malacca", 0, "THE STRAIT OF MALACCA"), ("dilemma", 0, "THE MALACCA DILEMMA"), ("build", 0, "THE BELT AND ROAD"),
        ("cpec", 0, "THE PAKISTAN SHORTCUT"), ("lastword", 0, "WITHIN RANGE"), ("wider", 0, "A TRILLION IN LOANS"), ("naval", 0, "THE NAVAL BUILD-UP"),
        ("ch4", 3.4, "THE KEY IN THE LOCK"), ("yet", 0, "NUMBERS AREN'T EVERYTHING"), ("why", 0, "LAND POWER vs SEA POWER"),
        ("ch5", 3.4, "A FROZEN COASTLINE"), ("warm", 0, "THE WARM-WATER DREAM"), ("openocean", 0, "THE TURKISH STRAITS"), ("choice", 0, "TWO WAYS OUT"),
        ("vlad", 0, "VLADIVOSTOK"), ("routes", 0, "OTHER ROUTES"), ("warming", 0, "A WARMING ARCTIC"), ("doors", 0, "THE ARCTIC'S TWO DOORS"),
        ("giuk", 0, "THE GIUK GAP"), ("rotterdam", 0, "SVALBARD"), ("choice2", 0, "NAVY OR ARMY?"),
        ("ch6", 3.4, "THE SHORT STRAW"), ("usa", 0, "THE AMERICAN ADVANTAGE"), ("reshape", 0, "")]
SEG = [[round(B[a] + o, 2), t] for a, o, t in HEAD]
CH = [[B["ch1"], "RUSSIA: A FORTRESS WITH NO WALLS"], [B["ch2"], "CHINA: SURROUNDED ON LAND"], [B["ch3"], "THE MALACCA DILEMMA"],
      [B["ch4"], "TAIWAN AND THE ISLAND CHAIN"], [B["ch5"], "RUSSIA'S FROZEN COAST"], [B["ch6"], "THE GEOGRAPHY OF POWER"]]
# ---- SFX
fl = [k[0] - 3 for k in K if k[4] == "f"]; zm = [k[0] - 3 for k in K if k[4] == "z"]
SFX = {"whoosh": [round(x + 0.2, 2) for x in fl], "zoom": [round(x + 0.2, 2) for x in zm],
       "title": [0.3] + [round(c[0], 2) for c in CH] + [round(B["c_locked"] + 2.6, 2), round(B["lastw"] + 0.6, 2)],
       "boom": [round(B[k], 2) for k in ("k2500", "y1991", "quote", "inv22", "million", "k3", "dilemma", "ship200", "gamble", "afford", "landsea")],
       "pop": [round(B[k] + 0.2, 2) for k in ("nor", "fin", "est", "lva", "ltu", "pol", "moscow", "plc", "sweden", "napoleon", "germany", "pol99", "balt04", "ussuri",
                                               "y1962", "galwan", "y1979", "danang", "y2009", "andaman", "changi", "miyako", "luzon", "gwadar", "diego", "murmansk",
                                               "bosph", "suez", "bab", "gib", "y1905", "jber", "kitsap", "svalbard")],
       "tick": [round(B["n14"] + i * 0.28, 2) for i in range(14)]}
# full-screen graphic scenes and map effects added to the first half
SFX["zoom"] += [round(x, 2) for x in (B["road"] - .2, B["price"], B["wall"] - .2, B["himal"] - .4, B["basin"] - .2, B["terrain"] - .2, B["frontiers"] + .05)]
SFX["pop"] += [6.55, round(B["c_share"] + 2.8, 2), round(B["c_share"] + 3.2, 2)] + [round(B[k], 2) for k in ("fs1", "fs2", "fs3", "fs4", "fifth", "metres", "third")] + [round(B["basin"] + .5, 2), round(B["rice"] + .8, 2)]
SFX["boom"] += [9.15]
SFX["tick"] += [round(B["altog"] + .6 + .45 * i, 2) for i in range(9)]
P = {"B": B, "K": K, "SEG": SEG, "CH": CH, "END": END, "SFX": SFX}
out = os.path.join(ROOT, "engine/ep2/assets"); json.dump(P, open(os.path.join(out, "plan.json"), "w"))
open(os.path.join(out, "plan.js"), "w").write("window.PLAN=" + json.dumps(P) + ";")
print(len(B), "anchors;", len(K), "camera keys; last anchor", B["lastw"])
