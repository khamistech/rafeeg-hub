#!/usr/bin/env python3
"""
Create service category hub pages and update homepage
"""
import os
import json
from pathlib import Path
from datetime import datetime

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

# Read the template
with open("_base_service_template.html", "r", encoding="utf-8") as f:
    TEMPLATE = f.read()

SERVICES = {
    "تسليك-مواسير": {
        "name": "تسليك مواسير",
        "desc": "خدمات تسليك احترافية للمواسير والمجاري",
        "icon": "🔧"
    },
    "أعمال-كهربائية": {
        "name": "أعمال كهربائية",
        "desc": "أعمال كهربائية آمنة ومعتمدة",
        "icon": "⚡"
    },
    "نجارة-وديكور": {
        "name": "نجارة وديكور",
        "desc": "نجارة وديكورات عالية الجودة",
        "icon": "🪓"
    },
    "دهان": {
        "name": "دهان",
        "desc": "دهان احترافي بأعلى جودة",
        "icon": "🎨"
    },
    "تركيب-غاز": {
        "name": "تركيب غاز",
        "desc": "تركيب وصيانة آمنة للغاز",
        "icon": "🔥"
    },
    "صيانة-عامة": {
        "name": "صيانة عامة",
        "desc": "صيانة شاملة وموثوقة",
        "icon": "🔧"
    },
    "مكافحة-حشرات": {
        "name": "مكافحة حشرات",
        "desc": "مكافحة احترافية وآمنة",
        "icon": "🐛"
    }
}

CITIES = ["أبوظبي", "دبي", "الشارقة", "عجمان"]


def create_hub_page(service_slug, service_data):
    """Create a category hub page"""

    # Build city links
    city_links = []
    for city in CITIES:
        city_links.append({
            "href": f"/{service_slug}-{city.replace(' ', '-')}/",
            "title": f"{service_data['name']} {city}",
            "desc": f"أسعار وخدمات في {city}"
        })

    html = TEMPLATE
    replacements = {
        "{{SLUG}}": service_slug,
        "{{PAGE_TITLE}}": f"{service_data['name']} في الإمارات | رفيق",
        "{{SERVICE_NAME}}": service_data['name'],
        "{{SERVICE_NAME_AR}}": service_data['name'],
        "{{CITY}}": "الإمارات",
        "{{BASE_PRICE}}": "متغير",
        "{{HERO_H2}}": f"{service_data['name']} احترافي في جميع الإمارات",
        "{{HERO_SUB}}": f"احصل على {service_data['name']} من فنيين معتمدين في أبوظبي، دبي، الشارقة، وعجمان",
        "{{H1_TEXT}}": f"{service_data['name']} - فنيون معتمدون في جميع الإمارات",
    }

    # Add city cards
    city_cards_html = ""
    for city in CITIES:
        city_cards_html += f"""
        <div class="city-card">
            <h3>{city}</h3>
            <p>اختر {service_data['name']} في {city}</p>
            <a href="/{service_slug}-{city.replace(' ', '-')}/" class="btn btn-primary">اعرض الأسعار</a>
        </div>"""

    replacements["{{CITY_CARDS}}"] = city_cards_html

    # Build the body content
    body = f"""
    <h2>خدمات {service_data['name']} في الإمارات</h2>
    <p>رفيق توفر خدمة {service_data['name']} الاحترافية والموثوقة في جميع إمارات الدولة. فنيونا المعتمدون يعملون بأعلى المعايير.</p>

    <h2>اختر إمارتك</h2>
    <p>اضغط على إمارتك لمعرفة الأسعار والعروض الخاصة بك:</p>

    {city_cards_html}

    <h2>لماذا تختار رفيق لخدمة {service_data['name']}؟</h2>
    <ul>
        <li>+4,500 فني معتمد في جميع الإمارات</li>
        <li>تقييم 4.8/5 من 135,000 عميل</li>
        <li>شهادات ISO 9001 و ISO 45001</li>
        <li>ضمان 90 يوم على كل خدمة</li>
        <li>أسعار شفافة بدون مفاجآت</li>
    </ul>
    """

    replacements["{{BODY_CONTENT}}"] = body

    for key, value in replacements.items():
        html = html.replace(key, str(value))

    return html


def create_homepage():
    """Update the homepage with all services"""

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Build services list for schema
    services_list = []
    for service_slug, service_data in SERVICES.items():
        services_list.append({
            "name": service_data['name'],
            "url": f"https://hub.rafeeg.ae/{service_slug}/",
            "image": f"https://hub.rafeeg.ae/{service_slug}/hero.jpg"
        })

    # Add AC services too
    ac_services = [
        ("تركيب-مكيفات", "تركيب مكيفات"),
        ("صيانة-مكيفات", "صيانة مكيفات"),
        ("تنظيف-مكيفات", "تنظيف مكيفات"),
        ("اصلاح-مكيفات", "إصلاح مكيفات"),
        ("شحن-فريون-مكيفات", "شحن فريون"),
    ]

    for slug, name in ac_services:
        services_list.append({
            "name": name,
            "url": f"https://hub.rafeeg.ae/{slug}/",
            "image": f"https://hub.rafeeg.ae/{slug}/hero.jpg"
        })

    # Build ItemList schema
    item_list_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "خدمات رفيق",
        "description": "جميع خدمات المنزل على تطبيق رفيق",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item['name'],
                "url": item['url'],
                "image": item['image']
            } for i, item in enumerate(services_list)
        ]
    }

    # Insert the schema before </head>
    schema_script = f"<script type=\"application/ld+json\">\n{json.dumps(item_list_schema, ensure_ascii=False, indent=2)}\n</script>"

    if "</head>" in content:
        content = content.replace("</head>", f"{schema_script}\n</head>")

    return content


def main():
    print("📄 Creating service hub pages...")
    total_hubs = 0

    for service_slug, service_data in SERVICES.items():
        print(f"  {service_data['name']}...", end="", flush=True)

        hub_html = create_hub_page(service_slug, service_data)
        hub_dir = Path(service_slug)
        hub_dir.mkdir(exist_ok=True)

        with open(hub_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(hub_html)

        print(" ✅")
        total_hubs += 1

    print(f"\n✅ Created {total_hubs} hub pages")

    print("\n📄 Updating homepage...")
    homepage = create_homepage()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(homepage)
    print("✅ Homepage updated")


if __name__ == "__main__":
    main()
