#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shared.py — Shared HTML section builder for ALL Rafeeg service pages.
Each function takes s (service config) and c (city config) and returns an HTML string.
"""
from datetime import date
from engine.icons import WA, APP, PHONE, STAR, CLOCK, SHIELD, CHECK, PIN, INSTAGRAM, TIKTOK, LINKEDIN, WA_FLOAT
from engine.css import get_css

TODAY = date.today().isoformat()
AVATAR_URLS = [
    "https://ar.rafeeg.ae/wp-content/uploads/2024/06/avatar-m1.jpg",
    "https://ar.rafeeg.ae/wp-content/uploads/2024/06/avatar-f1.jpg",
    "https://ar.rafeeg.ae/wp-content/uploads/2024/06/avatar-m2.jpg"
]

GUARANTEE_ICON_MAP = {
    "shield": '<svg viewBox="0 0 24 24"><path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.25C17.25 22.15 21 17.25 21 12V7L12 2z"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>',
}


# ─────────────────────────────────────────────────────────────
# 1. HEAD
# ─────────────────────────────────────────────────────────────
def build_head(s, c):
    slug = c["slug"]
    slug_en = c["slug_en"]
    city = c["city"]
    lat = c["lat"]
    lng = c["lng"]
    wikidata = c["wikidata"]
    neighborhoods = c["neighborhoods"]
    neighborhoods_full = c["neighborhoods_full"]

    title = s["title_template"].format(city=city)
    meta_desc = s["meta_desc_template"].format(city=city, neighborhoods=neighborhoods)
    og_desc = s["og_desc_template"].format(city=city)
    twitter_desc = s["twitter_desc_template"].format(city=city)
    image_prefix = s["image_prefix"]
    schema_service_desc = s["schema_service_desc"].format(city=city)
    schema_service_type = s["schema_service_type"]
    schema_low_price = s["schema_low_price"]
    schema_high_price = s["schema_high_price"]
    schema_offer_count = s["schema_offer_count"]
    schema_price_range = s["schema_price_range"]

    # Build PriceSpecification array
    price_specs_json = ",".join(
        f'{{"@type":"PriceSpecification","name":"{ps["name"]}","price":"{ps["price"]}","priceCurrency":"AED"}}'
        for ps in s["schema_price_specs"]
    )

    # Build HowTo steps from s["schema_howto_steps"]
    howto_steps = ",\n      ".join(
        f'{{"@type":"HowToStep","position":{i},"name":"{step["name"]}","text":"{step["text"].format(city=city)}"}}'
        for i, step in enumerate(s["schema_howto_steps"], 1)
    )

    # Build BreadcrumbList from s["breadcrumb_levels"] + current page
    bc_items = ""
    for i, bc in enumerate(s["breadcrumb_levels"], 1):
        bc_items += f',{{"@type":"ListItem","position":{i},"name":"{bc["name"]}","item":"https://hub.rafeeg.ae{bc["path"]}"}}'
    bc_pos = len(s["breadcrumb_levels"]) + 1
    bc_current_name = s["breadcrumb_levels"][-1]["name"] + " " + city if s.get("breadcrumb_current_template") is None else s.get("breadcrumb_current_template", "").format(city=city)
    bc_items += f',{{"@type":"ListItem","position":{bc_pos},"name":"{bc_current_name}","item":"https://hub.rafeeg.ae/{slug}/"}}'
    bc_items = bc_items[1:]  # remove leading comma

    # Build FAQ schema from s["faqs"] + optional c["city_faqs"]
    all_faqs = list(s["faqs"]) + list(c.get("city_faqs", []))
    faq_entities = ",\n      ".join(
        f'{{"@type":"Question","name":"{faq["q"].format(city=city, neighborhoods_full=neighborhoods_full)}","acceptedAnswer":{{"@type":"Answer","text":"{faq["a"].format(city=city, neighborhoods_full=neighborhoods_full)}"}}}}'
        for faq in all_faqs
    )

    css = get_css()
    # No escaping needed: {css} in an f-string simply substitutes the value;
    # literal { } chars inside the *value* are not treated as f-string syntax.

    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://hub.rafeeg.ae/{slug}/">
<link rel="alternate" hreflang="ar" href="https://hub.rafeeg.ae/{slug}/">
<link rel="alternate" hreflang="x-default" href="https://hub.rafeeg.ae/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://hub.rafeeg.ae/{slug}/">
<meta property="og:locale" content="ar_AE">
<meta property="og:image" content="https://hub.rafeeg.ae/{slug}/{image_prefix}-{slug_en}.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{twitter_desc}">
<meta name="twitter:image" content="https://hub.rafeeg.ae/{slug}/{image_prefix}-{slug_en}.jpg">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{"@type":"HomeAndConstructionBusiness","@id":"https://ar.rafeeg.ae/#organization","name":"رفيق","description":"رفيق هو تطبيق إماراتي للخدمات المنزلية، يربط أصحاب المنازل بأكثر من 4,500 فني معتمد في دبي وأبوظبي والشارقة وعجمان. تأسس في دولة الإمارات العربية المتحدة ويخدم 135,000 عميل حتى 2025.","url":"https://ar.rafeeg.ae","logo":"https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png","telephone":"+971600500200","email":"info@rafeeg.ae","priceRange":"{schema_price_range}","openingHours":"Mo-Su 07:00-22:00","address":{{"@type":"PostalAddress","addressLocality":"{city}","addressRegion":"{city}","addressCountry":"AE"}},"geo":{{"@type":"GeoCoordinates","latitude":"{lat}","longitude":"{lng}"}},"areaServed":[{{"@type":"City","name":"دبي"}},{{"@type":"City","name":"أبوظبي"}},{{"@type":"City","name":"الشارقة"}},{{"@type":"City","name":"عجمان"}}],"aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"135000","bestRating":"5"}},"sameAs":["https://www.instagram.com/rafeegapp","https://www.linkedin.com/company/rafeeg/","https://www.tiktok.com/@rafeeg.ae"]}},
    {{"@type":"Service","name":"{s["service_name"]} في {city}","description":"{schema_service_desc}","dateModified":"{TODAY}","provider":{{"@id":"https://ar.rafeeg.ae/#organization"}},"areaServed":{{"@type":"City","name":"{city}","sameAs":"https://www.wikidata.org/wiki/{wikidata}"}},"serviceType":"{schema_service_type}","offers":{{"@type":"AggregateOffer","priceCurrency":"AED","lowPrice":"{schema_low_price}","highPrice":"{schema_high_price}","offerCount":"{schema_offer_count}","priceSpecification":[{price_specs_json}]}}}},
    {{"@type":"HowTo","name":"{s["schema_howto_name"].format(city=city)}","step":[
      {howto_steps}
    ]}},
    {{"@type":"BreadcrumbList","itemListElement":[
      {bc_items}
    ]}},
    {{"@type":"FAQPage","mainEntity":[
      {faq_entities}
    ]}}
  ]
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{image_prefix}-{slug_en}.jpg" fetchpriority="high">
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=optional" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=optional"></noscript>
<style>
{css}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-1QSFZS28PT"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-1QSFZS28PT');</script>
</head>
<body>'''


# ─────────────────────────────────────────────────────────────
# 2. HEADER
# ─────────────────────────────────────────────────────────────
def build_header(s, c):
    city = c["city"]
    slug = c["slug"]
    service_name = s["service_name"]
    reading_time = s["reading_time"]

    # Build breadcrumb links from s["breadcrumb_levels"]
    bc_html = ""
    for bc in s["breadcrumb_levels"]:
        bc_html += f'''
      <a href="https://hub.rafeeg.ae{bc["path"]}">{bc["name"]}</a>
      <span class="sep">›</span>'''

    return f'''
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="https://hub.rafeeg.ae/" aria-label="رفيق — الرئيسية">
      <img src="https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png" alt="تطبيق رفيق" width="110" height="42" loading="eager">
    </a>
    <nav aria-label="التنقل الرئيسي">
      <ul class="nav-list" id="main-nav">
        <li class="has-dropdown">
          <a class="nav-link-drop" href="#" aria-haspopup="true">الإمارات <span class="drop-arrow">▾</span></a>
          <ul class="dropdown" role="menu">
            <li><a href="https://hub.rafeeg.ae/خدمات-أبوظبي/">أبوظبي</a></li>
            <li><a href="https://hub.rafeeg.ae/خدمات-دبي/">دبي</a></li>
            <li><a href="https://hub.rafeeg.ae/خدمات-الشارقة/">الشارقة</a></li>
            <li><a href="https://hub.rafeeg.ae/خدمات-عجمان/">عجمان</a></li>
          </ul>
        </li>
        <li class="has-dropdown">
          <a class="nav-link-drop" href="#" aria-haspopup="true">الخدمات <span class="drop-arrow">▾</span></a>
          <ul class="dropdown" role="menu">
            <li><a href="https://hub.rafeeg.ae/تركيب-سيراميك/">تركيب سيراميك</a></li>
            <li><a href="https://hub.rafeeg.ae/صيانة-مكيفات-دبي/">صيانة مكيفات</a></li>
            <li><a href="https://hub.rafeeg.ae/تسليك-مواسير/">تسليك مواسير</a></li>
            <li><a href="https://hub.rafeeg.ae/أعمال-كهربائية/">أعمال كهربائية</a></li>
            <li><a href="https://hub.rafeeg.ae/دهان/">دهان</a></li>
          </ul>
        </li>
      </ul>
    </nav>
    <div class="header-actions">
      <a class="phone-link" href="tel:+971600500200">
        {PHONE}
        600-500-200
      </a>
      <a class="btn-lang" href="https://en.rafeeg.ae/">English</a>
      <button class="hamburger" aria-label="القائمة" onclick="const n=document.getElementById('main-nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<h1 style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap">{service_name} في {city} — رفيق</h1>

<nav class="breadcrumb" aria-label="مسار التنقل">
  <div class="container breadcrumb-inner">
    <div>
      <a href="https://hub.rafeeg.ae/">الرئيسية</a>
      <span class="sep">›</span>{bc_html}
      <span aria-current="page">{s["service_name_short"]} {city}</span>
    </div>
    <div class="reading-time">{CLOCK} {reading_time} دقائق للقراءة</div>
  </div>
</nav>'''


# ─────────────────────────────────────────────────────────────
# 3. HERO
# ─────────────────────────────────────────────────────────────
def build_hero(s, c):
    city = c["city"]
    slug = c["slug"]
    slug_en = c["slug_en"]
    image_prefix = s["image_prefix"]
    wa_text = s["wa_text_template"].format(city=city)
    hero_title = s["hero_title"].format(city=city)
    hero_sub = s["hero_sub"]

    bullets_html = ""
    for b in s["hero_bullets"]:
        bullets_html += f'\n        <li><span class="chk">✓</span> {b}</li>'

    facts_html = ""
    for fact in s["ai_facts"]:
        facts_html += f'\n      <div class="ai-fact"><span>{fact["icon"]}</span> {fact["text"]}: <b>{fact["value"]}</b></div>'

    return f'''
<div class="urgency-strip" role="alert">
  ⚡ <strong>فنيون متاحون اليوم في {city}</strong> — احجز الآن واحصل على موعد نفس اليوم
</div>

<div class="container">
  <div class="ai-summary" role="note" aria-label="ملخص سريع">
    <div class="ai-summary-title">{s["ai_summary_title"].format(city=city)}</div>
    <div class="ai-summary-grid">{facts_html}
    </div>
  </div>

</div>

<div class="hero-wrap">
  <section class="hero" aria-label="قسم الترحيب">
    <div class="hero-text">
      <div class="hero-badge">
        {STAR}
        رفيق — خدمة معتمدة
      </div>
      <h2>{hero_title}</h2>
      <p class="hero-sub">{hero_sub}</p>
      <ul class="hero-bullets">{bullets_html}
      </ul>
      <div class="hero-ctas">
        <a class="btn-whatsapp-solid" href="https://wa.me/971600500200?text={wa_text}" target="_blank" rel="noopener">{WA} واتساب — احجز الآن</a>
        <a class="btn-green" href="https://rafeeggoogle.onelink.me/C8Hp/news">{APP} حمّل التطبيق الآن</a>
      </div>
    </div>
    <div class="hero-image" aria-hidden="true">
      <img src="{image_prefix}-{slug_en}.jpg" alt="{s["service_name"]} في {city} — خدمة احترافية من رفيق" width="340" height="380" loading="eager" fetchpriority="high" style="width:100%;height:100%;object-fit:cover;border-radius:0 var(--radius) var(--radius) 0;">
    </div>
  </section>
</div>'''


# ─────────────────────────────────────────────────────────────
# 4. FEATURES
# ─────────────────────────────────────────────────────────────
def build_features(s, c):
    cards = ""
    for f in s["features"]:
        cards += f'''
      <div class="feat-card"><div class="feat-icon">{f["icon"]}</div><div><div class="feat-title">{f["title"]}</div><div class="feat-desc">{f["desc"]}</div></div></div>'''
    return f'''
<section class="features-section">
  <div class="container">
    <p class="sec-label">{s["features_label"]}</p>
    <div class="features-grid">{cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 5. PRICING
# ─────────────────────────────────────────────────────────────
def build_pricing(s, c):
    city = c["city"]
    pricing_title = s["pricing_title"].format(city=city)
    pricing_subtitle = s["pricing_subtitle"]

    tables_html = ""
    for tbl in s["pricing_tables"]:
        # Build column headers
        col_heads = ""
        for col in tbl["columns"]:
            col_heads += f"<th>{col}</th>"

        # Build rows
        rows_html = ""
        for i, row in enumerate(tbl["rows"]):
            cells = ""
            for cell in row:
                cells += f"<td>{cell}</td>"
            if tbl.get("highlight_last") and i == len(tbl["rows"]) - 1:
                rows_html += f'\n            <tr style="background:#f0faf0">{cells}</tr>'
            else:
                rows_html += f"\n            <tr>{cells}</tr>"

        tables_html += f'''
      <div class="pricing-box" style="margin:0">
        <table class="pricing-table">
          <thead><tr><th colspan="{len(tbl["columns"])}">{tbl["header"]}</th></tr>
          <tr>{col_heads}</tr></thead>
          <tbody>{rows_html}
          </tbody>
        </table>
      </div>'''

    pricing_note = s["pricing_note"]

    return f'''
<section class="pricing-section" aria-labelledby="pricing-title">
  <div class="container">
    <p class="sec-label">قائمة الأسعار</p>
    <h2 class="sec-title" id="pricing-title">{pricing_title}</h2>
    <p class="sec-sub">{pricing_subtitle}</p>

    <div style="display:grid;grid-template-columns:1fr;gap:20px;max-width:620px;margin:0 auto 20px">{tables_html}
    </div>

    <p class="pricing-note">{pricing_note}</p>
    <div class="pricing-cta"><a class="btn-outline" href="https://wa.me/971600500200?text=أهلاً،+أريد+{s["service_name_short"]}+في+{city}">تواصل معنا — احجز الآن</a></div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 6. CALCULATOR
# ─────────────────────────────────────────────────────────────
def build_calc(s, c):
    city = c["city"]
    calc_title = s["calc_title"].format(city=city)
    calc_subtitle = s["calc_subtitle"]
    calc_unit_label = s["calc_unit_label"]
    calc_materials_label = s["calc_materials_label"]
    calc_default_display = s["calc_default_display"]
    calc_result_note = s["calc_result_note"]
    wa_text = f"أهلاً+رفيق،+أريد+{s['service_name_short']}+في+{city}.+التكلفة+المبدئية+حسب+الحاسبة:"

    # Build options
    options_html = ""
    for opt in s["calc_options"]:
        selected = " selected" if opt.get("selected") else ""
        options_html += f'\n          <option value="{opt["value"]}"{selected}>{opt["label"]}</option>'

    # Build MATERIALS JS dict
    mat_pairs = ",".join(f'{k}:{v}' for k, v in s["calc_materials"].items())

    return f'''
<section class="calc-section" aria-labelledby="calc-title">
  <div class="container">
    <p class="sec-label">احسب تكلفتك</p>
    <h2 class="sec-title" id="calc-title">{calc_title}</h2>
    <p class="sec-sub">{calc_subtitle}</p>
    <div class="calc-box">
      <div class="calc-field">
        <label class="calc-label" for="calc-type">{calc_unit_label}</label>
        <select class="calc-select" id="calc-type" onchange="calcUpdate()">{options_html}
        </select>
      </div>
      <div class="calc-field">
        <label class="calc-label" for="calc-rooms">{calc_unit_label}: <span id="rooms-display">1</span></label>
        <div class="calc-slider-wrap">
          <span style="font-size:12px;color:var(--muted)">5</span>
          <input class="calc-slider" type="range" id="calc-rooms" min="1" max="5" value="1" oninput="document.getElementById('rooms-display').textContent=this.value;calcUpdate()">
          <span style="font-size:12px;color:var(--muted)">1</span>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
        <input type="checkbox" id="calc-materials" onchange="calcUpdate()" style="width:18px;height:18px;cursor:pointer;accent-color:var(--green)">
        <label for="calc-materials" style="font-size:14px;font-weight:600;cursor:pointer">{calc_materials_label}</label>
      </div>
      <div class="calc-result" aria-live="polite">
        <div class="calc-result-label">التكلفة التقديرية المبدئية</div>
        <div class="calc-result-range" id="calc-output">{calc_default_display}</div>
        <div class="calc-result-note">{calc_result_note}</div>
      </div>
      <div class="calc-cta-reveal" id="calc-cta">
        <p class="price-confirm">تكلفتك التقديرية: <strong id="calc-confirm-price">{calc_default_display}</strong> — احجز الآن وسنؤكد السعر مجاناً</p>
        <a class="btn-whatsapp-solid" href="https://wa.me/971600500200?text={wa_text}" id="calc-wa-btn" target="_blank" rel="noopener" style="width:100%;justify-content:center">واتساب — احجز بهذا السعر</a>
      </div>
    </div>
  </div>
</section>
<script>
var MATERIALS = {{{mat_pairs}}};
function calcUpdate(){{
  var base=parseInt(document.getElementById('calc-type').value);
  var rooms=parseInt(document.getElementById('calc-rooms').value);
  var withMat=document.getElementById('calc-materials').checked;
  var mat=withMat?(MATERIALS[base]||0)*rooms:0;
  var total=base*rooms+mat;
  var txt=total.toLocaleString('ar-EG')+' درهم'+(withMat?' (شامل المواد)':' (تركيب فقط)');
  document.getElementById('calc-output').textContent=txt;
  document.getElementById('calc-confirm-price').textContent=txt;
  var waBtn=document.getElementById('calc-wa-btn');
  waBtn.href='https://wa.me/971600500200?text=أهلاً+رفيق،+أريد+{s["service_name_short"]}+في+{city}.+التكلفة+المبدئية+حسب+الحاسبة:+'+encodeURIComponent(txt);
  document.getElementById('calc-cta').classList.add('show');
}}
</script>'''


# ─────────────────────────────────────────────────────────────
# 7. PERSONAS
# ─────────────────────────────────────────────────────────────
def build_personas(s, c):
    city = c["city"]
    cards = ""
    for p in c["personas"]:
        cards += f'''
      <div class="persona-card">
        <div class="persona-top"><span class="persona-emoji">{p["emoji"]}</span><div><div class="persona-name">{p["name"]}</div><div class="persona-role">{p["role"]}</div></div></div>
        <p class="persona-scenario">{p["scenario"]}</p>
        <div class="persona-price-row"><span class="persona-price-tag">{p["price"]}</span><span class="persona-price-what">{p["detail"]}</span></div>
      </div>'''
    return f'''
<section class="persona-section" aria-labelledby="persona-title">
  <div class="container">
    <p class="sec-label">أمثلة تسعير حقيقية</p>
    <h2 class="sec-title" id="persona-title">من يحتاج {s["service_name"]} في {city}؟</h2>
    <p class="sec-sub">حالات حقيقية من عملاء رفيق في {city}</p>
    <div class="persona-grid">{cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 8. PROOF (stats + reviews)
# ─────────────────────────────────────────────────────────────
def build_proof(s, c):
    review_cards = ""
    for i, r in enumerate(c["reviews"]):
        avatar_url = AVATAR_URLS[i] if i < len(AVATAR_URLS) else AVATAR_URLS[0]
        svg_fallback = f"data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 44 44%22%3E%3Ccircle cx=%2222%22 cy=%2222%22 r=%2222%22 fill=%22%23189F18%22/%3E%3Ctext x=%2222%22 y=%2228%22 text-anchor=%22middle%22 fill=%22white%22 font-size=%2220%22 font-family=%22Cairo%22%3E{r['initial']}%3C/text%3E%3C/svg%3E"
        if i == 0:
            onerror = f"this.style.background='#189F18';this.style.borderRadius='50%';this.src='{svg_fallback}'"
        elif i == 1:
            onerror = f"this.style.background='#189F18';this.src='{svg_fallback}'"
        else:
            onerror = f"this.src='{svg_fallback}'"
        review_cards += f'''
      <div class="review-card">
        <div class="review-top">
          <img class="review-avatar" src="{avatar_url}" alt="{r['name']}" width="44" height="44" loading="lazy" onerror="{onerror}">
          <div><div class="review-name">{r['name']}</div><div class="review-stars">★★★★★</div></div>
        </div>
        <p class="review-text">{r['text']}</p>
      </div>'''
    return f'''
<section class="proof-section" aria-labelledby="proof-title">
  <div class="container">
    <p class="sec-label">أرقامنا تتحدث</p>
    <h2 class="sec-title" id="proof-title">نفتخر بخدمة 135,000 صاحب منزل</h2>
    <p class="sec-sub">في دولة الإمارات العربية المتحدة</p>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-num">135<em>,000</em></div><div class="stat-label">صاحب منزل يثق برفيق</div></div>
      <div class="stat-card"><div class="stat-num"><em>+</em>4,500</div><div class="stat-label">مقدم خدمة معتمد</div></div>
      <div class="stat-card"><div class="stat-num">4.8<em>/5</em></div><div class="stat-label">متوسط تقييم العملاء</div></div>
      <div class="stat-card"><div class="stat-num"><em>+</em>7</div><div class="stat-label">سنوات من التميّز</div></div>
    </div>
    <div class="reviews-grid">{review_cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 9. PROVIDERS
# ─────────────────────────────────────────────────────────────
def build_providers(s, c):
    city = c["city"]
    cards = ""
    for p in c["providers"]:
        cards += f'''
      <div class="provider-card">
        <div class="provider-badge">{p["badge"]}</div>
        <div class="provider-name">{p["name"]}</div>
        <div class="provider-stars">★★★★★ <span class="provider-rating-num">{p["rating"]}</span></div>
        <p class="provider-desc">{p["desc"]}</p>
        <div class="provider-meta">
          <div class="provider-address">📍 {p["location"]}</div>
          <div class="provider-jobs">✅ {p["jobs"]} مهمة</div>
          <span class="provider-tag">{p["tag"]}</span>
        </div>
      </div>'''
    return f'''
<section class="providers-section" aria-labelledby="providers-title">
  <div class="container">
    <p class="sec-label">مقدمو الخدمة المميزون</p>
    <h2 class="sec-title" id="providers-title">أفضل فنيي {s["service_name_short"]} عند رفيق في {city}</h2>
    <p class="sec-sub">فنيون معتمدون متخصصون في {s["service_name_short"]}</p>
    <div class="providers-grid">{cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 10. COMPARE (Pro vs DIY)
# ─────────────────────────────────────────────────────────────
def build_compare(s, c):
    compare_title = s["compare_title"]
    compare_subtitle = s["compare_subtitle"]

    rows_html = ""
    for row in s["compare_rows"]:
        rows_html += f'''
          <tr><td>{row["criteria"]}</td><td><span class="ico-yes">{row["pro"]}</span></td><td><span class="ico-no">{row["diy"]}</span></td></tr>'''

    return f'''
<section class="compare-section" aria-labelledby="compare-title">
  <div class="container">
    <p class="sec-label">{s["compare_label"]}</p>
    <h2 class="sec-title" id="compare-title">{compare_title}</h2>
    <p class="sec-sub">{compare_subtitle}</p>
    <div class="compare-table-wrap">
      <table class="compare-table">
        <thead><tr><th>المعيار</th><th class="pro">فني رفيق المعتمد ✅</th><th class="diy">بنفسك</th></tr></thead>
        <tbody>{rows_html}
        </tbody>
      </table>
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 11. INFOGRAPHIC
# ─────────────────────────────────────────────────────────────
def build_infographic(s, c):
    city = c["city"]
    info = c["infographic"]
    infographic_title = s["infographic_title"].format(city=city)
    infographic_subtitle = s["infographic_subtitle"]

    return f'''
<section class="infographic-section" aria-labelledby="info-title">
  <div class="container">
    <p class="sec-label">{s["infographic_label"]}</p>
    <h2 class="sec-title" id="info-title">{infographic_title}</h2>
    <p class="sec-sub" style="margin-bottom:40px">{infographic_subtitle}</p>
    <div class="infographic-grid">
      <div class="info-card"><span class="info-icon">🚿</span><div class="info-num">{info["jobs"]}</div><div class="info-label">{s["service_name_short"]} في {city}</div></div>
      <div class="info-card"><span class="info-icon">⭐</span><div class="info-num">{info["rating"]}</div><div class="info-label">تقييم متوسط للفنيين</div></div>
      <div class="info-card"><span class="info-icon">👷</span><div class="info-num">{info["technicians"]}</div><div class="info-label">فني معتمد</div></div>
      <div class="info-card"><span class="info-icon">📐</span><div class="info-num">{info["sqm"]}</div><div class="info-label">متر مربع مُركَّب</div></div>
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 12. CITIES SECTION
# ─────────────────────────────────────────────────────────────
def build_cities_section(s, c):
    city = c["city"]
    emoji = c["emoji"]
    neighborhoods = c["neighborhoods"]
    cities_price = s["cities_section_price"]

    other_cards = ""
    for oc in c["other_cities_cards"]:
        other_cards += f'''
      <div class="city-card">
        <a href="/{oc["slug"]}/" style="text-decoration:none;color:inherit;display:block">
        <div class="city-card-name">{oc["name"]} {oc["emoji"]}</div>
        <span class="city-card-tag" style="color:var(--green)">متاح الآن</span>
        <div class="city-card-areas">{oc["areas"]}</div>
        <div class="city-card-price">{oc["price"]}</div>
        </a>
      </div>'''
    return f'''
<section class="city-section" aria-labelledby="city-title">
  <div class="container">
    <p class="sec-label">مناطق الخدمة</p>
    <h2 class="sec-title" id="city-title">أسعار {s["service_name_short"]} حسب المدينة</h2>
    <p class="sec-sub">خدمة متاحة في جميع الإمارات — بدون رسوم زيارة مخفية</p>
    <div class="city-cards">
      <div class="city-card active">
        <div class="city-card-name">{city} {emoji}</div>
        <span class="city-card-tag">موقعك الحالي</span>
        <div class="city-card-areas">{neighborhoods}</div>
        <div class="city-card-price">{cities_price}</div>
      </div>{other_cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 13. CONTENT (body HTML)
# ─────────────────────────────────────────────────────────────
def build_content(s, c):
    city = c["city"]
    body_neighborhoods = c["body_neighborhoods_html"]
    body_html = s["body_content_html"].format(city=city, body_neighborhoods=body_neighborhoods)
    # Append city-specific extra body paragraph if defined
    city_extra = c.get("city_body_extra_html", "")
    if city_extra:
        body_html += "\n      " + city_extra.format(city=city)
    return f'''
<section class="content-section" aria-label="محتوى تفصيلي">
  <div class="container">
    <div class="content-body">
      {body_html}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 14. STEPS
# ─────────────────────────────────────────────────────────────
def build_steps(s, c):
    city = c["city"]
    steps_title = s["steps_title"]
    steps_subtitle = s["steps_subtitle"]

    cards = ""
    for step in s["steps"]:
        desc = step["desc"].format(city=city)
        cards += f'''
      <div class="step-card"><div class="step-num">{step["num"]}</div><div class="step-title">{step["title"]}</div><div class="step-desc">{desc}</div></div>'''

    return f'''
<section class="steps-section" aria-labelledby="steps-title">
  <div class="container">
    <p class="sec-label">{s["steps_label"]}</p>
    <h2 class="sec-title" id="steps-title">{steps_title}</h2>
    <p class="sec-sub" style="margin-bottom:40px">{steps_subtitle}</p>
    <div class="steps-grid">{cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 15. BEFORE / AFTER
# ─────────────────────────────────────────────────────────────
def build_before_after(s, c):
    city = c["city"]
    ba_title = s["ba_title"].format(city=city)
    ba_subtitle = s["ba_subtitle"]
    ba_image = s["before_after_image"]

    # Before stats
    before_stats = ""
    for st in s["ba_before_stats"]:
        before_stats += f'\n            <div class="ba-stat {st["type"]}"><span class="ba-ico">{st["icon"]}</span><strong>{st["label"]}</strong><small>{st["detail"]}</small></div>'

    # After stats
    after_stats = ""
    for st in s["ba_after_stats"]:
        after_stats += f'\n            <div class="ba-stat {st["type"]}"><span class="ba-ico">{st["icon"]}</span><strong>{st["label"]}</strong><small>{st["detail"]}</small></div>'

    # Footer items
    footer_items = ""
    for item in s["ba_footer_items"]:
        footer_items += f"<span>{item}</span>"

    return f'''
<section class="media-section" aria-labelledby="media-title">
  <div class="container">
    <p class="sec-label">وسائط بصرية</p>
    <h2 class="sec-title" id="media-title">{ba_title}</h2>
    <p class="sec-sub" style="margin-bottom:28px">{ba_subtitle}</p>
    <div class="ba-card">
      <div class="ba-img-wrap" style="position:relative;overflow:hidden">
        <img src="{ba_image}" alt="{s["service_name"]} في {city} — قبل وبعد خدمة رفيق" width="1024" height="576" loading="eager" style="width:100%;height:auto;display:block">
        <div class="ba-img-labels" style="direction:ltr">
          <span class="ba-img-label bad">قبل التجديد</span>
          <span class="ba-img-label good">بعد التجديد</span>
        </div>
      </div>
      <div class="ba-split" style="direction:ltr">
        <div class="ba-side ba-before" style="direction:rtl">
          <div class="ba-label-badge">قبل التجديد</div>
          <div class="ba-icon-row">{before_stats}
          </div>
          <div class="ba-desc">{s["ba_before_desc"]}</div>
        </div>
        <div class="ba-divider">→</div>
        <div class="ba-side ba-after" style="direction:rtl">
          <div class="ba-label-badge after">بعد التجديد</div>
          <div class="ba-icon-row">{after_stats}
          </div>
          <div class="ba-desc">{s["ba_after_desc"]}</div>
        </div>
      </div>
      <div class="ba-footer">
        {footer_items}
      </div>
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 16. MAP
# ─────────────────────────────────────────────────────────────
def build_map(s, c):
    city = c["city"]
    neighborhoods = c["neighborhoods"]
    map_url = c["map_embed"]
    return f'''
<section class="map-section" aria-labelledby="map-title">
  <div class="container">
    <p class="sec-label">نطاق الخدمة</p>
    <h2 class="sec-title" id="map-title">نطاق خدمتنا في {city}</h2>
    <p class="sec-sub" style="margin-bottom:24px">نغطي جميع مناطق {city}: {neighborhoods}، والمناطق الأخرى</p>
    <div class="map-wrap">
      <iframe src="{map_url}" width="100%" height="360" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{s["service_name"]} رفيق في {city}"></iframe>
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 17. FAQ
# ─────────────────────────────────────────────────────────────
def build_faq(s, c):
    city = c["city"]
    neighborhoods_full = c["neighborhoods_full"]
    faq_title = s["faq_title"].format(city=city)
    faq_subtitle = s["faq_subtitle"]

    items = ""
    all_faqs = list(s["faqs"]) + list(c.get("city_faqs", []))
    for faq in all_faqs:
        q = faq["q"].format(city=city, neighborhoods_full=neighborhoods_full)
        a = faq["a"].format(city=city, neighborhoods_full=neighborhoods_full)
        items += f'''
      <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <summary itemprop="name">{q}</summary>
        <div class="faq-answer" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
          <p itemprop="text">{a}</p>
        </div>
      </details>'''

    return f'''
<section class="faq-section" aria-labelledby="faq-title">
  <div class="container">
    <p class="sec-label">{s["faq_label"]}</p>
    <h2 class="sec-title" id="faq-title">{faq_title}</h2>
    <p class="sec-sub" style="margin-bottom:32px">{faq_subtitle}</p>
    <div class="faq-list">{items}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 18. WHATSAPP SHARE
# ─────────────────────────────────────────────────────────────
def build_wa_share(s, c):
    city = c["city"]
    slug = c["slug"]
    return f'''
<section class="whatsapp-share-section">
  <div class="container">
    <div class="whatsapp-share-box">
      <h3>هل أعجبك ما قرأت؟</h3>
      <p>شارك هذه الصفحة مع أصدقائك المحتاجين لـ{s["service_name_short"]} في {city}</p>
      <a class="btn-whatsapp-solid" href="https://wa.me/?text=احجز+{s["service_name_short"]}+في+{city}+مع+رفيق+https://hub.rafeeg.ae/{slug}/" target="_blank" rel="noopener">{WA} شارك عبر واتساب</a>
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 19. INTERNAL LINKS
# ─────────────────────────────────────────────────────────────
def build_links(s, c):
    cards = ""
    for link in c["internal_links"]:
        cards += f'''
      <a class="link-card" href="{link["href"]}"><div class="link-card-title">{link["title"]}</div><div class="link-card-desc">{link["desc"]}</div></a>'''
    return f'''
<section class="links-section" aria-labelledby="links-title">
  <div class="container">
    <p class="sec-label">خدمات ذات صلة</p>
    <h2 class="sec-title" id="links-title">اكتشف المزيد من خدمات السيراميك</h2>
    <p class="sec-sub" style="margin-bottom:28px">اختر ما يناسب احتياجك</p>
    <div class="links-grid">{cards}
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 20. CTA BANNER
# ─────────────────────────────────────────────────────────────
def build_cta(s, c):
    city = c["city"]
    cta_title = s["cta_title"].format(city=city)
    cta_subtitle = s["cta_subtitle"].format(city=city)

    seals_html = ""
    for seal in s["guarantee_seals"]:
        icon_svg = GUARANTEE_ICON_MAP.get(seal.get("icon_key") or seal.get("icon", "shield"), GUARANTEE_ICON_MAP["shield"])
        seals_html += f'\n      <div class="guarantee-seal">{icon_svg}{seal["text"].format(city=city)}</div>'

    return f'''
<section class="cta-banner">
  <div class="container">
    <h2>{cta_title}</h2>
    <p>{cta_subtitle}</p>
    <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:24px">{seals_html}
    </div>
    <div class="cta-buttons">
      <a class="btn-green" href="https://rafeeggoogle.onelink.me/C8Hp/news" style="font-size:17px;padding:16px 36px;">{APP} حمّل التطبيق الآن</a>
      <a class="btn-whatsapp" href="https://wa.me/971600500200?text=أهلاً،+أريد+{s["service_name_short"]}+في+{city}" target="_blank" rel="noopener" style="font-size:17px;padding:15px 36px;">{WA} تواصل عبر واتساب</a>
    </div>
  </div>
</section>'''


# ─────────────────────────────────────────────────────────────
# 21. FOOTER + FLOATING WA + STICKY CTA + INTERSECTION OBSERVER
# ─────────────────────────────────────────────────────────────
def build_footer(s, c):
    city = c["city"]
    return f'''
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <img class="footer-logo-img" src="https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png" alt="تطبيق رفيق" width="110" height="40" loading="lazy">
        <p class="footer-about">رفيق — تطبيق الخدمات المنزلية الأول في الإمارات. يربطك بأكثر من 4,500 مقدم خدمة معتمد في دبي وأبوظبي والشارقة وعجمان.</p>
        <a class="btn-green" href="https://rafeeggoogle.onelink.me/C8Hp/news" style="font-size:14px;padding:10px 20px;">📱 حمّل التطبيق</a>
      </div>
      <div>
        <div class="footer-col-title">روابط سريعة</div>
        <ul class="footer-links">
          <li><a href="https://hub.rafeeg.ae/">الرئيسية</a></li>
          <li><a href="https://ar.rafeeg.ae/about-us/">من نحن</a></li>
          <li><a href="https://ar.rafeeg.ae/contact-us/">تواصل معنا</a></li>
          <li><a href="https://ar.rafeeg.ae/rafeeg-franchise/">فرص الاستثمار</a></li>
          <li><a href="https://ar.rafeeg.ae/faqs/">الأسئلة الشائعة</a></li>
          <li><a href="https://en.rafeeg.ae/">English</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">تواصل معنا</div>
        <ul class="footer-links">
          <li><a href="tel:+971600500200">📞 600-500-200</a></li>
          <li><a href="https://wa.me/971600500200?text=أهلاً،+أريد+{s["service_name_short"]}+في+{city}" target="_blank" rel="noopener">💬 واتساب</a></li>
          <li><a href="mailto:info@rafeeg.ae">✉️ info@rafeeg.ae</a></li>
          <li><span style="color:#6b7280">📍 {city}، الإمارات العربية المتحدة</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">© 2025 رفيق. جميع الحقوق محفوظة.</p>
      <div class="social-links">
        <a href="https://www.instagram.com/rafeegapp" aria-label="Instagram" target="_blank" rel="noopener">{INSTAGRAM}</a>
        <a href="https://www.tiktok.com/@rafeeg.ae" aria-label="TikTok" target="_blank" rel="noopener">{TIKTOK}</a>
        <a href="https://www.linkedin.com/company/rafeeg/" aria-label="LinkedIn" target="_blank" rel="noopener">{LINKEDIN}</a>
      </div>
    </div>
  </div>
</footer>

<a class="float-wa" href="https://wa.me/971600500200?text=أهلاً،+أريد+{s["service_name_short"]}+في+{city}" target="_blank" rel="noopener" aria-label="تواصل معنا عبر واتساب">
  <span class="float-wa-label">تواصل معنا</span>
  {WA_FLOAT}
</a>
<div class="sticky-cta" id="sticky-cta" role="complementary" aria-label="حجز سريع">
  <a class="btn-whatsapp-solid" href="https://wa.me/971600500200?text=أهلاً+رفيق،+أريد+{s["service_name_short"]}+في+{city}" target="_blank" rel="noopener">💬 واتساب — احجز الآن</a>
  <a class="btn-green" href="https://rafeeggoogle.onelink.me/C8Hp/news">📱 حمّل التطبيق</a>
</div>
<script>
(function(){{
  var sticky=document.getElementById('sticky-cta');
  var hero=document.querySelector('.hero-wrap');
  if(!sticky||!hero)return;
  var observer=new IntersectionObserver(function(entries){{
    sticky.style.display=entries[0].isIntersecting?'none':'flex';
  }},{{threshold:0.1}});
  observer.observe(hero);
}})();
</script>
</body>
</html>'''


# ─────────────────────────────────────────────────────────────
# Convenience: build full page
# ─────────────────────────────────────────────────────────────
def build_page(s, c):
    """Generate complete HTML page. Returns HTML string."""
    return (
        build_head(s, c)
        + build_header(s, c)
        + build_hero(s, c)
        + build_features(s, c)
        + build_pricing(s, c)
        + build_calc(s, c)
        + build_personas(s, c)
        + build_proof(s, c)
        + build_providers(s, c)
        + build_compare(s, c)
        + build_infographic(s, c)
        + build_cities_section(s, c)
        + build_content(s, c)
        + build_steps(s, c)
        + build_before_after(s, c)
        + build_map(s, c)
        + build_faq(s, c)
        + build_wa_share(s, c)
        + build_links(s, c)
        + build_cta(s, c)
        + build_footer(s, c)
    )
