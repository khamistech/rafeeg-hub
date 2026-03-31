#!/usr/bin/env python3
"""
Rafeeg Page Builder
Usage: python3 _build_page.py _configs/SLUG.json
Reads base template + JSON config → writes output/SLUG/index.html

Routing:
  parent_slug == ""  → _base_hub_template.html   (hub/category page)
  parent_slug != ""  → _base_service_template.html (city service page)
"""
import json, sys, os, re

DIR = os.path.dirname(__file__)
HUB_TEMPLATE_PATH     = os.path.join(DIR, '_base_hub_template.html')
SERVICE_TEMPLATE_PATH = os.path.join(DIR, '_base_service_template.html')

# ══════════════════════════════════════════════════════════════════
# Shared builders (used by both hub + service templates)
# ══════════════════════════════════════════════════════════════════

def build_persona_card(p):
    return f"""
      <div class="persona-card">
        <div class="persona-top">
          <span class="persona-emoji" aria-hidden="true">{p['emoji']}</span>
          <div>
            <div class="persona-name">{p['name']}</div>
            <div class="persona-role">{p['role']}</div>
          </div>
        </div>
        <p class="persona-scenario">{p['scenario']}</p>
        <div class="persona-price-row">
          <span class="persona-price-tag">{p['price']}</span>
          <span class="persona-price-what">{p['what']}</span>
        </div>
      </div>"""

def build_provider_card(p):
    stars_full = '★' * int(float(p['rating']))
    stars_empty = '☆' * (5 - int(float(p['rating'])))
    return f"""
      <div class="provider-card">
        <div class="provider-badge">{p['badge']}</div>
        <div class="provider-name">{p['name']}</div>
        <div class="provider-stars">{stars_full}{stars_empty} <span class="provider-rating-num">{p['rating']}</span></div>
        <p class="provider-desc">{p['desc']}</p>
        <div class="provider-meta">
          <div class="provider-address">📍 {p['address']}</div>
          <div class="provider-jobs">✅ {p['jobs']}</div>
          <span class="provider-tag">{p['tag']}</span>
        </div>
      </div>"""

def build_review_card(r):
    return f"""
      <div class="review-card" itemscope itemtype="https://schema.org/Review">
        <div class="review-top">
          <img class="review-avatar" src="{r['avatar']}" alt="{r['name']}" width="44" height="44" loading="lazy">
          <div>
            <div class="review-name" itemprop="author">{r['name']}</div>
            <div class="review-stars">★★★★★</div>
          </div>
        </div>
        <p class="review-text" itemprop="reviewBody">{r['text']}</p>
      </div>"""

def build_faq_item(f):
    return f"""
      <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <summary itemprop="name">{f['q']}</summary>
        <div class="faq-answer" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
          <p itemprop="text">{f['a']}</p>
        </div>
      </details>"""

def build_info_card(i):
    return f"""
      <div class="info-card">
        <span class="info-icon">{i['icon']}</span>
        <div class="info-num">{i['num']}</div>
        <div class="info-label">{i['label']}</div>
      </div>"""

def build_city_card(c):
    active_class = ' active' if c.get('active') else ''
    active_tag = 'موقعك الحالي' if c.get('active') else 'متاح الآن'
    tag_color = '' if c.get('active') else ' style="color:var(--green)"'
    return f"""
      <div class="city-card{active_class}">
        <div class="city-card-name">{c['name']}</div>
        <span class="city-card-tag"{tag_color}>{active_tag}</span>
        <div class="city-card-areas">{c['areas']}</div>
        <div class="city-card-price">من {c['price']} درهم</div>
      </div>"""

def build_link_card(l):
    return f"""
      <a class="link-card" href="{l['href']}">
        <div class="link-card-title">{l['title']}</div>
        <div class="link-card-desc">{l['desc']}</div>
      </a>"""

def build_pricing_rows(rows):
    html = ''
    for r in rows:
        html += f'<tr><td>{r["name"]}</td><td>{r["price"]}</td></tr>\n          '
    return html

