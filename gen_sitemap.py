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

# ── Thin/stub pages to exclude from sitemap ───────────────────────────────────
# These have no real service content yet (<600 words, "coming soon" pages)
EXCLUDE = {
    "ارضيات",
    "ديكور",
    "تنجيد",
    "مسابح",
    "المنيوم",
    "زجاج",
    "تزيين-حدائق",
    "حديد-مشغول",
    "الاجهزة-المنزلية",
}

# ── Priority & changefreq rules ───────────────────────────────────────────────
# Evaluated top-to-bottom — first match wins (startswith matching on slug)
# Ordering: more specific patterns must come BEFORE broader ones
RULES = [
    # ── Ceramic — small bathroom (more specific, before generic حمامات) ──────
    ("تركيب-سيراميك-حمامات-صغيرة-",       0.7, "monthly"),  # small bath city pages
    ("تركيب-سيراميك-حمامات-صغيرة",        0.7, "monthly"),  # small bath hub

    # ── Ceramic — bathroom (high intent: waterproofing, most expensive) ───────
    ("تركيب-سيراميك-حمامات-",              0.9, "monthly"),  # bathroom city pages
    ("تركيب-سيراميك-حمامات",              0.8, "monthly"),  # bathroom category hub

    # ── Ceramic — kitchen ─────────────────────────────────────────────────────
    ("تركيب-سيراميك-مطابخ-",              0.8, "monthly"),  # kitchen city pages
    ("تركيب-سيراميك-مطابخ",              0.8, "monthly"),  # kitchen category hub

    # ── Ceramic — floor ───────────────────────────────────────────────────────
    ("تركيب-سيراميك-أرضيات-",             0.8, "monthly"),  # floor city pages
    ("تركيب-سيراميك-أرضيات",             0.8, "monthly"),  # floor category hub

    # ── Ceramic — wall ────────────────────────────────────────────────────────
    ("تركيب-سيراميك-جدران-",              0.8, "monthly"),  # wall city pages
    ("تركيب-سيراميك-جدران",              0.8, "monthly"),  # wall category hub

    # ── Ceramic — main hub & generic city pages ───────────────────────────────
    ("تركيب-سيراميك-",                    0.7, "monthly"),  # other ceramic city pages
    ("تركيب-سيراميك",                     0.8, "monthly"),  # main ceramic category hub

    # ── AC — صيانة (top priority service) ────────────────────────────────────
    ("صيانة-مكيفات-",                     0.9, "monthly"),  # AC maintenance city pages
    ("صيانة-مكيفات",                      0.8, "monthly"),  # AC maintenance hub

    # ── AC — تنظيف ────────────────────────────────────────────────────────────
    ("تنظيف-مكيفات-",                     0.8, "monthly"),  # AC cleaning city pages
    ("تنظيف-مكيفات",                      0.7, "monthly"),  # AC cleaning hub

    # ── AC — إصلاح ────────────────────────────────────────────────────────────
    ("اصلاح-مكيفات-",                     0.8, "monthly"),  # AC repair city pages
    ("اصلاح-مكيفات",                      0.7, "monthly"),  # AC repair hub

    # ── AC — other sub-services ───────────────────────────────────────────────
    ("شحن-فريون-مكيفات-",                 0.7, "monthly"),
    ("شحن-فريون-مكيفات",                  0.6, "monthly"),
    ("تركيب-مكيفات-",                     0.7, "monthly"),
    ("تركيب-مكيفات",                      0.6, "monthly"),
    ("تنظيف-دكتات-مكيفات-",               0.7, "monthly"),
    ("تنظيف-دكتات-مكيفات",                0.6, "monthly"),
    ("تصليح-مكيفات-سبلت-",                0.7, "monthly"),
    ("تصليح-مكيفات-سبلت",                 0.6, "monthly"),
    ("فك-وتركيب-مكيفات-",                 0.6, "monthly"),
    ("مكيف-لا-يبرد-",                     0.6, "monthly"),
]

# City hub pages — handled separately in get_priority_freq
CITY_HUBS = {"أبوظبي", "دبي", "الشارقة", "عجمان"}


def get_priority_freq(slug):
    if slug == "":
        return 1.0, "weekly"
    if slug in EXCLUDE:
        return None, None   # excluded — skip this page
    if slug in CITY_HUBS:
        return 0.7, "monthly"
    for pattern, priority, freq in RULES:
        if slug.startswith(pattern):
            return priority, freq
    return 0.6, "monthly"   # default: other real-content pages


# ── Collect all pages ─────────────────────────────────────────────────────────
pages = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in sorted(dirs) if not d.startswith('.')]
    if "index.html" not in files:
        continue
    path  = os.path.join(root, "index.html")
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    slug  = root.replace(BASE, "").strip("/")

    priority, freq = get_priority_freq(slug)
    if priority is None:
        continue  # skip excluded pages

    # Use Unicode URL (matches canonical URLs in pages, no percent-encoding)
    url = f"{DOMAIN}/{slug}/" if slug else f"{DOMAIN}/"
    pages.append((priority, slug or "__home__", url, mtime.strftime("%Y-%m-%d"), freq))

# Sort: priority desc, then slug alpha
pages.sort(key=lambda x: (-x[0], x[1]))

# ── Build XML ─────────────────────────────────────────────────────────────────
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    f'  <!-- Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} — {len(pages)} URLs -->',
    '',
]

sections = {
    1.0: "<!-- ═══ HOMEPAGE ══════════════════════════════════════════════ -->",
    0.9: "<!-- ═══ TOP CITY PAGES (صيانة مكيفات + سيراميك حمامات) ══════ -->",
    0.8: "<!-- ═══ CATEGORY HUBS + HIGH-VALUE CITY PAGES ════════════════ -->",
    0.7: "<!-- ═══ SECONDARY CITY PAGES + CITY HUBS ══════════════════════ -->",
    0.6: "<!-- ═══ SUPPORTING SERVICE PAGES ═════════════════════════════ -->",
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

# ── Write file ────────────────────────────────────────────────────────────────
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(xml)

print(f"✓ sitemap.xml written — {len(pages)} URLs")
excluded = sum(1 for root, dirs, files in os.walk(BASE)
               if "index.html" in files
               and os.path.basename(root) in EXCLUDE)
print(f"  Excluded {excluded} thin/stub pages")
print()
for priority, slug, url, lastmod, freq in pages:
    label = slug if slug != "__home__" else "/"
    print(f"  {priority:.1f}  {label}")
