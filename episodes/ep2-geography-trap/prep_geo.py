"""Map data for Episode 2 -> engine/ep2/assets/geo.js
python3 episodes/ep2-geography-trap/prep_geo.py /home/user/geo-motion/data engine/ep2/assets/geo.js"""
import json, sys
src, out = sys.argv[1], sys.argv[2]
def rnd(c, n):
    if isinstance(c[0], (int, float)): return [round(c[0], n), round(c[1], n)]
    return [rnd(x, n) for x in c]
def polys(g): return g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
def F(a3, coords, n, extra=None):
    p = {"a": a3}; p.update(extra or {})
    return {"type": "Feature", "properties": p, "geometry": {"type": "MultiPolygon", "coordinates": rnd(coords, n)}}
L = lambda n: json.load(open(f"{src}/{n}.geojson"))
w110, w50, w10 = L("ne_110m_admin_0_countries"), L("ne_50m_admin_0_countries"), L("ne_10m_admin_0_countries")
D = {"w110": [F(f["properties"]["ADM0_A3"], polys(f["geometry"]), 2) for f in w110["features"]],
     "w50": [F(f["properties"]["ADM0_A3"], polys(f["geometry"]), 2, {"c": f["properties"].get("CONTINENT")}) for f in w50["features"]]}
REG = {"sg": (102.8, 105.0, 0.5, 2.2, ["SGP", "MYS", "IDN"], 4), "bos": (25.5, 30.0, 39.5, 41.8, ["TUR", "GRC", "BGR"], 3),
       "gib": (-7, -4.5, 35.3, 36.8, ["ESP", "GBR", "MAR", "GIB"], 4), "bering": (-180, -160, 60, 70, ["RUS", "USA"], 3),
       "vlad": (130.5, 133.5, 42.3, 43.8, ["RUS"], 4), "taiwan": (119, 123, 21.5, 26, ["TWN"], 3)}
D["r10"] = []
for name, (x0, x1, y0, y1, a3s, n) in REG.items():
    for f in w10["features"]:
        a = f["properties"]["ADM0_A3"]
        if a not in a3s: continue
        keep = [p for p in polys(f["geometry"]) if any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in p[0])]
        if keep: D["r10"].append(F(a, keep, n, {"r": name}))
rv = L("ne_10m_rivers_lake_centerlines"); want = {"Yangtze", "Chang Jiang", "Huang", "Indus", "Brahmaputra", "Yarlung", "Sutlej", "Ussuri", "Red", "Hong", "Volga", "Dnipro", "Dnieper", "Vistula", "Wisla", "Oder", "Odra", "Rhine"}
D["rivers"] = []
for f in rv["features"]:
    n = f["properties"].get("name")
    if n not in want: continue
    g = f["geometry"]; ls = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
    if n == "Red" and not any(100 < x < 110 for l in ls for x, y in l): continue
    D["rivers"].append({"type": "Feature", "properties": {"a": n}, "geometry": {"type": "MultiLineString", "coordinates": rnd(ls, 2)}})
st = L("ne_50m_admin_1_states_provinces_lakes")
D["states"] = [F(f["properties"]["name"], polys(f["geometry"]), 2) for f in st["features"] if f["properties"].get("adm0_a3") == "CHN" and f["properties"].get("name") in ("Xinjiang", "Xizang")]
open(out, "w").write("window.G=" + json.dumps(D, separators=(",", ":")) + ";")
print({k: len(v) for k, v in D.items()}, sorted({f["properties"]["a"] for f in D["rivers"]}), sorted({f["properties"]["a"]+":"+f["properties"]["r"] for f in D["r10"]}))
