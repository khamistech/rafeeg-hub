#!/usr/bin/env python3
"""
Generate proper service images matching project standards:
- Hero: portrait 768×1376, professional service worker
- Before/After: landscape 1408×768, left=before(problem), right=after(fixed)
Both downloaded from loremflickr using targeted service keywords.
"""
import urllib.request, ssl, os, time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

# Service → (hero_keywords, before_keywords, after_keywords, hero_lock, before_lock, after_lock)
SERVICES = {
    "تسليك-مواسير": {
        "hero":   ("plumber,drain,professional,worker",   1001),
        "before": ("clogged,dirty,pipe,drain,blocked",    1002),
        "after":  ("clean,pipe,drain,maintenance,fixed",  1003),
    },
    "أعمال-كهربائية": {
        "hero":   ("electrician,wiring,professional,worker", 2001),
        "before": ("old,wiring,electrical,broken,panel",     2002),
        "after":  ("new,electrical,panel,clean,installation",2003),
    },
    "نجارة-وديكور": {
        "hero":   ("carpenter,wood,workshop,craftsman",      3001),
        "before": ("empty,room,wall,bare,unfurnished",       3002),
        "after":  ("furniture,wood,interior,custom,shelf",   3003),
    },
    "دهان": {
        "hero":   ("painter,wall,brush,interior,professional", 4001),
        "before": ("old,peeling,paint,wall,dirty",             4002),
        "after":  ("fresh,paint,wall,clean,interior,bright",   4003),
    },
    "تركيب-غاز": {
        "hero":   ("technician,gas,installation,worker,kitchen", 5001),
        "before": ("kitchen,empty,pipes,old,installation",       5002),
        "after":  ("kitchen,gas,stove,clean,installed",          5003),
    },
    "صيانة-عامة": {
        "hero":   ("handyman,tools,repair,worker,home",    6001),
        "before": ("broken,damaged,wall,home,repair",      6002),
        "after":  ("renovated,fixed,clean,home,interior",  6003),
    },
    "مكافحة-حشرات": {
        "hero":   ("pest,control,spray,technician,worker", 7001),
        "before": ("insects,pest,dirty,infestation,home",  7002),
        "after":  ("clean,spray,pest,free,home,fresh",     7003),
    },
}

CITIES  = ["أبوظبي", "دبي", "الشارقة", "عجمان"]
CITY_OFFSET = {"أبوظبي": 0, "دبي": 10, "الشارقة": 20, "عجمان": 30}

# Target dimensions matching AC pages
HERO_W, HERO_H = 768, 1376
BA_W,   BA_H   = 1408, 768


def fetch_bytes(keywords, lock, w, h):
    """Fetch image bytes from loremflickr with retry."""
    url = f"https://loremflickr.com/{w}/{h}/{keywords}?lock={lock}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            resp = urllib.request.urlopen(req, context=ctx, timeout=25)
            data = resp.read()
            if len(data) < 4000:
                raise ValueError(f"too small ({len(data)}B)")
            return data
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
    return None


def save_jpg_webp(img: Image.Image, base_path: str):
    """Save as both jpg and webp."""
    img.save(base_path + ".jpg", "JPEG", quality=88, optimize=True)
    img.save(base_path + ".webp", "WEBP", quality=82, method=6)
    kb_j = os.path.getsize(base_path + ".jpg") // 1024
    kb_w = os.path.getsize(base_path + ".webp") // 1024
    print(f"      jpg={kb_j}KB  webp={kb_w}KB")


