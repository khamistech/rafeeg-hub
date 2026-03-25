#!/usr/bin/env python3
"""
Download real photos from loremflickr.com for all service pages.
Uses keyword-based search with lock seeds for consistent, service-appropriate images.
"""
import urllib.request, ssl, os, time, json

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

# service slug → (hero_keywords, before_after_keywords, hero_lock, ba_lock)
SERVICE_IMAGES = {
    "تسليك-مواسير":   ("plumbing,pipes,plumber",       "drain,pipe,water",      10, 20),
    "أعمال-كهربائية": ("electrician,electrical,wiring", "electricity,panel,wire", 30, 40),
    "نجارة-وديكور":   ("carpentry,wood,interior",       "furniture,woodwork",    50, 60),
    "دهان":           ("painting,painter,wall",          "paint,brush,interior",  70, 80),
    "تركيب-غاز":      ("appliances,kitchen,technician", "gas,stove,repair",      90, 100),
    "صيانة-عامة":     ("handyman,tools,repair,home",    "maintenance,worker",    110, 120),
    "مكافحة-حشرات":   ("pest,spray,control,insect",     "cleaning,spray,home",   130, 140),
}

CITIES = ["أبوظبي", "دبي", "الشارقة", "عجمان"]
CITY_OFFSETS = {"أبوظبي": 0, "دبي": 1, "الشارقة": 2, "عجمان": 3}


def download_image(keywords, lock, width, height, out_path):
    """Download image from loremflickr with retry."""
    url = f"https://loremflickr.com/{width}/{height}/{keywords}?lock={lock}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            resp = urllib.request.urlopen(req, context=ctx, timeout=20)
            data = resp.read()
            if len(data) < 5000:
                raise ValueError(f"Image too small: {len(data)} bytes")
            with open(out_path, 'wb') as f:
                f.write(data)
            return True
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                print(f"    ⚠️  Failed after 3 attempts: {e}")
                return False
    return False


def main():
    total = 0
    success = 0

    # 1. Hub pages (7)
    print("\n=== Hub Pages ===")
    for service_slug, (hero_kw, ba_kw, hero_lock, ba_lock) in SERVICE_IMAGES.items():
        os.makedirs(service_slug, exist_ok=True)

        # Hero image
        total += 1
        path = f"{service_slug}/hero.jpg"
        print(f"  Downloading {service_slug}/hero.jpg ...", end=' ', flush=True)
        if download_image(hero_kw, hero_lock, 1200, 630, path):
            size_kb = os.path.getsize(path) // 1024
            print(f"✅ {size_kb}KB")
            success += 1
        time.sleep(1)

        # Before/after image
        total += 1
        path = f"{service_slug}/ac-before-after.jpg"
        print(f"  Downloading {service_slug}/ac-before-after.jpg ...", end=' ', flush=True)
        if download_image(ba_kw, ba_lock, 1024, 576, path):
            size_kb = os.path.getsize(path) // 1024
            print(f"✅ {size_kb}KB")
            success += 1
        time.sleep(1)

    # 2. City pages (28: 7 services × 4 cities)
    print("\n=== City Pages ===")
    for service_slug, (hero_kw, ba_kw, hero_lock, ba_lock) in SERVICE_IMAGES.items():
        for city in CITIES:
            page_slug = f"{service_slug}-{city}"
            os.makedirs(page_slug, exist_ok=True)

            # Use city offset to get slightly different image per city
            city_offset = CITY_OFFSETS[city]

            # Hero image
            total += 1
            path = f"{page_slug}/hero.jpg"
            print(f"  Downloading {page_slug}/hero.jpg ...", end=' ', flush=True)
            if download_image(hero_kw, hero_lock + city_offset, 1200, 630, path):
                size_kb = os.path.getsize(path) // 1024
                print(f"✅ {size_kb}KB")
                success += 1
            time.sleep(0.8)

            # Before/after image
            total += 1
            path = f"{page_slug}/ac-before-after.jpg"
            print(f"  Downloading {page_slug}/ac-before-after.jpg ...", end=' ', flush=True)
            if download_image(ba_kw, ba_lock + city_offset, 1024, 576, path):
                size_kb = os.path.getsize(path) // 1024
                print(f"✅ {size_kb}KB")
                success += 1
            time.sleep(0.8)

    print(f"\n{'='*50}")
    print(f"Done: {success}/{total} images downloaded successfully")
    if success < total:
        print(f"⚠️  {total - success} images failed — run script again to retry")


if __name__ == "__main__":
    main()
