#!/usr/bin/env python3
"""
Generate all service page images using fal.ai flux/schnell.
- Hero:        768×1376 portrait — professional worker on the job
- Before/After: 1408×768 — composite of before(704×768) + after(704×768)

Generates unique hero per page (35 pages) + 1 BA composite per service (7).
Total: ~49 fal.ai calls.
"""
import requests, os, time, json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

FAL_KEY = "ff27ffc3-2e6d-4f2d-b19b-e2a241239b0d:968d18c810e7d0e0aba234d9d401b8ef"
FAL_URL = "https://fal.run/fal-ai/flux/schnell"
HEADERS = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}

CITIES = ["أبوظبي", "دبي", "الشارقة", "عجمان"]
CITY_EN = {"أبوظبي": "Abu Dhabi", "دبي": "Dubai", "الشارقة": "Sharjah", "عجمان": "Ajman"}

SERVICES = {
    "تسليك-مواسير": {
        "hero_base": "professional Arab plumber in uniform using drain cleaning machine, modern UAE bathroom, bright professional lighting, close-up portrait, photorealistic",
        "before": "badly clogged dirty kitchen sink drain with standing water and debris, dark grimy pipes, UAE apartment kitchen, realistic photo",
        "after":  "perfectly clean clear kitchen sink drain, sparkling chrome pipes, water flowing freely, after professional plumbing service, UAE apartment, bright",
        "seed": 1000,
    },
    "أعمال-كهربائية": {
        "hero_base": "professional electrician wearing hard hat and safety gloves working on modern electrical panel, UAE home, bright workshop lighting, portrait, photorealistic",
        "before": "old messy tangled electrical wiring, outdated fuse box, loose cables hanging, safety hazard, UAE home, realistic photo",
        "after":  "brand new organized electrical panel with labeled circuit breakers, neat cable management, professional installation complete, UAE home, bright",
        "seed": 2000,
    },
    "نجارة-وديكور": {
        "hero_base": "skilled Arab carpenter measuring custom wooden wardrobe panels in workshop, sawdust, professional tools, UAE interior, portrait, photorealistic",
        "before": "empty bare room with plain white walls, no built-in furniture, raw unfurnished interior, UAE apartment, realistic photo",
        "after":  "elegant custom built-in wooden wardrobe wall-to-wall, beautiful interior carpentry, warm wood tones, modern UAE apartment, professionally finished",
        "seed": 3000,
    },
    "دهان": {
        "hero_base": "professional painter in overalls rolling fresh white paint on interior wall, UAE apartment, bright natural light, portrait, photorealistic",
        "before": "old peeling paint on walls, faded yellowed color, stained patches, worn interior UAE apartment wall, realistic photo",
        "after":  "freshly painted smooth walls in modern neutral color, perfect even finish, bright clean interior, UAE apartment, professional result",
        "seed": 4000,
    },
    "تركيب-غاز": {
        "hero_base": "professional gas technician in safety gear installing copper gas pipe in UAE kitchen, technical precision, portrait, photorealistic",
        "before": "kitchen wall before gas installation, exposed rough concrete, no gas pipe, preparation stage, UAE apartment, realistic photo",
        "after":  "professional gas line installation complete, neat copper pipes, safety valves, modern UAE kitchen gas connection, clean and certified",
        "seed": 5000,
    },
    "صيانة-عامة": {
        "hero_base": "professional handyman with tool belt fixing door hinge in UAE apartment hallway, confident smile, uniform, portrait, photorealistic",
        "before": "damaged UAE apartment interior, cracked wall plaster, broken door hinge, worn fixtures, maintenance needed, realistic photo",
        "after":  "fully repaired UAE apartment interior, smooth walls, working fixtures, fresh repairs complete, clean maintained home, bright",
        "seed": 6000,
    },
    "مكافحة-حشرات": {
        "hero_base": "professional pest control technician in white protective suit with backpack sprayer treating UAE apartment, portrait, photorealistic",
        "before": "kitchen corner with cockroach infestation signs, droppings, dusty grimy cabinet interior, UAE apartment, realistic photo",
        "after":  "spotless clean sanitized UAE apartment kitchen after professional pest control, no pests, gleaming surfaces, treated and certified",
        "seed": 7000,
    },
}

# City-specific hero suffix to add variety
CITY_SUFFIX = {
    "أبوظبي":  "in Abu Dhabi UAE",
    "دبي":     "in Dubai UAE",
    "الشارقة": "in Sharjah UAE",
    "عجمان":   "in Ajman UAE",
}


def fal_generate(prompt: str, width: int, height: int, seed: int):
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


def save_pair(img_bytes: bytes, base_path: str, target_w: int, target_h: int):
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    # Resize/crop to exact target dimensions
    scale = max(target_w / img.width, target_h / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - target_w) // 2
    y = (nh - target_h) // 2
    img = img.crop((x, y, x + target_w, y + target_h))
    img.save(base_path + ".jpg",  "JPEG", quality=88, optimize=True)
    img.save(base_path + ".webp", "WEBP", quality=82, method=6)
    kj = os.path.getsize(base_path + ".jpg")  // 1024
    kw = os.path.getsize(base_path + ".webp") // 1024
    print(f"      → {base_path.split('/')[-2]}/{base_path.split('/')[-1]}  jpg={kj}KB  webp={kw}KB")
    return img


