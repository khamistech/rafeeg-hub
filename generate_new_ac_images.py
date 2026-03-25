#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate AI images for the new AC pages using fal.ai flux/schnell:
- تركيب-مكيفات-عجمان
- شحن-فريون-مكيفات-عجمان
- تصليح-مكيفات-سبلت (دبي، الشارقة، عجمان)
- تنظيف-دكتات-مكيفات (دبي، الشارقة، عجمان)
- Hub pages (تصليح-مكيفات-سبلت/, تنظيف-دكتات-مكيفات/)
"""
import requests, os, time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

FAL_KEY = "ff27ffc3-2e6d-4f2d-b19b-e2a241239b0d:968d18c810e7d0e0aba234d9d401b8ef"
FAL_URL = "https://fal.run/fal-ai/flux/schnell"
HEADERS = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}


def fal_generate(prompt, width, height, seed):
    payload = {
        "prompt": prompt,
        "image_size": {"width": width, "height": height},
        "num_inference_steps": 8,
        "guidance_scale": 3.5,
        "seed": seed,
    }
    for attempt in range(3):
        try:
            r = requests.post(FAL_URL, headers=HEADERS, json=payload, timeout=120)
            if r.status_code == 200:
                data = r.json()
                img_url = data["images"][0]["url"]
                img_r = requests.get(img_url, timeout=30)
                if img_r.status_code == 200:
                    return img_r.content
            else:
                print(f"      fal error {r.status_code}: {r.text[:100]}")
        except Exception as e:
            print(f"      attempt {attempt+1} error: {e}")
        if attempt < 2:
            time.sleep(3)
    return None


def save_pair(img_bytes, base_path, target_w, target_h):
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    scale = max(target_w / img.width, target_h / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - target_w) // 2
    y = (nh - target_h) // 2
    img = img.crop((x, y, x + target_w, y + target_h))
    img.save(base_path + ".jpg", "JPEG", quality=88, optimize=True)
    img.save(base_path + ".webp", "WEBP", quality=82, method=6)
    kj = os.path.getsize(base_path + ".jpg") // 1024
    kw = os.path.getsize(base_path + ".webp") // 1024
    print(f"      → {base_path.split('/')[-2]}/{base_path.split('/')[-1]}  jpg={kj}KB  webp={kw}KB")
    return img


def make_ba_composite(before_bytes, after_bytes, out_base):
    W, H = 1408, 768
    half = W // 2

    def crop_half(data):
        img = Image.open(BytesIO(data)).convert("RGB")
        sc = max(half / img.width, H / img.height)
        nw, nh = int(img.width * sc), int(img.height * sc)
        img = img.resize((nw, nh), Image.LANCZOS)
        x = (nw - half) // 2
        y = (nh - H) // 2
        return img.crop((x, y, x + half, y + H))

    canvas = Image.new("RGB", (W, H))
    canvas.paste(crop_half(before_bytes), (0, 0))
    canvas.paste(crop_half(after_bytes), (half, 0))

    draw = ImageDraw.Draw(canvas)
    draw.line([(half, 0), (half, H)], fill=(255, 255, 255), width=4)
    cx, cy, r = half, H // 2, 30
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255))
    draw.polygon([(cx-10, cy-14), (cx+12, cy), (cx-10, cy+14)], fill=(40, 40, 40))

    try:
        fn = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if not os.path.exists(fn):
            fn = "/System/Library/Fonts/Arial.ttf"
        font = ImageFont.truetype(fn, 34)
    except:
        font = ImageFont.load_default()

    pad = 14
    for text, fg, bg, side in [
        ("BEFORE", (255,255,255), (180,30,30), "left"),
        ("AFTER",  (255,255,255), (30,140,50),  "right"),
    ]:
        bb = draw.textbbox((0, 0), text, font=font)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        if side == "left":
            x0 = 20
        else:
            x0 = W - 20 - tw - pad*2
        y0 = 20
        draw.rectangle([x0, y0, x0+tw+pad*2, y0+th+pad], fill=bg)
        draw.text((x0+pad, y0+pad//2), text, fill=fg, font=font)

    canvas.save(out_base + ".jpg", "JPEG", quality=88, optimize=True)
    canvas.save(out_base + ".webp", "WEBP", quality=82, method=6)
    kj = os.path.getsize(out_base + ".jpg") // 1024
    kw = os.path.getsize(out_base + ".webp") // 1024
    print(f"      → BA composite  jpg={kj}KB  webp={kw}KB")


# ── New pages to generate ────────────────────────────────────────────────────

# AC split repair (تصليح مكيفات سبلت)
TASLEEH_HERO = "professional UAE AC technician in uniform diagnosing split air conditioner unit with tools, modern apartment, focused repair work, portrait orientation, photorealistic"
TASLEEH_BEFORE = "broken split AC unit on apartment wall, red error lights flashing, not cooling, indoor unit dripping water, UAE home, realistic photo"
TASLEEH_AFTER = "repaired functioning split AC unit running perfectly, cool air flowing, green indicator light, clean installation, UAE home, bright"

# AC duct cleaning (تنظيف دكتات)
DUKAT_HERO = "professional HVAC technician in white uniform cleaning air conditioning duct with specialized vacuum equipment, UAE building, portrait orientation, photorealistic"
DUKAT_BEFORE = "dirty dusty air conditioning duct interior with thick layer of dust and debris, clogged ventilation, UAE apartment, realistic photo"
DUKAT_AFTER = "clean sanitized air conditioning duct after professional cleaning, spotless interior, fresh air flow, UAE apartment, bright"

# City suffixes
CITY_SUFFIX = {
    "أبوظبي": "in Abu Dhabi UAE",
    "دبي":    "in Dubai UAE",
    "الشارقة":"in Sharjah UAE",
    "عجمان":  "in Ajman UAE",
}

PAGES = [
    # (slug, service_type, city, seed_base, is_hub, ba_slug_for_reuse)
    # تصليح-مكيفات-سبلت
    ("تصليح-مكيفات-سبلت-دبي",     "tasleeh", "دبي",     8100, False, None),
    ("تصليح-مكيفات-سبلت-الشارقة", "tasleeh", "الشارقة", 8200, False, None),
    ("تصليح-مكيفات-سبلت-عجمان",   "tasleeh", "عجمان",   8300, False, None),
    ("تصليح-مكيفات-سبلت",          "tasleeh", None,      8000, True,  None),
    # تنظيف-دكتات-مكيفات
    ("تنظيف-دكتات-مكيفات-دبي",     "dukat",   "دبي",     9100, False, None),
    ("تنظيف-دكتات-مكيفات-الشارقة", "dukat",   "الشارقة", 9200, False, None),
    ("تنظيف-دكتات-مكيفات-عجمان",   "dukat",   "عجمان",   9300, False, None),
    ("تنظيف-دكتات-مكيفات",          "dukat",   None,      9000, True,  None),
    # تركيب/شحن عجمان (AC install + freon)
    ("تركيب-مكيفات-عجمان",         "tarkib",  "عجمان",   8500, False, None),
    ("شحن-فريون-مكيفات-عجمان",     "freon",   "عجمان",   8600, False, None),
]

# BA prompts per service
BA_PROMPTS = {
    "tasleeh": (TASLEEH_BEFORE, TASLEEH_AFTER),
    "dukat":   (DUKAT_BEFORE,  DUKAT_AFTER),
    "tarkib": (
        "wall with no air conditioner, just brackets and copper pipes ready for installation, UAE apartment, realistic photo",
        "brand new split air conditioner perfectly installed on wall, running cold air, UAE apartment, bright professional installation"
    ),
    "freon": (
        "AC technician measuring refrigerant pressure, low freon reading on gauge, UAE apartment, not cooling, realistic photo",
        "AC technician refilling refrigerant freon with certified equipment, UAE apartment, proper servicing complete, bright"
    ),
}

HERO_PROMPTS = {
    "tasleeh": TASLEEH_HERO,
    "dukat":   DUKAT_HERO,
    "tarkib":  "professional Arab AC installation technician in uniform mounting split AC unit on wall bracket, UAE apartment, portrait orientation, photorealistic",
    "freon":   "professional AC technician in uniform connecting refrigerant freon gas cylinder to split air conditioner, UAE apartment, portrait orientation, photorealistic",
}


def main():
    total_calls = 0

    # Generate shared BA images per service type
    ba_cache = {}
    service_types = list({p[1] for p in PAGES})

    print("\n=== Generating Before/After composites ===\n")
    for svc in service_types:
        if svc in ba_cache:
            continue
        before_prompt, after_prompt = BA_PROMPTS[svc]
        seed_before = {"tasleeh": 8050, "dukat": 9050, "tarkib": 8550, "freon": 8650}[svc]

        print(f"\n  [{svc}] BEFORE...", end=" ", flush=True)
        b_data = fal_generate(before_prompt, 704, 768, seed_before)
        total_calls += 1
        if not b_data:
            print("❌ failed")
            continue
        print("✅")
        time.sleep(1)

        print(f"  [{svc}] AFTER...", end=" ", flush=True)
        a_data = fal_generate(after_prompt, 704, 768, seed_before + 10)
        total_calls += 1
        if not a_data:
            print("❌ failed")
            continue
        print("✅")
        time.sleep(1)

        ba_cache[svc] = (b_data, a_data)

    # Write BA composites + generate heroes
    print("\n\n=== Generating hero images ===\n")
    for slug, svc, city, seed, is_hub, _ in PAGES:
        page_dir = slug
        os.makedirs(page_dir, exist_ok=True)

        # Write BA composite (same for all cities of a service)
        if svc in ba_cache:
            b_data, a_data = ba_cache[svc]
            print(f"  [{slug}] BA composite...", end=" ", flush=True)
            make_ba_composite(b_data, a_data, f"{page_dir}/ac-before-after")
        else:
            print(f"  [{slug}] BA skipped (generation failed)")

        # Hero image
        hero_base = HERO_PROMPTS[svc]
        if city:
            hero_prompt = hero_base + f", {CITY_SUFFIX[city]}"
        else:
            hero_prompt = hero_base + ", UAE"

        print(f"  [{slug}] hero...", end=" ", flush=True)
        hero_data = fal_generate(hero_prompt, 768, 1376, seed)
        total_calls += 1
        if hero_data:
            print("✅")
            save_pair(hero_data, f"{page_dir}/hero", 768, 1376)
        else:
            print("❌")
        time.sleep(1)

    print(f"\n✅ Done — {total_calls} fal.ai calls")


if __name__ == "__main__":
    main()