def build_compare_rows(rows):
    html = ''
    for r in rows:
        pro = f'<span class="ico-yes">✓{" " + r["pro_note"] if r.get("pro_note") else ""}</span>'
        diy = f'<span class="ico-no">{r.get("diy_note", "✗")}</span>'
        html += f'<tr><td>{r["label"]}</td><td>{pro}</td><td>{diy}</td></tr>\n          '
    return html

def build_ba_stats(stats):
    html = ''
    for s in stats:
        cls = 'bad' if s.get('bad') else 'good'
        html += f'<div class="ba-stat {cls}"><span class="ba-ico">{s["icon"]}</span><strong>{s["value"]}</strong><small>{s["label"]}</small></div>\n'
    return html

# ══════════════════════════════════════════════════════════════════
# Hub-only builders
# ══════════════════════════════════════════════════════════════════

def build_hub_city_card(h):
    return f"""<a href="/{h['slug']}/" class="hub-city-card">
            <div class="hub-city-top">
              <span class="hub-city-icon">{h['icon']}</span>
              <div>
                <div class="hub-city-name">{h['city']}</div>
                <span class="hub-city-available">متاح اليوم</span>
              </div>
            </div>
            <div class="hub-city-price">يبدأ من <strong>{h['price_from']}</strong> <span>درهم</span></div>
            <div class="hub-city-coverage">{h['coverage']}</div>
            <div class="hub-city-response">⚡ وصول {h['response_time']}</div>
            <div class="hub-city-cta">احجز في {h['city']} ←</div>
          </a>"""

def build_service_chip(s):
    return f"""<a href="{s['href']}" class="service-chip">
            <span class="service-chip-icon">{s['icon']}</span>{s['label']}</a>"""

def build_city_compare_row(r):
    return f"""<tr>
            <td><div class="city-compare-city">
              <span class="city-compare-emoji">{r['icon']}</span>
              <span class="city-compare-name">{r['city']}</span></div></td>
            <td><span class="price-badge">{r['price_from']} — {r['price_to']} درهم</span></td>
            <td>{r['response_time']}</td>
            <td>{r['coverage']}</td>
            <td><a href="/{r['slug']}/" class="compare-book-btn">احجز الآن</a></td>
          </tr>"""

def build_steps(steps):
    arabic_nums = ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨']
    html = ''
    for i, s in enumerate(steps):
        num = arabic_nums[i] if i < len(arabic_nums) else str(i + 1)
        html += f"""<div class="step-card">
              <div class="step-num">{num}</div>
              <div class="step-title">{s['title']}</div>
              <div class="step-desc">{s['desc']}</div>
            </div>"""
    return html

# ══════════════════════════════════════════════════════════════════
# Schema builders
# ══════════════════════════════════════════════════════════════════

