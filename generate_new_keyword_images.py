#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate fal.ai images for new keyword pages:
- فك-وتركيب-مكيفات (hub + 4 cities)
- مكيف-لا-يبرد (hub + 4 cities)

Hero: 768x1376 portrait — unique per city variant
BA composite: 1408x768 — shared across hub + 4 city pages per service
"""
import os, json, time, requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

BASE = os.path.dirname(os.path.abspath(__file__))
FAL_KEY = "ff27ffc3-2e6d-4f2d-b19b-e2a241239b0d:968d18c810e7d0e0aba234d9d401b8ef"
FAL_URL = "https://fal.run/fal-ai/flux/schnell"
HEADERS = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}


def fal_generate(prompt, width, height, seed=42):
    payload = {
        "prompt": prompt,
        "image_size": {"width": width, "height": height},
        "num_inference_steps": 8,
        "guidance_scale": 3.5,
        "seed": seed,
    }
    r = requests.post(FAL_URL, headers=HEADERS, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    images = data.get("images", [])
    if not images:
        print(f"  ✗ No images in response: {data}")
        return None
    img_url = images[0]["url"]
    img_r = requests.get(img_url, timeout=60)
    img_r.raise_for_status()
    return img_r.content


def save_jpg_and_webp(img_bytes, out_dir, filename_base):
    """Save as .jpg and .webp"""
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    jpg_path = os.path.join(out_dir, f"{filename_base}.jpg")
    webp_path = os.path.join(out_dir, f"{filename_base}.webp")
    img.save(jpg_path, "JPEG", quality=88, optimize=True)
    img.save(webp_path, "WEBP", quality=82, method=6)
    print(f"    saved {jpg_path}")
    return img


def make_ba_composite(before_bytes, after_bytes, out_dir):
    """Create 1408x768 before/after composite"""
    before = Image.open(BytesIO(before_bytes)).convert("RGB").resize((704, 768), Image.LANCZOS)
    after = Image.open(BytesIO(after_bytes)).convert("RGB").resize((704, 768), Image.LANCZOS)

    composite = Image.new("RGB", (1408, 768))
    composite.paste(before, (0, 0))
    composite.paste(after, (704, 0))

    draw = ImageDraw.Draw(composite)

    # White divider line
    draw.line([(703, 0), (703, 768)], fill="white", width=4)
    draw.line([(705, 0), (705, 768)], fill="white", width=4)

    # Arrow in center
    cx, cy = 704, 384
    draw.ellipse([cx-28, cy-28, cx+28, cy+28], fill="white")
    draw.polygon([(cx-8, cy-12), (cx+16, cy), (cx-8, cy+12)], fill="#1a1a2e")

    # BEFORE badge
    draw.rectangle([20, 20, 180, 60], fill=(220, 38, 38))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
    draw.text((30, 28), "BEFORE", fill="white", font=font)

    # AFTER badge
    draw.rectangle([724+20, 20, 724+180, 60], fill=(34, 197, 94))
    draw.text((724+30, 28), "AFTER", fill="white", font=font)

    jpg_path = os.path.join(out_dir, "ac-before-after.jpg")
    webp_path = os.path.join(out_dir, "ac-before-after.webp")
    composite.save(jpg_path, "JPEG", quality=88, optimize=True)
    composite.save(webp_path, "WEBP", quality=82, method=6)
    print(f"    saved composite {jpg_path}")


# ─── Service configs ─────────────────────────────────────────────────────────

SERVICES = {
    "فك-وتركيب-مكيفات": {
        "hero_prompts": {
            None:    "professional Arab HVAC technician in blue uniform carefully dismounting split AC indoor unit from wall bracket in modern UAE living room, precise work, daylight",
            "أبوظبي": "professional Arab technician in uniform carefully removing split AC unit from luxury Abu Dhabi villa wall, clean modern interior, bright lighting",
            "دبي":    "professional Arab HVAC worker in blue uniform carefully lifting AC indoor unit off wall bracket in modern Dubai apartment, professional tools, natural light",
            "الشارقة": "Arab AC technician in uniform dismounting air conditioner unit from wall in Sharjah modern apartment, focused work, clean environment",
            "عجمان":  "professional technician in uniform carefully removing old AC unit from Ajman apartment wall, replacing with new position, bright room",
        },
        "ba_before_prompt": "home interior in UAE with no air conditioning, worker about to dismantle AC unit from wall, empty brackets visible, dusty old unit, hot weather outside",
        "ba_after_prompt":  "same UAE home interior, brand new professionally installed split AC unit on wall in perfect position, clean modern look, cool comfortable room",
        "ba_seed_before": 101,
        "ba_seed_after":  202,
        "hero_seeds": {None: 301, "أبوظبي": 302, "دبي": 303, "الشارقة": 304, "عجمان": 305},
    },
    "مكيف-لا-يبرد": {
        "hero_prompts": {
            None:    "professional Arab HVAC technician in uniform using manifold gauge to check AC refrigerant pressure in UAE home, diagnostic tools, focused expression, daylight",
            "أبوظبي": "professional Arab AC technician in Abu Dhabi apartment checking air conditioner refrigerant level with pressure gauge, technical diagnostic, bright interior",
            "دبي":    "professional HVAC technician in blue uniform checking split AC system refrigerant with gauge in modern Dubai apartment, precise diagnosis",
            "الشارقة": "Arab air conditioning technician checking AC that is not cooling properly in Sharjah home, using diagnostic gauge, professional work",
            "عجمان":  "AC repair technician in uniform diagnosing air conditioner not cooling problem in Ajman residence, tools and gauge, professional look",
        },
        "ba_before_prompt": "hot stuffy UAE room with air conditioner running but not cooling, person sweating, thermometer showing high temperature, air conditioner light blinking fault indicator",
        "ba_after_prompt":  "same UAE room now perfectly cooled, air conditioner working efficiently, comfortable cool atmosphere, person relaxed, temperature display showing 19 degrees",
        "ba_seed_before": 401,
        "ba_seed_after":  402,
        "hero_seeds": {None: 501, "أبوظبي": 502, "دبي": 503, "الشارقة": 504, "عجمان": 505},
    },
}

CITIES_ORDER = [None, "أبوظبي", "دبي", "الشارقة", "عجمان"]


def get_page_dir(service_slug, city):
    if city is None:
        slug = service_slug
    else:
        slug = f"{service_slug}-{city}"
    return os.path.join(BASE, slug)


def main():
    for service_slug, cfg in SERVICES.items():
        print(f"\n{'='*60}")
        print(f"Service: {service_slug}")
        print(f"{'='*60}")

        # 1. Generate BA composite ONCE and share across all city pages
        print(f"\n  Generating BA composite images...")
        before_bytes = fal_generate(cfg["ba_before_prompt"], 704, 768, cfg["ba_seed_before"])
        time.sleep(1)
        after_bytes = fal_generate(cfg["ba_after_prompt"], 704, 768, cfg["ba_seed_after"])
        time.sleep(1)

        if before_bytes and after_bytes:
            # Apply BA to all city dirs
            for city in CITIES_ORDER:
                out_dir = get_page_dir(service_slug, city)
                os.makedirs(out_dir, exist_ok=True)
                make_ba_composite(before_bytes, after_bytes, out_dir)
        else:
            print("  ✗ BA generation failed, skipping")

        # 2. Generate unique hero per city variant
        print(f"\n  Generating hero images...")
        for city in CITIES_ORDER:
            city_label = city or "hub"
            print(f"  Hero for {city_label}...")
            prompt = cfg["hero_prompts"][city]
            seed = cfg["hero_seeds"][city]
            hero_bytes = fal_generate(prompt, 768, 1376, seed)
            time.sleep(1)
            if hero_bytes:
                out_dir = get_page_dir(service_slug, city)
                os.makedirs(out_dir, exist_ok=True)
                save_jpg_and_webp(hero_bytes, out_dir, "hero")
            else:
                print(f"  ✗ Hero failed for {city_label}")

    print("\n✅ All images generated!")


if __name__ == "__main__":
    main()
