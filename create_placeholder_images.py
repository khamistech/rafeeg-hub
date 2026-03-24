#!/usr/bin/env python3
"""
Create placeholder images for all new service pages using PIL
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

SERVICES = {
    "تسليك-مواسير": "Plumbing Services",
    "أعمال-كهربائية": "Electrical Services",
    "نجارة-وديكور": "Carpentry & Decor",
    "دهان": "Painting Services",
    "تركيب-غاز": "Gas Installation",
    "صيانة-عامة": "General Maintenance",
    "مكافحة-حشرات": "Pest Control"
}

CITIES = ["أبوظبي", "دبي", "الشارقة", "عجمان"]


def create_image(service_name, city, image_type="hero"):
    """Create a placeholder image"""
    width, height = 1200, 630

    # Gradient background
    img = Image.new("RGB", (width, height), color=(41, 128, 185))

    # Add a pattern
    draw = ImageDraw.Draw(img)

    # Add diagonal pattern
    for i in range(0, width + height, 50):
        draw.line([(i, 0), (i - height, height)], fill=(52, 152, 219), width=2)

    # Try to load a font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 60)
        sub_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # Add text
    if image_type == "hero":
        text = f"{service_name}\n{city}"
        y_offset = height // 2 - 100
    else:
        text = f"Before & After\n{service_name}"
        y_offset = height // 2 - 80

    # Draw text with shadow effect
    for x_offset in [-2, 2]:
        for y_offset_shadow in [-2, 2]:
            draw.text(
                (width // 2 + x_offset, y_offset + y_offset_shadow),
                text,
                fill=(0, 0, 0, 128),
                font=title_font if image_type == "hero" else sub_font,
                anchor="mm",
            )

    # Draw main text
    draw.text(
        (width // 2, y_offset),
        text,
        fill=(255, 255, 255),
        font=title_font if image_type == "hero" else sub_font,
        anchor="mm",
    )

    return img


def main():
    os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

    total = 0

    for service_slug, service_name in SERVICES.items():
        print(f"\n📸 {service_name}")

        for city in CITIES:
            page_slug = f"{service_slug}-{city.replace(' ', '-')}"
            page_dir = Path(page_slug)
            page_dir.mkdir(exist_ok=True)

            # Create hero image
            print(f"  • {city} hero...", end="", flush=True)
            hero_img = create_image(service_name, city, "hero")
            hero_path = page_dir / "hero.jpg"
            hero_img.save(str(hero_path), "JPEG", quality=92)
            print(" ✅")
            total += 1

            # Create before/after image
            print(f"  • {city} before/after...", end="", flush=True)
            ba_img = create_image(service_name, city, "before_after")
            ba_path = page_dir / "ac-before-after.jpg"
            ba_img.save(str(ba_path), "JPEG", quality=92)
            print(" ✅")
            total += 1

    print(f"\n✅ Created {total} placeholder images")


if __name__ == "__main__":
    main()
