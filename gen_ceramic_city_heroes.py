#!/usr/bin/env python3
"""Generate hero images for تركيب-سيراميك city pages via fal.ai"""

import json, os, sys, urllib.request, urllib.error

FAL_API_KEY = "ff27ffc3-2e6d-4f2d-b19b-e2a241239b0d:968d18c810e7d0e0aba234d9d401b8ef"
FAL_ENDPOINT = "https://fal.run/fal-ai/flux/dev"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    {
        "slug": "تركيب-سيراميك-دبي",
        "city_en": "Dubai",
        "city_ar": "دبي",
        "prompt": (
            "Professional ceramic tile installation in a modern Dubai apartment living room. "
            "Expert UAE technician in clean white uniform carefully placing large-format 60x60cm "
            "grey porcelain floor tiles using laser level. Marina-style interior with floor-to-ceiling "
            "windows, precise 2mm grout lines, professional tools visible. "
            "Photorealistic editorial photography, soft natural daylight, clean professional environment. "
            "No text, no watermarks."
        ),
    },
    {
        "slug": "تركيب-سيراميك-أبوظبي",
        "city_en": "Abu Dhabi",
        "city_ar": "أبوظبي",
        "prompt": (
            "Professional ceramic tile installation in a spacious Abu Dhabi villa majlis. "
            "Expert UAE technician in clean uniform laying large-format white marble-look porcelain "
            "tiles 80x80cm on villa floor. Traditional-modern Gulf interior, wide open space, "
            "laser level tool visible, perfectly aligned grout lines. "
            "Photorealistic editorial photography, warm natural lighting. No text, no watermarks."
        ),
    },
    {
        "slug": "تركيب-سيراميك-الشارقة",
        "city_en": "Sharjah",
        "city_ar": "الشارقة",
        "prompt": (
            "Professional ceramic tile installation in a Sharjah family apartment. "
            "Expert UAE technician in clean uniform installing beige porcelain floor tiles 60x60cm "
            "in a bright family living room. Middle-class UAE apartment interior, careful tile placement, "
            "precision spacers visible, freshly grouted clean lines. "
            "Photorealistic editorial photography, bright natural lighting. No text, no watermarks."
        ),
    },
    {
        "slug": "تركيب-سيراميك-عجمان",
        "city_en": "Ajman",
        "city_ar": "عجمان",
        "prompt": (
            "Professional ceramic tile installation in an Ajman residential apartment. "
            "Expert UAE technician in clean uniform laying white ceramic floor tiles 40x40cm "
            "in a clean bright apartment room. Affordable UAE residential interior, careful tile "
            "alignment with laser level, clean grout lines, professional tools. "
            "Photorealistic editorial photography, natural daylight. No text, no watermarks."
        ),
    },
]

HERO_SIZE = {"width": 680, "height": 760}


def generate_image(prompt, api_key):
    payload = json.dumps({
        "prompt": prompt,
        "image_size": HERO_SIZE,
        "num_images": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        FAL_ENDPOINT,
        data=payload,
        headers={"Authorization": f"Key {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["images"][0]["url"]


def download_image(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as resp:
        with open(dest, "wb") as f:
            f.write(resp.read())


for page in PAGES:
    slug = page["slug"]
    out_path = os.path.join(BASE_DIR, slug, "hero.jpg")

    # Skip if already exists
    if os.path.exists(out_path):
        print(f"  SKIP  {slug}/hero.jpg (already exists)")
        continue

    print(f"\n  Generating hero for {slug} ({page['city_en']})...")
    try:
        url = generate_image(page["prompt"], FAL_API_KEY)
        print(f"  Downloading -> {slug}/hero.jpg")
        download_image(url, out_path)
        print(f"  ✅ Saved: {out_path}")
    except Exception as e:
        print(f"  ❌ ERROR for {slug}: {e}", file=sys.stderr)

print("\nDone.")
