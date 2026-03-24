#!/usr/bin/env python3
"""
Rafeeg Page Builder
Usage: python3 _build_page.py _configs/تركيب-مكيفات-الشارقة.json
Reads base template + JSON config → writes output/SLUG/index.html
"""
import json, sys, os, re

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '_base_service_template.html')

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

def build_schema(c):
    slug = c['slug']
    city = c['city']
    service = c['service_name']
    base_price = c['base_price']
    faqs = c['faq_items']

    faq_entities = ',\n'.join([
        f'{{"@type":"Question","name":"{f["q"]}","acceptedAnswer":{{"@type":"Answer","text":"{f["a"]}"}}}}'
        for f in faqs
    ])

    steps_json = ',\n'.join([
        f'{{"@type":"HowToStep","position":{i+1},"name":"{s["title"]}","text":"{s["desc"]}"}}'
        for i, s in enumerate(c.get('steps', [
            {"title": "حمّل التطبيق وسجّل", "desc": f"أدخل عنوانك في {city} ونوع المكيف."},
            {"title": "اختر الخدمة والموعد", "desc": "حدد نوع الخدمة ووقتاً يناسبك."},
            {"title": "تأكيد الحجز والسعر", "desc": "ستستقبل تأكيداً فورياً بتفاصيل الفني والسعر."},
            {"title": "وصول الفني المعتمد", "desc": "يصل الفني في الوقت المحدد بجميع أدواته."},
            {"title": "الخدمة والتقييم", "desc": "بعد الانتهاء تُقيّم الفني ونضمن رضاك."}
        ]))
    ])

    return f'''{{
  "@context": "https://schema.org",
  "@graph": [
    {{"@type":"LocalBusiness","@id":"https://ar.rafeeg.ae/#organization","name":"رفيق","url":"https://ar.rafeeg.ae","logo":"https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png","telephone":"+971600500200","email":"info@rafeeg.ae","address":{{"@type":"PostalAddress","addressLocality":"{city}","addressRegion":"{city}","addressCountry":"AE"}},"aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"135000","bestRating":"5"}},"sameAs":["https://www.instagram.com/rafeegapp","https://www.linkedin.com/company/rafeeg/","https://www.tiktok.com/@rafeeg.ae"]}},
    {{"@type":"Service","name":"{service} في {city}","description":"خدمة {service} في {city} من مقدمي خدمة معتمدين عبر تطبيق رفيق","provider":{{"@id":"https://ar.rafeeg.ae/#organization"}},"areaServed":{{"@type":"City","name":"{city}"}},"serviceType":"{service}","offers":{{"@type":"Offer","priceCurrency":"AED","priceSpecification":{{"@type":"PriceSpecification","minPrice":"{base_price}","priceCurrency":"AED"}}}}}},
    {{"@type":"HowTo","name":"كيف تحجز {service} في {city} عبر رفيق","step":[{steps_json}]}},
    {{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"الرئيسية","item":"https://hub.rafeeg.ae/"}},{{"@type":"ListItem","position":2,"name":"{c['parent_name']}","item":"https://hub.rafeeg.ae/{c['parent_slug']}/"}},{{"@type":"ListItem","position":3,"name":"{service} في {city}","item":"https://hub.rafeeg.ae/{slug}/"}}]}},
    {{"@type":"FAQPage","mainEntity":[{faq_entities}]}}
  ]
}}'''

