import json, sys
src, out = sys.argv[1], sys.argv[2]
def rnd(c, n):
    if isinstance(c[0], (int, float)): return [round(c[0], n), round(c[1], n)]
    return [rnd(x, n) for x in c]
def polys(g): return g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
def F(a3, coords, n, extra=None):
    p = {"a": a3}; p.update(extra or {})
    return {"type": "Feature", "properties": p, "geometry": {"type": "MultiPolygon", "coordinates": rnd(coords, n)}}
w110 = json.load(open(f"{src}/ne_110m_admin_0_countries.geojson"))
w50 = json.load(open(f"{src}/ne_50m_admin_0_countries.geojson"))
w10 = json.load(open(f"{src}/ne_10m_admin_0_countries.geojson"))
lk = json.load(open(f"{src}/ne_10m_lakes.geojson"))
st = json.load(open(f"{src}/ne_50m_admin_1_states_provinces_lakes.geojson"))
D = {}
D["w110"] = [F(f["properties"]["ADM0_A3"], polys(f["geometry"]), 2) for f in w110["features"]]
D["w50"] = [F(f["properties"]["ADM0_A3"], polys(f["geometry"]), 2, {"c": f["properties"].get("CONTINENT")}) for f in w50["features"]]
REG = {"bering": (-180, -160, 60, 70, ["RUS", "USA"], 4), "detroit": (-84, -82, 41.6, 43, ["USA", "CAN"], 4),
       "proberts": (-124, -122.4, 48.6, 49.4, ["USA", "CAN"], 4), "istanbul": (28.3, 29.9, 40.7, 41.6, ["TUR", "GRC", "BGR"], 4),
       "rome": (12.2, 12.7, 41.7, 42.1, ["VAT", "ITA"], 5), "deadsea": (34.5, 36.5, 30.5, 32.5, ["ISR", "JOR", "PSX", "PSE", "EGY"], 4),
       "baarle": (4.5, 5.5, 51.1, 51.8, ["BEL", "NLD"], 4)}
D["r10"] = []
for name, (x0, x1, y0, y1, a3s, n) in REG.items():
    for f in w10["features"]:
        a = f["properties"]["ADM0_A3"]
        if a not in a3s: continue
        keep = [p for p in polys(f["geometry"]) if any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in p[0])]
        if keep: D["r10"].append(F(a, keep, n, {"r": name}))
D["lakes"] = [F(f["properties"]["name"], polys(f["geometry"]), 4) for f in lk["features"] if f["properties"].get("name") in ("Lake Baikal", "Dead Sea", "Lake Erie", "Lake St. Clair", "Lake Huron")]
D["states"] = [F(f["properties"]["name"], polys(f["geometry"]), 3) for f in st["features"] if f["properties"].get("adm0_a3") == "USA" and f["properties"].get("name") in ("California", "Nevada", "Oregon", "Arizona", "Utah", "Idaho")]
open(out, "w").write("window.G=" + json.dumps(D, separators=(",", ":")) + ";")
print({k: len(v) for k, v in D.items()}, sorted({f["properties"]["a"] + ":" + f["properties"]["r"] for f in D["r10"]}))
