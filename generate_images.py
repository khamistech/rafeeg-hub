#!/usr/bin/env python3
"""
Generate hero and before/after images for all new service pages
Uses fal.ai nano-banana-2 endpoint
"""
import subprocess
import json
import os
import requests
import time
from pathlib import Path

FAL_KEY = os.environ.get("FAL_KEY")
BASE_URL = "https://queue.fal.run/fal-ai/nano-banana-2"
API_KEY_HEADER = FAL_KEY if FAL_KEY and not FAL_KEY.startswith("fal_") else f"fal_{FAL_KEY}" if FAL_KEY else None

SERVICES = {
    "تسليك-مواسير": {
        "name": "تسليك مواسير",
        "hero_prompt": "professional plumber using modern drain cleaning equipment in a modern bathroom, professional photography, detailed, bright lighting",
        "before_after_prompt": "before and after comparison of clogged and cleared drain pipes, split image, professional",
        "seed_base": 40000
    },
    "أعمال-كهربائية": {
        "name": "أعمال كهربائية",
        "hero_prompt": "professional electrician installing wiring on electrical panel in a modern home, technical work, professional photography, bright",
        "before_after_prompt": "before and after of electrical system upgrade, split image showing old and new panels",
        "seed_base": 41000
    },
    "نجارة-وديكور": {
        "name": "نجارة وديكور",
        "hero_prompt": "skilled carpenter crafting custom wooden shelves and furniture in a bright workshop, high quality wood, professional lighting",
        "before_after_prompt": "before and after of custom built-in wardrobe installation, empty room vs finished elegant wooden shelving",
        "seed_base": 42000
    },
    "دهان": {
        "name": "دهان",
        "hero_prompt": "professional painter applying fresh paint to interior walls, perfect technique, modern apartment, bright natural light",
        "before_after_prompt": "before and after of interior wall painting transformation, same room showing color change from old to fresh new paint",
        "seed_base": 43000
    },
    "تركيب-غاز": {
        "name": "تركيب غاز",
        "hero_prompt": "professional gas technician installing kitchen gas line safely, technical precision, modern kitchen, professional lighting",
        "before_after_prompt": "before and after of gas system installation, showing empty space vs complete professional installation",
        "seed_base": 44000
    },
    "صيانة-عامة": {
        "name": "صيانة عامة",
        "hero_prompt": "handyman performing general home maintenance repairs, fixing various things, modern home, professional appearance",
        "before_after_prompt": "before and after of comprehensive home maintenance work, room transformation showing repairs completed",
        "seed_base": 45000
    },
    "مكافحة-حشرات": {
        "name": "مكافحة حشرات",
        "hero_prompt": "professional pest control technician spraying insecticide in home, safety equipment, technical precision, modern setting",
        "before_after_prompt": "before and after pest control treatment, showing infestation signs and clean treated home",
        "seed_base": 46000
    }
}

CITIES = ["أبوظبي", "دبي", "الشارقة", "عجمان"]


def generate_image(prompt, seed):
    """Generate a single image using fal.ai nano-banana-2"""
    payload = {
        "prompt": prompt,
        "image_size": {"width": 1200, "height": 630},
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "seed": seed
    }

    headers = {}
    if API_KEY_HEADER:
        headers["Authorization"] = f"Key {API_KEY_HEADER}"

    try:
        print(f"  Generating with seed {seed}...", end="", flush=True)
        response = requests.post(BASE_URL, json=payload, headers=headers, timeout=120)

        if response.status_code == 200:
            result = response.json()
            if "image" in result:
                img_url = result["image"]["url"]
                return img_url
            elif "images" in result and len(result["images"]) > 0:
                img_url = result["images"][0]["url"]
                return img_url

        print(f" ❌ Status {response.status_code}")
        return None
    except Exception as e:
        print(f" ❌ Error: {e}")
        return None


def download_image(url, filepath):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Save as JPG
            with open(filepath.replace(".webp", ".jpg"), "wb") as f:
                f.write(response.content)
            print(f"    ✅ Downloaded: {filepath.replace('.webp', '.jpg')}")
            return True
    except Exception as e:
        print(f"    ❌ Download failed: {e}")
    return False


def main():
    os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

    if not API_KEY_HEADER:
        print("❌ FAL_KEY environment variable not set")
        return

    total_images = 0

    for service_slug, service_data in SERVICES.items():
        print(f"\n🎨 {service_data['name']}")

        for city in CITIES:
            page_slug = f"{service_slug}-{city.replace(' ', '-')}"
            page_dir = Path(page_slug)
            page_dir.mkdir(exist_ok=True)

            # Generate hero image
            hero_seed = service_data["seed_base"] + CITIES.index(city)
            print(f"  📸 Hero ({city})...", end="", flush=True)
            hero_url = generate_image(service_data["hero_prompt"], hero_seed)

            if hero_url:
                hero_path = page_dir / "hero.jpg"
                if download_image(hero_url, str(hero_path)):
                    total_images += 1
                time.sleep(2)
            else:
                print()

            # Generate before/after image
            ba_seed = service_data["seed_base"] + 100 + CITIES.index(city)
            print(f"  🔄 Before/After ({city})...", end="", flush=True)
            ba_url = generate_image(service_data["before_after_prompt"], ba_seed)

            if ba_url:
                ba_path = page_dir / "ac-before-after.jpg"
                if download_image(ba_url, str(ba_path)):
                    total_images += 1
                time.sleep(2)
            else:
                print()

    print(f"\n✅ Generated {total_images} images")


if __name__ == "__main__":
    main()