def build(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        c = json.load(f)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Build composite blocks
    persona_cards   = ''.join(build_persona_card(p) for p in c['personas'])
    provider_cards  = ''.join(build_provider_card(p) for p in c['providers'])
    review_cards    = ''.join(build_review_card(r) for r in c['reviews'])
    faq_items       = ''.join(build_faq_item(f) for f in c['faq_items'])
    info_items      = ''.join(build_info_card(i) for i in c['info_items'])
    city_cards      = ''.join(build_city_card(c2) for c2 in c['city_cards'])
    link_cards      = ''.join(build_link_card(l) for l in c['links_cards'])
    pricing_rows    = build_pricing_rows(c['pricing_rows'])
    compare_rows    = build_compare_rows(c['compare_rows'])
    ba_before_stats = build_ba_stats(c['ba_before_stats'])
    ba_after_stats  = build_ba_stats(c['ba_after_stats'])
    schema_json     = build_schema(c)

    calc_options = ''
    for opt in c['calc_options']:
        calc_options += f'<option value="{opt["min"]},{opt["max"]}">{opt["label"]}</option>\n          '

    # Replacements map
    replacements = {
        '{{SLUG}}':           c['slug'],
        '{{PAGE_TITLE}}':     c['page_title'],
        '{{META_DESC}}':      c['meta_desc'],
        '{{OG_DESC}}':        c['og_desc'],
        '{{SERVICE_NAME}}':   c['service_name'],
        '{{CITY}}':           c['city'],
        '{{BASE_PRICE}}':     str(c['base_price']),
        '{{PARENT_SLUG}}':    c['parent_slug'],
        '{{PARENT_NAME}}':    c['parent_name'],
        '{{WA_MSG}}':         c['wa_msg'],
        '{{HERO_H2}}':        c['hero_h2'],
        '{{HERO_SUB}}':       c['hero_sub'],
        '{{HERO_BULLETS}}':   ''.join(f'<li><span class="chk" aria-hidden="true">✓</span> {b}</li>\n        ' for b in c['hero_bullets']),
        '{{PRICING_ROWS}}':   pricing_rows,
        '{{PRICING_NOTE}}':   c['pricing_note'],
        '{{CALC_OPTIONS}}':   calc_options,
        '{{CALC_INIT}}':      c['calc_init'],
        '{{PERSONA_TITLE}}':  c['persona_title'],
        '{{PERSONA_SUB}}':    c['persona_sub'],
        '{{PERSONA_CARDS}}':  persona_cards,
        '{{REVIEWS}}':        review_cards,
        '{{PROVIDERS_TITLE}}':c['providers_title'],
        '{{PROVIDERS_SUB}}':  c['providers_sub'],
        '{{PROVIDER_CARDS}}': provider_cards,
        '{{COMPARE_TITLE}}':  c['compare_title'],
        '{{COMPARE_SUB}}':    c['compare_sub'],
        '{{COMPARE_ROWS}}':   compare_rows,
        '{{INFO_LABEL}}':     c['info_label'],
        '{{INFO_TITLE}}':     c['info_title'],
        '{{INFO_SUB}}':       c['info_sub'],
        '{{INFO_ITEMS}}':     info_items,
        '{{CITY_CARDS}}':     city_cards,
        '{{BODY_CONTENT}}':   c['body_content'],
        '{{FAQ_ITEMS}}':      faq_items,
        '{{LINKS_CARDS}}':    link_cards,
        '{{CTA_H2}}':         c['cta_h2'],
        '{{CTA_P}}':          c['cta_p'],
        '{{READING_TIME}}':   str(c.get('reading_time', 12)),
        '{{H1_TEXT}}':        c.get('h1_text', c['service_name'] + ' في ' + c['city'] + ' — رفيق'),
        '{{BA_BEFORE_STATS}}':ba_before_stats,
        '{{BA_BEFORE_DESC}}': c['ba_before_desc'],
        '{{BA_AFTER_STATS}}': ba_after_stats,
        '{{BA_AFTER_DESC}}':  c['ba_after_desc'],
        '{{BA_FOOTER}}':      ''.join(f'<span>{item}</span>' for item in c['ba_footer']),
        '{{MAP_IFRAME_SRC}}': c['map_iframe_src'],
        '{{MAP_COVERAGE}}':   c['map_coverage'],
        '{{SCHEMA_JSON}}':    schema_json,
    }

    for key, val in replacements.items():
        html = html.replace(key, val)

    # Write output
    out_dir = os.path.join(os.path.dirname(__file__), c['slug'])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✅ Built: {out_path}')
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
