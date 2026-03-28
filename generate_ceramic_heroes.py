#!/usr/bin/env python3
"""Generate hero images for ceramic installation city pages using fal.ai API."""

import json
import os
import shutil
import time
import urllib.request

API_KEY = "ff27ffc3-2e6d-4f2d-b19b-e2a241239b0d:968d18c810e7d0e0aba234d9d401b8ef"
API_URL = "https://fal.run/fal-ai/flux/dev"
BASE_DIR = "/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2"

IMAGES = [
    {
        "name": "Dubai hero",
        "prompt": "Professional ceramic tile installation in a modern Dubai apartment. An expert technician in clean uniform carefully laying large format porcelain tiles on a living room floor. Bright natural light from large windows, modern minimalist interior, Dubai Marina towers visible through window. Professional tools visible. Photorealistic, editorial photography style.",
        "size": {"width": 680, "height": 760},
        "path": os.path.join(BASE_DIR, "تركيب-سيراميك-دبي", "hero.jpg"),
    },
    {
        "name": "Abu Dhabi hero",
        "prompt": "Professional ceramic tile installation in a luxury Abu Dhabi villa. Expert worker installing polished porcelain floor tiles in a spacious majlis (sitting room). Traditional Arabic modern interior design, warm lighting, elegant space. Professional tools and level visible. Photorealistic, editorial photography.",
        "size": {"width": 680, "height": 760},
        "path": os.path.join(BASE_DIR, "تركيب-سيراميك-أبوظبي", "hero.jpg"),
    },
    {
        "name": "Sharjah hero",
        "prompt": "Professional bathroom ceramic tile installation in Sharjah apartment. Expert technician installing wall tiles in a modern bathroom renovation. Clean white and grey tiles, professional grouting tools visible. Bright clean workspace. Photorealistic, editorial photography style.",
        "size": {"width": 680, "height": 760},
        "path": os.path.join(BASE_DIR, "تركيب-سيراميك-الشارقة", "hero.jpg"),
    },
    {
        "name": "Ajman hero",
        "prompt": "Professional floor ceramic tile installation in Ajman home. Expert worker laying ceramic floor tiles in a bedroom. Modern UAE home interior, natural lighting, professional equipment. Clean and organized workspace. Photorealistic, editorial photography.",
        "size": {"width": 680, "height": 760},
        "path": os.path.join(BASE_DIR, "تركيب-سيراميك-عجمان", "hero.jpg"),
    },
    {
        "name": "Before-After",
        "prompt": "Split image showing ceramic tile renovation before and after. Left side: old cracked damaged floor tiles, dirty grout, worn surface. Right side: same space with brand new polished ceramic tiles perfectly installed, clean grout lines, gleaming surface. Professional renovation photography, dramatic transformation.",
        "size": {"width": 1024, "height": 576},
        "path": os.path.join(BASE_DIR, "تركيب-سيراميك-دبي", "ceramic-before-after.jpg"),
    },
]

# Folders to copy the before-after image to
BEFORE_AFTER_COPIES = [
    os.path.join(BASE_DIR, "تركيب-سيراميك-أبوظبي", "ceramic-before-after.jpg"),
    os.path.join(BASE_DIR, "تركيب-سيراميك-الشارقة", "ceramic-before-after.jpg"),
    os.path.join(BASE_DIR, "تركيب-سيراميك-عجمان", "ceramic-before-after.jpg"),
]


def generate_image(prompt, image_size):
    """Call fal.ai API and return the image URL."""
    payload = json.dumps({
        "prompt": prompt,
        "image_size": image_size,
        "num_images": 1,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Key {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data["images"][0]["url"]


def download_image(url, dest_path):
    """Download image from URL to local path."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(dest_path, "wb") as f:
            f.write(resp.read())


def main():
    for img in IMAGES:
        print(f"\n--- Generating: {img['name']} ---")
        print(f"  Size: {img['size']['width']}x{img['size']['height']}")

        url = generate_image(img["prompt"], img["size"])
        print(f"  URL: {url}")

        download_image(url, img["path"])
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  Saved: {img['path']}")
        print(f"  File size: {size_kb:.1f} KB")

        # Small delay to be nice to the API
        time.sleep(1)

    # Copy before-after image to other city folders
    src = IMAGES[-1]["path"]
    print(f"\n--- Copying before-after image to other cities ---")
    for dest in BEFORE_AFTER_COPIES:
        shutil.copy2(src, dest)
        size_kb = os.path.getsize(dest) / 1024
        print(f"  Copied to: {dest} ({size_kb:.1f} KB)")

    # Final summary
    print("\n=== SUMMARY ===")
    all_paths = [img["path"] for img in IMAGES] + BEFORE_AFTER_COPIES
    for p in all_paths:
        if os.path.exists(p):
            size_kb = os.path.getsize(p) / 1024
            print(f"  {size_kb:>8.1f} KB  {p}")
        else:
            print(f"  MISSING     {p}")

    print("\nDone!")


if __name__ == "__main__":
    main()
