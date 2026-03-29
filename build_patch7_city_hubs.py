#!/usr/bin/env python3
"""Patch 7: Add 3 new ceramic service cards to each city hub page."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

CITIES = [
    {
        "slug": "أبوظبي",
        "old_anchor": "https://hub.rafeeg.ae/تزيين-حدائق-أبوظبي/",
        "cards": [
            {
                "href": "https://hub.rafeeg.ae/بورسلين-حمامات-أبوظبي/",
                "icon": "💎",
                "name": "بورسلين حمامات في أبوظبي",
                "desc": "تركيب بورسلين الحمامات — امتصاص ماء أقل من 0.5% وعزل مائي متضمن",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/تصميم-حمامات-أبوظبي/",
                "icon": "🎨",
                "name": "تصميم حمامات في أبوظبي",
                "desc": "تصميم وتجديد حمامات مودرن وفندقي ومينيمال — استشارة مجانية",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/سيراميك-راس-الخيمة-أبوظبي/",
                "icon": "🏭",
                "name": "سيراميك RAK في أبوظبي",
                "desc": "تركيب RAKstone وRAKporcelain وRAKwood وRAKmarble",
                "price": "من 25 د.إ/م²",
            },
        ],
    },
    {
        "slug": "دبي",
        "old_anchor": "https://hub.rafeeg.ae/تزيين-حدائق-دبي/",
        "cards": [
            {
                "href": "https://hub.rafeeg.ae/بورسلين-حمامات-دبي/",
                "icon": "💎",
                "name": "بورسلين حمامات في دبي",
                "desc": "تركيب بورسلين الحمامات — امتصاص ماء أقل من 0.5% وعزل مائي متضمن",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/تصميم-حمامات-دبي/",
                "icon": "🎨",
                "name": "تصميم حمامات في دبي",
                "desc": "تصميم وتجديد حمامات مودرن وفندقي ومينيمال — استشارة مجانية",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/سيراميك-راس-الخيمة-دبي/",
                "icon": "🏭",
                "name": "سيراميك RAK في دبي",
                "desc": "تركيب RAKstone وRAKporcelain وRAKwood وRAKmarble",
                "price": "من 25 د.إ/م²",
            },
        ],
    },
    {
        "slug": "الشارقة",
        "old_anchor": "https://hub.rafeeg.ae/تزيين-حدائق-الشارقة/",
        "cards": [
            {
                "href": "https://hub.rafeeg.ae/بورسلين-حمامات-الشارقة/",
                "icon": "💎",
                "name": "بورسلين حمامات في الشارقة",
                "desc": "تركيب بورسلين الحمامات — امتصاص ماء أقل من 0.5% وعزل مائي متضمن",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/تصميم-حمامات-الشارقة/",
                "icon": "🎨",
                "name": "تصميم حمامات في الشارقة",
                "desc": "تصميم وتجديد حمامات مودرن وفندقي ومينيمال — استشارة مجانية",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/سيراميك-راس-الخيمة-الشارقة/",
                "icon": "🏭",
                "name": "سيراميك RAK في الشارقة",
                "desc": "تركيب RAKstone وRAKporcelain وRAKwood وRAKmarble",
                "price": "من 25 د.إ/م²",
            },
        ],
    },
    {
        "slug": "عجمان",
        "old_anchor": "https://hub.rafeeg.ae/تزيين-حدائق-عجمان/",
        "cards": [
            {
                "href": "https://hub.rafeeg.ae/بورسلين-حمامات-عجمان/",
                "icon": "💎",
                "name": "بورسلين حمامات في عجمان",
                "desc": "تركيب بورسلين الحمامات — امتصاص ماء أقل من 0.5% وعزل مائي متضمن",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/تصميم-حمامات-عجمان/",
                "icon": "🎨",
                "name": "تصميم حمامات في عجمان",
                "desc": "تصميم وتجديد حمامات مودرن وفندقي ومينيمال — استشارة مجانية",
                "price": "من 1,000 درهم/حمام",
            },
            {
                "href": "https://hub.rafeeg.ae/سيراميك-راس-الخيمة-عجمان/",
                "icon": "🏭",
                "name": "سيراميك RAK في عجمان",
                "desc": "تركيب RAKstone وRAKporcelain وRAKwood وRAKmarble",
                "price": "من 25 د.إ/م²",
            },
        ],
    },
]


def build_card(c):
    return f"""        <a href="{c['href']}" class="cat-card">
          <div class="cat-card-icon">{c['icon']}</div>
          <div class="cat-card-name">{c['name']}</div>
          <div class="cat-card-desc">{c['desc']}</div>
          <div class="cat-card-price">{c['price']}</div>
          <span class="cat-card-cta">احجز الآن</span>
        </a>"""


for city in CITIES:
    path = os.path.join(BASE, city["slug"], "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Find the closing </a> after the last card (تزيين-حدائق) and insert new cards after it
    anchor = city["old_anchor"]
    # Find the closing </a>\n      </div> after the تزيين-حدائق card
    search = f'        <a href="{anchor}" class="cat-card">'
    pos = html.find(search)
    if pos == -1:
        print(f"⚠️  Could not find anchor in {city['slug']}, skipping")
        continue

    # Find the </a> that closes this card block
    close_tag = "        </a>\n      </div>"
    close_pos = html.find(close_tag, pos)
    if close_pos == -1:
        # Try alternate closing
        close_tag = "        </a>\n    </div>"
        close_pos = html.find(close_tag, pos)

    if close_pos == -1:
        print(f"⚠️  Could not find closing tag in {city['slug']}, skipping")
        continue

    # Insert new cards before the closing </div>
    insert_point = close_pos + len("        </a>")
    new_cards = "\n" + "\n".join(build_card(c) for c in city["cards"])
    html = html[:insert_point] + new_cards + html[insert_point:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Updated {city['slug']} — added {len(city['cards'])} cards")

print("\n✅ Done")
