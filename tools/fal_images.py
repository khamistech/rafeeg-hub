#!/usr/bin/env python3
"""
fal_images.py - Generate service page images via fal.ai API

Usage:
    python tools/fal_images.py --service bathroom-ceramic --city sharjah --slug-en sharjah --api-key KEY
    python tools/fal_images.py --service bathroom-ceramic --city أبوظبي --slug-en abu-dhabi --api-key KEY --hero-only
    python tools/fal_images.py --service bathroom-ceramic --city دبي --slug-en dubai --api-key KEY --ba-only
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Service prompt definitions
# ---------------------------------------------------------------------------
PROMPTS = {
    "bathroom-ceramic": {
        "hero": (
            "Professional bathroom ceramic tile installation in a modern {city} bathroom. "
            "Expert technician in clean uniform installing porcelain tiles on bathroom wall. "
            "Modern UAE bathroom with waterproofing visible. "
            "Photorealistic editorial photography, soft natural lighting."
        ),
        "before_after": (
            "Split comparison image: left side shows old damaged cracked bathroom tiles "
            "with mold in grout and water stains, right side shows newly renovated modern "
            "bathroom with pristine porcelain tiles and new waterproofing. "
            "Professional renovation photography, clean lighting."
        ),
        "image_prefix": "bathroom-ceramic-installation",
        "ba_filename": "ceramic-before-after.jpg",
        "slug_prefix": "تركيب-سيراميك-حمامات",
    },
    "wall-ceramic": {
        "hero": (
            "Professional wall ceramic tile installation in a modern {city} living room. "
            "Expert technician in clean uniform carefully placing large-format ceramic tiles on a wall. "
            "Modern UAE interior with precision leveling tools visible. "
            "Photorealistic editorial photography, soft natural lighting, clean professional environment."
        ),
        "before_after": (
            "Split comparison image: left side shows old damaged cracked wall tiles "
            "with peeling grout and water stains on a UAE home wall, right side shows beautifully "
            "renovated wall with pristine modern ceramic tiles perfectly aligned and grouted. "
            "Professional renovation photography, clean lighting."
        ),
        "image_prefix": "wall-ceramic-installation",
        "ba_filename": "wall-ceramic-before-after.jpg",
        "slug_prefix": "تركيب-سيراميك-جدران",
    },
    "kitchen-ceramic": {
        "hero": (
            "Professional kitchen ceramic tile installation in a modern {city} kitchen. "
            "Expert technician in clean uniform installing anti-slip porcelain floor tiles. "
            "Modern UAE kitchen with splash back tiles and grease-resistant wall tiles visible. "
            "Photorealistic editorial photography, warm natural lighting, clean professional environment."
        ),
        "before_after": (
            "Split comparison image: left side shows old stained cracked kitchen tiles "
            "with greasy grout and worn floor tiles in a UAE home kitchen, right side shows "
            "beautifully renovated kitchen with pristine anti-slip porcelain floor and "
            "modern splash back tiles perfectly aligned. "
            "Professional renovation photography, clean lighting."
        ),
        "image_prefix": "kitchen-ceramic-installation",
        "ba_filename": "kitchen-ceramic-before-after.jpg",
        "slug_prefix": "تركيب-سيراميك-مطابخ",
    },
    "floor-ceramic": {
        "hero": (
            "Professional floor ceramic tile installation in a modern {city} home. "
            "Expert technician in clean uniform laying large-format porcelain floor tiles with laser level. "
            "Modern UAE living room with perfectly aligned floor tiles and clean grout lines visible. "
            "Photorealistic editorial photography, soft natural lighting, clean professional environment."
        ),
        "before_after": (
            "Split comparison image: left side shows old worn cracked floor tiles "
            "with dirty grout lines and uneven surface in a UAE home, right side shows "
            "beautifully renovated floor with pristine large-format porcelain tiles "
            "perfectly leveled and grouted with uniform spacing. "
            "Professional renovation photography, clean lighting."
        ),
        "image_prefix": "floor-ceramic-installation",
        "ba_filename": "floor-ceramic-before-after.jpg",
        "slug_prefix": "تركيب-سيراميك-أرضيات",
    },
    "small-bathroom-ceramic": {
        "hero": (
            "Professional small bathroom ceramic tile installation in a compact modern {city} bathroom. "
            "Expert technician in clean uniform installing large-format white porcelain tiles on walls and floor. "
            "Small UAE bathroom 4 square meters with visual enlargement technique, anti-slip tiles, waterproofing layer visible. "
            "Photorealistic editorial photography, bright lighting, clean professional environment."
        ),
        "before_after": (
            "Split comparison image: left side shows a cramped small bathroom with old dark cracked small tiles "
            "making it look tiny, right side shows the same small bathroom renovated with large-format white "
            "porcelain tiles on walls and floor making it look spacious and modern. "
            "Professional renovation photography, bright clean lighting."
        ),
        "image_prefix": "small-bathroom-ceramic-installation",
        "ba_filename": "small-bathroom-ceramic-before-after.jpg",
        "slug_prefix": "تركيب-سيراميك-حمامات-صغيرة",
    },
    "rak-ceramic": {
        "hero": (
            "Professional RAK Ceramics tile installation in a luxury {city} home. "
            "Expert technician in clean uniform installing premium large-format RAK porcelain tiles on floor. "
            "Showroom-quality finish with perfectly aligned grout lines, modern UAE interior design. "
            "Photorealistic editorial photography, bright natural lighting, clean professional environment."
        ),
        "before_after": (
            "Split comparison image: left side shows old worn outdated floor tiles with cracked grout "
            "and uneven surface in a UAE home, right side shows stunning premium RAK Ceramics porcelain "
            "large-format tiles perfectly installed with precise grout lines and mirror-like finish. "
            "Professional renovation photography, bright clean lighting."
        ),
        "image_prefix": "rak-ceramic-installation",
        "ba_filename": "rak-ceramic-before-after.jpg",
        "slug_prefix": "سيراميك-راس-الخيمة",
    },
    # Future services can be added here
}

# ---------------------------------------------------------------------------
# Image specs
# ---------------------------------------------------------------------------
HERO_SIZE = {"width": 680, "height": 760}
BA_SIZE = {"width": 1024, "height": 576}
FAL_ENDPOINT = "https://fal.run/fal-ai/flux/dev"


def generate_image(prompt: str, size: dict, api_key: str) -> str:
    """Call fal.ai API and return the image URL."""
    payload = json.dumps({
        "prompt": prompt,
        "image_size": size,
        "num_images": 1,
    }).encode("utf-8")

    req = urllib.request.Request(
        FAL_ENDPOINT,
        data=payload,
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR  fal.ai returned HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"  ERROR  Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    images = data.get("images", [])
    if not images:
        print("  ERROR  No images returned from fal.ai", file=sys.stderr)
        sys.exit(1)

    return images[0]["url"]


def download_image(url: str, dest_path: str) -> None:
    """Download an image from *url* and save to *dest_path*."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(dest_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
    except Exception as e:
        print(f"  ERROR  Failed to download image: {e}", file=sys.stderr)
        sys.exit(1)


