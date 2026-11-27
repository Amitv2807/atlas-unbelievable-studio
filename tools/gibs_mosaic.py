"""Build a sharp regional satellite texture with baked-in terrain shading from NASA GIBS.
Usage: python gibs_mosaic.py LON0 LAT0 LON1 LAT1 OUT.jpg [--level 7] [--relief-level 9] [--relief 0.55]
Imagery: NASA Blue Marble Next Generation (500 m) via GIBS; terrain: ASTER GDEM shaded relief. NASA imagery is public domain.
Writes OUT.jpg plus OUT.json with the exact bbox for the renderer."""
import sys, io, json, math, argparse, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
B = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best"
LAYERS = {"bmng": ("BlueMarble_NextGeneration/default/2004-08-01/500m", 7, ".jpeg"),
          "relief": ("ASTER_GDEM_Greyscale_Shaded_Relief/default/2000-03-01/31.25m", 11, ".jpeg")}
def fetch(url):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return Image.open(io.BytesIO(r.read())).convert("RGB")
        except Exception: pass
    return None
def mosaic(layer, level, lon0, lat0, lon1, lat1):
    path, maxl, ext = LAYERS[layer]; level = min(level, maxl)
    res = 0.5625 / 2**level; span = 512 * res
    c0, c1 = int((lon0+180)//span), int((lon1+180)//span); r0, r1 = int((90-lat1)//span), int((90-lat0)//span)
    jobs = {(r, c): f"{B}/{path}/{level}/{r}/{c}{ext}" for r in range(r0, r1+1) for c in range(c0, c1+1)}
    if len(jobs) > 400: raise SystemExit(f"too many tiles ({len(jobs)}); lower the level")
    im = Image.new("RGB", ((c1-c0+1)*512, (r1-r0+1)*512))
    with cf.ThreadPoolExecutor(16) as ex:
        for (r, c), t in zip(jobs, ex.map(fetch, jobs.values())):
            if t: im.paste(t.resize((512, 512)), ((c-c0)*512, (r-r0)*512))
    gx0, gy0 = c0*span-180, 90-r0*span
    box = (round((lon0-gx0)/res), round((gy0-lat1)/res), round((lon1-gx0)/res), round((gy0-lat0)/res))
    return im.crop(box), len(jobs), res
ap = argparse.ArgumentParser(); ap.add_argument("lon0", type=float); ap.add_argument("lat0", type=float); ap.add_argument("lon1", type=float); ap.add_argument("lat1", type=float)
ap.add_argument("out"); ap.add_argument("--level", type=int, default=7); ap.add_argument("--relief-level", type=int, default=9); ap.add_argument("--relief", type=float, default=0.55); ap.add_argument("--max-width", type=int, default=4096)
a = ap.parse_args()
img, n1, res = mosaic("bmng", a.level, a.lon0, a.lat0, a.lon1, a.lat1)
rel, n2, _ = mosaic("relief", a.relief_level, a.lon0, a.lat0, a.lon1, a.lat1)
W = min(max(img.width, rel.width), a.max_width); H = round(W * img.height / img.width)
col = np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32)
hs = np.asarray(rel.resize((W, H), Image.LANCZOS).convert("L")).astype(np.float32) / 255.0
valid = hs > 0.02; mu = hs[valid].mean() if valid.any() else 0.5; hs = np.where(valid, hs, mu)   # no-data (sea) = flat
shade = 1.0 + a.relief * (hs - mu) * 2.2           # emboss mountains/valleys around the mean
out = np.clip(col * shade[..., None] * 1.08, 0, 255)
r_, g_, b_ = out[..., 0], out[..., 1], out[..., 2]; L = 0.3*r_ + 0.59*g_ + 0.11*b_
m = (np.clip((70 - L) / 40, 0, 1) * ((b_ >= r_*0.9) & (b_ >= g_*0.75))).astype(np.float32)   # dark bluish = water
from PIL import ImageFilter; m = np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(2, W/img.width*0.8)))).astype(np.float32)/255.0
ocean = np.array([16, 74, 122], np.float32); out = out*(1-m[..., None]) + ocean*(0.75 + 0.5*L[..., None]/70)*m[..., None]
out = np.clip(out, 0, 255).astype(np.uint8)
Image.fromarray(out).save(a.out, quality=90)
json.dump({"bbox": [a.lon0, a.lat0, a.lon1, a.lat1], "w": W, "h": H, "src": "NASA Blue Marble NG + ASTER GDEM shaded relief (GIBS)", "km_per_px": round(111.32*(a.lon1-a.lon0)/W*math.cos(math.radians((a.lat0+a.lat1)/2)), 3)},
          open(a.out.rsplit(".", 1)[0] + ".json", "w"))
print(f"{a.out}: {W}x{H}px, {n1}+{n2} tiles, ~{111.32*(a.lon1-a.lon0)/W*math.cos(math.radians((a.lat0+a.lat1)/2)):.2f} km/px")
