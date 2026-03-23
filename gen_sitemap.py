# -*- coding: utf-8 -*-
"""
gen_sitemap.py — Auto-generate sitemap.xml for hub.rafeeg.ae
Run after any page is added, removed, or URL-changed.
Usage: python3 gen_sitemap.py
"""
import os, datetime

BASE     = os.path.dirname(os.path.abspath(__file__))
DOMAIN   = "https://hub.rafeeg.ae"
OUT_FILE = os.path.join(BASE, "sitemap.xml")

# ── Priority & changefreq rules ──────────────────────────────────────────────
# Evaluated top-to-bottom — first match wins
RULES = [
    # slug pattern (substring match)          priority  changefreq
    ("",                                       1.0,     "weekly"),   # homepage (empty slug)
    ("صيانة-مكيفات-",                          0.9,     "monthly"),  # صيانة city pages
    ("صيانة-مكيفات",                           0.8,     "monthly"),  # صيانة category
    ("تنظيف-مكيفات-",                          0.8,     "monthly"),  # تنظيف city pages
    ("تنظيف-مكيفات",                           0.7,     "monthly"),  # تنظيف category
    ("اصلاح-مكيفات-",                          0.8,     "monthly"),  # اصلاح city pages
    ("اصلاح-مكيفات",                           0.7,     "monthly"),  # اصلاح category
]

# City hub pages
CITY_HUBS = {"أبوظبي", "دبي", "الشارقة", "عجمان"}

def get_priority_freq(slug):
    if slug == "":
        return 1.0, "weekly"
    if slug in CITY_HUBS:
        return 0.7, "monthly"
    for pattern, priority, freq in RULES:
        if pattern and slug.startswith(pattern):
            return priority, freq
    return 0.6, "monthly"

# ── Collect all pages ────────────────────────────────────────────────────────
pages = []
for root, dirs, files in os.walk(BASE):
    # Skip hidden directories and non-page folders
    dirs[:] = [d for d in sorted(dirs) if not d.startswith('.')]
    if "index.html" not in files:
        continue
    path  = os.path.join(root, "index.html")
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    slug  = root.replace(BASE, "").strip("/")
    priority, freq = get_priority_freq(slug)
    url   = f"{DOMAIN}/{slug}/" if slug else f"{DOMAIN}/"
    pages.append((priority, slug or "__home__", url, mtime.strftime("%Y-%m-%d"), freq))

# Sort: priority desc, then slug alpha
pages.sort(key=lambda x: (-x[0], x[1]))

# ── Build XML ────────────────────────────────────────────────────────────────
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    f'  <!-- Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} — {len(pages)} URLs -->',
    '',
]

sections = {
    1.0:  "<!-- ═══ HOMEPAGE ═══════════════════════════════════════ -->",
    0.9:  "<!-- ═══ MAIN SERVICE PAGES (صيانة) ═══════════════════ -->",
    0.8:  "<!-- ═══ CATEGORY & SUB-SERVICE PAGES ══════════════════ -->",
    0.7:  "<!-- ═══ CITY HUBS ══════════════════════════════════════ -->",
    0.6:  "<!-- ═══ OTHER SERVICE CATEGORIES ══════════════════════ -->",
}
last_priority = None

for priority, slug, url, lastmod, freq in pages:
    if priority != last_priority and priority in sections:
        lines.append(f"  {sections[priority]}")
        last_priority = priority
    lines += [
        "  <url>",
        f"    <loc>{url}</loc>",
        f"    <lastmod>{lastmod}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{priority:.1f}</priority>",
        "  </url>",
    ]

lines.append("</urlset>")

xml = "\n".join(lines)

# ── Write file ───────────────────────────────────────────────────────────────
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"✓ sitemap.xml written — {len(pages)} URLs")
for priority, slug, url, lastmod, freq in pages:
    label = slug if slug != "__home__" else "/"
    print(f"  {priority:.1f}  {label}")
