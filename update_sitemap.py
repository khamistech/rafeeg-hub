#!/usr/bin/env python3
"""
Generate sitemap.xml with all pages
"""
import os
from pathlib import Path
from datetime import datetime

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

SERVICES = {
    "تسليك-مواسير": "تسليك مواسير",
    "أعمال-كهربائية": "أعمال كهربائية",
    "نجارة-وديكور": "نجارة وديكور",
    "دهان": "دهان",
    "تركيب-غاز": "تركيب غاز",
    "صيانة-عامة": "صيانة عامة",
    "مكافحة-حشرات": "مكافحة حشرات",
    "تركيب-مكيفات": "تركيب مكيفات",
    "صيانة-مكيفات": "صيانة مكيفات",
    "تنظيف-مكيفات": "تنظيف مكيفات",
    "اصلاح-مكيفات": "إصلاح مكيفات",
    "شحن-فريون-مكيفات": "شحن فريون",
}

CITIES = ["أبوظبي", "دبي", "الشارقة", "عجمان"]

def main():
    print("📄 Generating sitemap.xml...")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'

    # Homepage
    sitemap += f'''  <url>
    <loc>https://hub.rafeeg.ae/</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>\n'''

    total_urls = 1

    # Hub pages (priority 0.9)
    for service_slug, service_name in SERVICES.items():
        sitemap += f'''  <url>
    <loc>https://hub.rafeeg.ae/{service_slug}/</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>\n'''
        total_urls += 1

    # City pages (priority 0.8)
    for service_slug in SERVICES.keys():
        for city in CITIES:
            page_slug = f"{service_slug}-{city.replace(' ', '-')}"
            sitemap += f'''  <url>
    <loc>https://hub.rafeeg.ae/{page_slug}/</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n'''
            total_urls += 1

    sitemap += '</urlset>'

    # Write sitemap
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"✅ Sitemap generated with {total_urls} URLs")
    print(f"   - 1 homepage")
    print(f"   - {len(SERVICES)} hub pages")
    print(f"   - {len(SERVICES) * len(CITIES)} city/service pages")


if __name__ == "__main__":
    main()
