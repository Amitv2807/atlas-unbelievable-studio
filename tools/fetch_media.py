"""Fetch free-to-reuse photos and video clips for Atlas Unbelievable, with attribution.
  python fetch_media.py commons "Lake Baikal" --type image|video --n 5 --out DIR
  python fetch_media.py nasa "earth from space station" --type image|video --n 3 --out DIR
Only public domain / CC0 / CC BY / CC BY-SA are accepted (no NC, no ND: the channel is monetized).
Every download is logged to DIR/credits.json and DIR/CREDITS.txt (paste the lines into the video description).
Videos are downloaded with yt-dlp."""
import sys, os, re, json, argparse, subprocess, urllib.request, urllib.parse, html
def _contact():
    c = os.environ.get("ATLAS_CONTACT", "").strip()
    p = os.path.expanduser("~/.atlas_contact")
    if not c and os.path.exists(p): c = open(p).read().strip()
    return c
_C = _contact()
UA = {"User-Agent": "AtlasMediaFetcher/1.0 (educational videos" + ("; " + _C if _C else "") + ")"}
YTDLP = os.path.join(os.path.dirname(sys.executable), "yt-dlp")
OK = re.compile(r"^(public domain|pd|cc0|cc[- ]by(-sa)?[- ]?\d|cc[- ]by(-sa)?$)", re.I)
import time
def safe(url):
    u = urllib.parse.urlsplit(url); return urllib.parse.urlunsplit((u.scheme, u.netloc, urllib.parse.quote(urllib.parse.unquote(u.path)), u.query, u.fragment))
def fetch_bytes(url, timeout=60):
    for k in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(safe(url), headers=UA), timeout=timeout) as r: data = r.read()
            time.sleep(1.0); return data
        except urllib.error.HTTPError as e:
            if e.code in (429, 503): w = int(e.headers.get("Retry-After") or 0) or 5 * (k + 1); print(f"  rate-limited, waiting {w}s"); time.sleep(w); continue
            raise
    raise RuntimeError("gave up after retries: " + url)
def get(url): return json.loads(fetch_bytes(url, 40))
def strip(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
def log(out, rec):
    p = os.path.join(out, "credits.json"); data = json.load(open(p)) if os.path.exists(p) else []
    data.append(rec); json.dump(data, open(p, "w"), indent=1)
    with open(os.path.join(out, "CREDITS.txt"), "a") as f: f.write(f"{rec['title']} — {rec['author']} — {rec['license']} — {rec['source']}\n")
def ytdlp(url, dest):
    r = subprocess.run([YTDLP, "-q", "--no-playlist", "--user-agent", UA["User-Agent"], "-f", "bv*[height<=1080]+ba/b[height<=1080]/b", "--merge-output-format", "mp4", "-o", dest, url], capture_output=True, text=True)
    return r.returncode == 0, r.stderr.strip()[-300:]
def commons(q, typ, n, out):
    ft = "bitmap" if typ == "image" else "video"
    s = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": f"{q} filetype:{ft}",
        "gsrnamespace": 6, "gsrlimit": 30, "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 1920, "format": "json"}))
    got = 0
    for p in sorted(s.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = p["imageinfo"][0]; md = ii.get("extmetadata", {}); lic = strip(md.get("LicenseShortName", {}).get("value"))
        if not OK.match(lic) or re.search(r"\b(nc|nd)\b", lic, re.I): print("  skip (license):", lic, "|", p["title"]); continue
        name = re.sub(r"[^\w.-]+", "_", p["title"][5:])[:80]; dest = os.path.join(out, name)
        if typ == "image":
            url = ii.get("thumburl") or ii["url"]; open(dest, "wb").write(fetch_bytes(url))
        else:
            dest = os.path.splitext(dest)[0] + ".mp4"; ok, err = ytdlp(ii["descriptionurl"], dest)
            if not ok:  # fall back to the original file, then convert
                raw = dest + ".src"; open(raw, "wb").write(fetch_bytes(ii["url"], 180))
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", dest], check=True); os.remove(raw)
        log(out, {"file": os.path.basename(dest), "title": p["title"][5:], "author": strip(md.get("Artist", {}).get("value")) or "unknown",
                  "license": lic, "source": ii["descriptionurl"]})
        print("  OK", lic, "|", os.path.basename(dest)); got += 1
        if got >= n: break
def nasa(q, typ, n, out):
    s = get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": typ, "page_size": 20}))
    got = 0
    for it in s["collection"]["items"]:
        d = it["data"][0]; files = get(it["href"]); 
        pick = [f for f in files if f.endswith("~orig.mp4") or f.endswith("~large.jpg")] or [f for f in files if f.endswith((".mp4", ".jpg"))]
        if not pick: continue
        url = safe(pick[0].replace("http://", "https://")); name = re.sub(r"[^\w.-]+", "_", d["nasa_id"])[:80] + (".mp4" if typ == "video" else ".jpg"); dest = os.path.join(out, name)
        if typ == "video":
            ok, err = ytdlp(url, dest)
            if not ok: print("  fail", err); continue
        else: open(dest, "wb").write(fetch_bytes(url))
        log(out, {"file": name, "title": d.get("title", ""), "author": d.get("photographer") or d.get("center") or "NASA", "license": "Public domain (NASA)",
                  "source": f"https://images.nasa.gov/details/{urllib.parse.quote(d['nasa_id'])}"})
        print("  OK NASA |", name); got += 1
        if got >= n: break
ap = argparse.ArgumentParser(); ap.add_argument("src", choices=["commons", "nasa"]); ap.add_argument("query")
ap.add_argument("--type", default="image", choices=["image", "video"]); ap.add_argument("--n", type=int, default=3); ap.add_argument("--out", default="media")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); (commons if a.src == "commons" else nasa)(a.query, a.type, a.n, a.out)