def run(service: str, city: str, slug_en: str, api_key: str,
        hero_only: bool = False, ba_only: bool = False) -> None:
    """Generate and download the requested images."""

    if service not in PROMPTS:
        print(f"  ERROR  Unknown service '{service}'. Available: {', '.join(PROMPTS.keys())}")
        sys.exit(1)

    cfg = PROMPTS[service]
    slug_prefix = cfg["slug_prefix"]

    # Output directory: html_v2/{slug_prefix}-{city}/
    # This matches the folder created by build.py (uses Arabic city name, not slug_en)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # html_v2/
    out_dir = os.path.join(base_dir, f"{slug_prefix}-{city}")

    print(f"\n  Service : {service}")
    print(f"  City    : {city}")
    print(f"  Slug    : {slug_en}")
    print(f"  Output  : {out_dir}\n")

    # -- Hero image ----------------------------------------------------------
    if not ba_only:
        hero_prompt = cfg["hero"].format(city=city)
        hero_filename = f"{cfg['image_prefix']}-{slug_en}.jpg"
        hero_path = os.path.join(out_dir, hero_filename)

        print(f"  Generating hero image ({HERO_SIZE['width']}x{HERO_SIZE['height']})...")
        hero_url = generate_image(hero_prompt, HERO_SIZE, api_key)
        print(f"  Downloading -> {hero_filename}")
        download_image(hero_url, hero_path)
        print(f"  Hero image saved: {hero_path}\n")

    # -- Before/After image --------------------------------------------------
    if not hero_only:
        ba_prompt = cfg["before_after"]
        ba_filename = cfg["ba_filename"]
        ba_path = os.path.join(out_dir, ba_filename)

        print(f"  Generating before/after image ({BA_SIZE['width']}x{BA_SIZE['height']})...")
        ba_url = generate_image(ba_prompt, BA_SIZE, api_key)
        print(f"  Downloading -> {ba_filename}")
        download_image(ba_url, ba_path)
        print(f"  Before/after image saved: {ba_path}\n")

    print("  Done!\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate service page images via fal.ai"
    )
    parser.add_argument("--service", required=True,
                        help=f"Service key ({', '.join(PROMPTS.keys())})")
    parser.add_argument("--city", required=True,
                        help="City name used in prompts (English or Arabic)")
    parser.add_argument("--slug-en", required=True,
                        help="English slug for filenames (e.g. sharjah, abu-dhabi)")
    parser.add_argument("--api-key", required=True,
                        help="fal.ai API key")
    parser.add_argument("--hero-only", action="store_true",
                        help="Generate hero image only")
    parser.add_argument("--ba-only", action="store_true",
                        help="Generate before/after image only")

    args = parser.parse_args()

    if args.hero_only and args.ba_only:
        print("  ERROR  Cannot use --hero-only and --ba-only together", file=sys.stderr)
        sys.exit(1)

    run(
        service=args.service,
        city=args.city,
        slug_en=args.slug_en,
        api_key=args.api_key,
        hero_only=args.hero_only,
        ba_only=args.ba_only,
    )


if __name__ == "__main__":
    main()