def make_ba_composite(before_bytes: bytes, after_bytes: bytes, out_base: str):
    W, H = 1408, 768
    half = W // 2

    def crop_half(data):
        img = Image.open(BytesIO(data)).convert("RGB")
        sc = max(half / img.width, H / img.height)
        nw, nh = int(img.width * sc), int(img.height * sc)
        img = img.resize((nw, nh), Image.LANCZOS)
        x = (nw - half) // 2
        y = (nh - H)    // 2
        return img.crop((x, y, x + half, y + H))

    canvas = Image.new("RGB", (W, H))
    canvas.paste(crop_half(before_bytes), (0, 0))
    canvas.paste(crop_half(after_bytes),  (half, 0))

    draw = ImageDraw.Draw(canvas)

    # Divider line
    draw.line([(half, 0), (half, H)], fill=(255, 255, 255), width=4)

    # Arrow circle
    cx, cy, r = half, H // 2, 30
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255))
    draw.polygon([(cx-10, cy-14), (cx+12, cy), (cx-10, cy+14)], fill=(40, 40, 40))

    # Labels
    try:
        fn = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if not os.path.exists(fn):
            fn = "/System/Library/Fonts/Arial.ttf"
        font = ImageFont.truetype(fn, 34)
    except:
        font = ImageFont.load_default()

    pad = 14
    for text, fg, bg, side in [
        ("BEFORE", (255,255,255), (180,30,30),  "left"),
        ("AFTER",  (255,255,255), (30,140,50),   "right"),
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

    canvas.save(out_base + ".jpg",  "JPEG", quality=88, optimize=True)
    canvas.save(out_base + ".webp", "WEBP", quality=82, method=6)
    kj = os.path.getsize(out_base + ".jpg")  // 1024
    kw = os.path.getsize(out_base + ".webp") // 1024
    print(f"      → BA composite  jpg={kj}KB  webp={kw}KB")


def main():
    total_calls = 0

    # Pre-generate BA composites (1 per service = 14 fal calls)
    ba_cache = {}  # service_slug → (before_bytes, after_bytes)

    print("\n=== Generating Before/After composites (7 services × 2 images) ===")
    for svc_slug, svc in SERVICES.items():
        print(f"\n  [{svc_slug}]")

        print(f"    generating BEFORE...", end=" ", flush=True)
        b_data = fal_generate(svc["before"], 704, 768, svc["seed"] + 500)
        total_calls += 1
        if not b_data:
            print("❌ failed, skipping")
            continue
        print("✅")
        time.sleep(1)

        print(f"    generating AFTER...",  end=" ", flush=True)
        a_data = fal_generate(svc["after"],  704, 768, svc["seed"] + 600)
        total_calls += 1
        if not a_data:
            print("❌ failed, skipping")
            continue
        print("✅")
        time.sleep(1)

        ba_cache[svc_slug] = (b_data, a_data)

        # Write BA for hub page
        os.makedirs(svc_slug, exist_ok=True)
        print(f"    compositing hub BA...", end=" ", flush=True)
        make_ba_composite(b_data, a_data, f"{svc_slug}/ac-before-after")

        # Write BA for all 4 city pages (same composite)
        for city in CITIES:
            page_dir = f"{svc_slug}-{city}"
            os.makedirs(page_dir, exist_ok=True)
            make_ba_composite(b_data, a_data, f"{page_dir}/ac-before-after")

    # Generate hero images (1 per page = 35 fal calls)
    print("\n\n=== Generating Hero images (35 pages) ===")
    page_num = 0
    total_pages = len(SERVICES) + len(SERVICES) * len(CITIES)

    for svc_slug, svc in SERVICES.items():
        # Hub hero
        page_num += 1
        print(f"\n  [{page_num}/{total_pages}] {svc_slug}/ (hub)")
        prompt = svc["hero_base"] + ", UAE"
        print(f"    generating hero...", end=" ", flush=True)
        data = fal_generate(prompt, 768, 1376, svc["seed"])
        total_calls += 1
        if data:
            print("✅")
            save_pair(data, f"{svc_slug}/hero", 768, 1376)
        else:
            print("❌")
        time.sleep(1)

        # City heroes
        for i, city in enumerate(CITIES):
            page_num += 1
            page_dir = f"{svc_slug}-{city}"
            os.makedirs(page_dir, exist_ok=True)
            print(f"\n  [{page_num}/{total_pages}] {page_dir}/")
            prompt = svc["hero_base"] + f", {CITY_SUFFIX[city]}"
            print(f"    generating hero...", end=" ", flush=True)
            data = fal_generate(prompt, 768, 1376, svc["seed"] + i + 1)
            total_calls += 1
            if data:
                print("✅")
                save_pair(data, f"{page_dir}/hero", 768, 1376)
            else:
                print("❌")
            time.sleep(1)

    print(f"\n\n✅ Done — {total_calls} fal.ai calls made")


if __name__ == "__main__":
    main()