def build_schema(c):
    slug = c['slug']
    city = c['city']
    service = c['service_name']
    base_price = c['base_price']
    faqs = c['faq_items']
    date_mod = c.get('date_modified', '2026-03-30')
    lat = c.get('lat', '25.2048')
    lng = c.get('lng', '55.2708')
    wikidata = c.get('wikidata', 'Q612')
    low_price = c.get('low_price', str(base_price))
    high_price = c.get('high_price', str(int(base_price) * 2))
    price_range = c.get('price_range', f'درهم {low_price}–{high_price}')
    is_hub = c.get('parent_slug', '') == ''

    faq_entities = ',\n'.join([
        f'{{"@type":"Question","name":"{f["q"]}","acceptedAnswer":{{"@type":"Answer","text":"{f["a"]}"}}}}'
        for f in faqs
    ])

    steps_json = ',\n'.join([
        f'{{"@type":"HowToStep","position":{i+1},"name":"{s["title"]}","text":"{s["desc"]}"}}'
        for i, s in enumerate(c.get('steps', [
            {"title": "حمّل التطبيق وسجّل", "desc": f"أدخل عنوانك في {city} ونوع الخدمة."},
            {"title": "اختر الخدمة والموعد", "desc": "حدد نوع الخدمة ووقتاً يناسبك."},
            {"title": "تأكيد الحجز والسعر", "desc": "ستستقبل تأكيداً فورياً بتفاصيل الفني والسعر."},
            {"title": "وصول الفني المعتمد", "desc": "يصل الفني في الوقت المحدد بجميع أدواته."},
            {"title": "الخدمة والتقييم", "desc": "بعد الانتهاء تُقيّم الفني ونضمن رضاك."}
        ]))
    ])

    price_specs = ''
    for row in c.get('pricing_rows', []):
        price_val = row['price'].replace(' درهم', '').replace(',', '').split('–')[0].strip()
        price_specs += f'{{"@type":"PriceSpecification","name":"{row["name"]}","price":"{price_val}","priceCurrency":"AED"}},'
    if price_specs:
        price_specs = price_specs.rstrip(',')
        offers_block = f'"offers":{{"@type":"AggregateOffer","priceCurrency":"AED","lowPrice":"{low_price}","highPrice":"{high_price}","priceSpecification":[{price_specs}]}}'
    else:
        offers_block = f'"offers":{{"@type":"Offer","priceCurrency":"AED","price":"{base_price}"}}'

    # Breadcrumb: 2-level for hubs, 3-level for city pages
    if is_hub:
        breadcrumb = f'{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"الرئيسية","item":"https://hub.rafeeg.ae/"}},{{"@type":"ListItem","position":2,"name":"{service}","item":"https://hub.rafeeg.ae/{slug}/"}}]}}'
    else:
        breadcrumb = f'{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"الرئيسية","item":"https://hub.rafeeg.ae/"}},{{"@type":"ListItem","position":2,"name":"{c["parent_name"]}","item":"https://hub.rafeeg.ae/{c["parent_slug"]}/"}},{{"@type":"ListItem","position":3,"name":"{service} في {city}","item":"https://hub.rafeeg.ae/{slug}/"}}]}}'

    # Hub-only: ItemList + WebPage with speakable
    extra_schemas = ''
    if is_hub:
        hub_city_links = c.get('hub_city_links', [])
        if hub_city_links:
            list_items = ',\n'.join([
                f'{{"@type":"ListItem","position":{i+1},"url":"https://hub.rafeeg.ae/{h["slug"]}/","name":"{service} {h["city"]}"}}'
                for i, h in enumerate(hub_city_links)
            ])
            extra_schemas += f''',
    {{"@type":"ItemList","name":"{service} في مدن الإمارات","itemListElement":[{list_items}]}}'''

        extra_schemas += f''',
    {{"@type":"WebPage","@id":"https://hub.rafeeg.ae/{slug}/#webpage","name":"{service} في الإمارات — رفيق","inLanguage":"ar","speakable":{{"@type":"SpeakableSpecification","cssSelector":[".hub-intro-answer",".faq-section"]}}}}'''

    return f'''{{
  "@context": "https://schema.org",
  "@graph": [
    {{"@type":"HomeAndConstructionBusiness","@id":"https://ar.rafeeg.ae/#organization","name":"رفيق","description":"رفيق هو تطبيق إماراتي للخدمات المنزلية، يربط أصحاب المنازل بأكثر من 4,500 فني معتمد في دبي وأبوظبي والشارقة وعجمان.","url":"https://ar.rafeeg.ae","logo":"https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png","telephone":"+971600500200","email":"info@rafeeg.ae","priceRange":"{price_range}","openingHours":"Mo-Su 07:00-22:00","address":{{"@type":"PostalAddress","addressLocality":"{city}","addressRegion":"{city}","addressCountry":"AE"}},"geo":{{"@type":"GeoCoordinates","latitude":"{lat}","longitude":"{lng}"}},"areaServed":[{{"@type":"City","name":"دبي"}},{{"@type":"City","name":"أبوظبي"}},{{"@type":"City","name":"الشارقة"}},{{"@type":"City","name":"عجمان"}}],"aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"135000","bestRating":"5"}},"sameAs":["https://www.instagram.com/rafeegapp","https://www.linkedin.com/company/rafeeg/","https://www.tiktok.com/@rafeeg.ae"]}},
    {{"@type":"Service","name":"{service} في {city}","description":"خدمة {service} في {city} من مقدمي خدمة معتمدين عبر تطبيق رفيق. ضمان على الخدمة، فنيون معتمدون، أسعار شفافة.","dateModified":"{date_mod}","provider":{{"@id":"https://ar.rafeeg.ae/#organization"}},"areaServed":{{"@type":"City","name":"{city}","sameAs":"https://www.wikidata.org/wiki/{wikidata}"}},"serviceType":"{service}",{offers_block}}},
    {{"@type":"HowTo","name":"كيف تحجز {service} في {city} عبر رفيق","step":[{steps_json}]}},
    {breadcrumb},
    {{"@type":"FAQPage","mainEntity":[{faq_entities}]}}{extra_schemas}
  ]
}}'''