def make_before_after(before_data: bytes, after_data: bytes) -> Image.Image:
    """Create 1408×768 composite: left=before, right=after, with divider + labels."""
    half_w = BA_W // 2

    # Load + crop each half
    def load_half(data):
        img = Image.open(BytesIO(data)).convert("RGB")
        # Fill half_w × BA_H keeping aspect ratio, then center-crop
        scale = max(half_w / img.width, BA_H / img.height)
        new_w = int(img.width * scale)
        new_h = int(img.height * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        x = (new_w - half_w) // 2
        y = (new_h - BA_H)   // 2
        return img.crop((x, y, x + half_w, y + BA_H))

    left  = load_half(before_data)   # before
    right = load_half(after_data)    # after

    canvas = Image.new("RGB", (BA_W, BA_H))
    canvas.paste(left,  (0, 0))
    canvas.paste(right, (half_w, 0))

    draw = ImageDraw.Draw(canvas)

    # Central divider line + arrow
    divider_x = half_w
    draw.line([(divider_x, 0), (divider_x, BA_H)], fill=(255, 255, 255), width=4)

    # Arrow circle in center
    cx, cy, r = divider_x, BA_H // 2, 28
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    # Arrow → right
    draw.polygon([
        (cx - 8, cy - 12), (cx + 8, cy), (cx - 8, cy + 12)
    ], fill=(30, 30, 30))

    # Labels
    try:
        font_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
        font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    except:
        try:
            font_lg = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
            font_sm = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        except:
            font_lg = ImageFont.load_default()
            font_sm = font_lg

    label_y = 24
    pad = 16

    # "BEFORE" badge top-left
    before_txt = "BEFORE"
    bb = draw.textbbox((0, 0), before_txt, font=font_lg)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.rectangle([20, label_y, 20 + tw + pad * 2, label_y + th + pad], fill=(180, 30, 30))
    draw.text((20 + pad, label_y + pad // 2), before_txt, fill=(255, 255, 255), font=font_lg)

    # "AFTER" badge top-right
    after_txt = "AFTER"
    bb2 = draw.textbbox((0, 0), after_txt, font=font_lg)
    tw2, th2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
    ax = BA_W - 20 - tw2 - pad * 2
    draw.rectangle([ax, label_y, ax + tw2 + pad * 2, label_y + th2 + pad], fill=(30, 140, 50))
    draw.text((ax + pad, label_y + pad // 2), after_txt, fill=(255, 255, 255), font=font_lg)

    return canvas


def make_hero(data: bytes) -> Image.Image:
    """Crop/resize to portrait 768×1376."""
    img = Image.open(BytesIO(data)).convert("RGB")
    scale = max(HERO_W / img.width, HERO_H / img.height)
    new_w = int(img.width  * scale)
    new_h = int(img.height * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    x = (new_w - HERO_W) // 2
    y = (new_h - HERO_H) // 2
    return img.crop((x, y, x + HERO_W, y + HERO_H))


def process_dir(slug, svc_data, city_offset):
    os.makedirs(slug, exist_ok=True)
    hero_kw,   hero_lock   = svc_data["hero"]
    before_kw, before_lock = svc_data["before"]
    after_kw,  after_lock  = svc_data["after"]

    # Hero
    print(f"    hero ({hero_kw[:30]})...", end=" ", flush=True)
    hdata = fetch_bytes(hero_kw, hero_lock + city_offset, 900, 1600)
    if hdata:
        save_jpg_webp(make_hero(hdata), f"{slug}/hero")
    else:
        print("❌ failed")
    time.sleep(0.8)

    # Before/After composite
    print(f"    before/after...", end=" ", flush=True)
    bdata = fetch_bytes(before_kw, before_lock + city_offset, 800, 600)
    adata = fetch_bytes(after_kw,  after_lock  + city_offset, 800, 600)
    if bdata and adata:
        save_jpg_webp(make_before_after(bdata, adata), f"{slug}/ac-before-after")
    else:
        print("❌ failed")
    time.sleep(0.8)


def main():
    total_dirs = len(SERVICES) + len(SERVICES) * len(CITIES)
    done = 0

    # 1. Hub pages
    print("\n=== Hub pages ===")
    for svc_slug, svc_data in SERVICES.items():
        print(f"  [{done+1}/{total_dirs}] {svc_slug}/")
        process_dir(svc_slug, svc_data, 0)
        done += 1

    # 2. City pages
    print("\n=== City pages ===")
    for svc_slug, svc_data in SERVICES.items():
        for city in CITIES:
            page_slug = f"{svc_slug}-{city}"
            offset = CITY_OFFSET[city]
            print(f"  [{done+1}/{total_dirs}] {page_slug}/")
            process_dir(page_slug, svc_data, offset)
            done += 1

    print(f"\n✅ Done — {done} directories processed")


if __name__ == "__main__":
    main()