# ══════════════════════════════════════════════════════════════════
# Main build function
# ══════════════════════════════════════════════════════════════════

def build(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        c = json.load(f)

    # Route to the correct template
    is_hub = c.get('parent_slug', '') == ''
    template_path = HUB_TEMPLATE_PATH if is_hub else SERVICE_TEMPLATE_PATH

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Build composite blocks (shared)
    persona_cards   = ''.join(build_persona_card(p) for p in c.get('personas', []))
    provider_cards  = ''.join(build_provider_card(p) for p in c.get('providers', []))
    review_cards    = ''.join(build_review_card(r) for r in c.get('reviews', []))
    faq_items       = ''.join(build_faq_item(f) for f in c['faq_items'])
    info_items      = ''.join(build_info_card(i) for i in c.get('info_items', []))
    city_cards      = ''.join(build_city_card(c2) for c2 in c.get('city_cards', []))
    link_cards      = ''.join(build_link_card(l) for l in c.get('links_cards', []))
    pricing_rows    = build_pricing_rows(c.get('pricing_rows', []))
    compare_rows    = build_compare_rows(c.get('compare_rows', []))
    ba_before_stats = build_ba_stats(c.get('ba_before_stats', []))
    ba_after_stats  = build_ba_stats(c.get('ba_after_stats', []))
    schema_json     = build_schema(c)

    calc_options = ''
    for opt in c.get('calc_options', []):
        calc_options += f'<option value="{opt["min"]},{opt["max"]}">{opt["label"]}</option>\n          '

    # Build hub-specific blocks
    hub_city_cards    = ''.join(build_hub_city_card(h) for h in c.get('hub_city_links', []))
    service_chips     = ''.join(build_service_chip(s) for s in c.get('service_types', []))
    city_compare_rows = ''.join(build_city_compare_row(r) for r in c.get('city_compare_rows', []))
    steps_html        = build_steps(c.get('steps', []))
    intro_answer      = c.get('intro_answer', c.get('hero_sub', ''))

    # Replacements map (all placeholders — unused ones become empty string)
    replacements = {
        '{{SLUG}}':             c['slug'],
        '{{PAGE_TITLE}}':       c['page_title'],
        '{{META_DESC}}':        c['meta_desc'],
        '{{OG_DESC}}':          c['og_desc'],
        '{{SERVICE_NAME}}':     c['service_name'],
        '{{CITY}}':             c['city'],
        '{{BASE_PRICE}}':       str(c['base_price']),
        '{{PARENT_SLUG}}':      c.get('parent_slug', ''),
        '{{PARENT_NAME}}':      c.get('parent_name', 'الرئيسية'),
        '{{WA_MSG}}':           c['wa_msg'],
        '{{HERO_H2}}':          c['hero_h2'],
        '{{HERO_SUB}}':         c['hero_sub'],
        '{{HERO_BULLETS}}':     ''.join(f'<li><span class="chk" aria-hidden="true">✓</span> {b}</li>\n        ' for b in c.get('hero_bullets', [])),
        '{{PRICING_ROWS}}':     pricing_rows,
        '{{PRICING_NOTE}}':     c.get('pricing_note', ''),
        '{{CALC_OPTIONS}}':     calc_options,
        '{{CALC_INIT}}':        c.get('calc_init', ''),
        '{{PERSONA_TITLE}}':    c.get('persona_title', ''),
        '{{PERSONA_SUB}}':      c.get('persona_sub', ''),
        '{{PERSONA_CARDS}}':    persona_cards,
        '{{REVIEWS}}':          review_cards,
        '{{PROVIDERS_TITLE}}':  c.get('providers_title', ''),
        '{{PROVIDERS_SUB}}':    c.get('providers_sub', ''),
        '{{PROVIDER_CARDS}}':   provider_cards,
        '{{COMPARE_TITLE}}':    c.get('compare_title', ''),
        '{{COMPARE_SUB}}':      c.get('compare_sub', ''),
        '{{COMPARE_ROWS}}':     compare_rows,
        '{{INFO_LABEL}}':       c.get('info_label', ''),
        '{{INFO_TITLE}}':       c.get('info_title', ''),
        '{{INFO_SUB}}':         c.get('info_sub', ''),
        '{{INFO_ITEMS}}':       info_items,
        '{{CITY_CARDS}}':       city_cards,
        '{{BODY_CONTENT}}':     c.get('body_content', ''),
        '{{FAQ_ITEMS}}':        faq_items,
        '{{LINKS_CARDS}}':      link_cards,
        '{{CTA_H2}}':           c.get('cta_h2', ''),
        '{{CTA_P}}':            c.get('cta_p', ''),
        '{{READING_TIME}}':     str(c.get('reading_time', 12)),
        '{{H1_TEXT}}':          c.get('h1_text', c['service_name'] + ' في ' + c['city'] + ' — رفيق'),
        '{{BA_BEFORE_STATS}}':  ba_before_stats,
        '{{BA_BEFORE_DESC}}':   c.get('ba_before_desc', ''),
        '{{BA_AFTER_STATS}}':   ba_after_stats,
        '{{BA_AFTER_DESC}}':    c.get('ba_after_desc', ''),
        '{{BA_FOOTER}}':        ''.join(f'<span>{item}</span>' for item in c.get('ba_footer', [])),
        '{{MAP_IFRAME_SRC}}':   c.get('map_iframe_src', ''),
        '{{MAP_COVERAGE}}':     c.get('map_coverage', ''),
        '{{SCHEMA_JSON}}':      schema_json,
        # RAK v2 optional fields
        '{{URGENCY_STRIP}}':    c.get('urgency_strip', ''),
        '{{AI_SUMMARY}}':       c.get('ai_summary', ''),
        '{{GUARANTEE_SEALS}}':  c.get('guarantee_seals', ''),
        # Hub-only placeholders
        '{{HUB_CITY_CARDS}}':   hub_city_cards,
        '{{SERVICE_TYPE_CHIPS}}': service_chips,
        '{{CITY_COMPARE_ROWS}}': city_compare_rows,
        '{{STEPS_HTML}}':       steps_html,
        '{{INTRO_ANSWER}}':     intro_answer,
    }

    for key, val in replacements.items():
        html = html.replace(key, val)

    # Write output
    out_dir = os.path.join(DIR, c['slug'])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    template_type = 'HUB' if is_hub else 'SERVICE'
    print(f'✅ [{template_type}] Built: {out_path}')
    print(f'   Lines: {html.count(chr(10))}')
    remaining = re.findall(r'\{\{[A-Z_]+\}\}', html)
    if remaining:
        print(f'   ⚠️  Unfilled placeholders: {set(remaining)}')
    else:
        print(f'   ✓  All placeholders filled')
    return out_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 _build_page.py _configs/SLUG.json')
        sys.exit(1)
    build(sys.argv[1])
