#!/usr/bin/env python3
"""
Orphan page fixer — ensures every page has at least one incoming internal link.

Strategy:
  1. Build full site graph from all configs
  2. For every hub: ensure all its city/spoke pages are in links_cards
  3. For every city/spoke page: ensure its parent hub is in links_cards
  4. For standalone pages (no parent, no children): ensure they appear
     in at least one related page's links_cards
  5. Rebuild only pages whose configs were changed

Run: python3 _fix_orphans.py
"""
import json, os, re, glob, subprocess

DIR        = os.path.dirname(__file__)
CONFIGS    = os.path.join(DIR, '_configs')
BUILD      = os.path.join(DIR, '_build_page.py')

CITY_NAMES = {'أبوظبي', 'دبي', 'الشارقة', 'عجمان'}

# ─────────────────────────────────────────────────────────────────
# Step 1 — Load all configs
# ─────────────────────────────────────────────────────────────────

def load_configs():
    configs = {}
    for f in glob.glob(os.path.join(CONFIGS, '*.json')):
        slug = os.path.basename(f).replace('.json', '')
        try:
            d = json.load(open(f, encoding='utf-8'))
            configs[slug] = d
        except Exception as e:
            print(f'⚠️  Bad JSON: {f}: {e}')
    return configs

# ─────────────────────────────────────────────────────────────────
# Step 2 — Build parent→children and child→parent maps
# ─────────────────────────────────────────────────────────────────

def build_hierarchy(configs):
    parent_to_children = {}   # hub_slug → [city_slug, ...]
    child_to_parent    = {}   # city_slug → hub_slug

    for slug, d in configs.items():
        parent = d.get('parent_slug', '')
        if parent and parent in configs:
            parent_to_children.setdefault(parent, []).append(slug)
            child_to_parent[slug] = parent

    return parent_to_children, child_to_parent

# ─────────────────────────────────────────────────────────────────
# Step 3 — Helpers
# ─────────────────────────────────────────────────────────────────

def links_card_hrefs(d):
    """Return set of slugs already in links_cards."""
    return set(
        lc['href'].strip('/')
        for lc in d.get('links_cards', [])
        if lc.get('href')
    )

def ensure_link(d, slug, title, desc):
    """Add slug to links_cards if not already present. Returns True if changed."""
    existing = links_card_hrefs(d)
    if slug in existing:
        return False
    if 'links_cards' not in d:
        d['links_cards'] = []
    d['links_cards'].append({
        'href':  f'/{slug}/',
        'title': title,
        'desc':  desc
    })
    return True

def service_name(d):
    return d.get('service_name', d.get('slug', ''))

def city_of(d):
    return d.get('city', '')

def save(slug, d):
    path = os.path.join(CONFIGS, f'{slug}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def rebuild(slug):
    cfg = os.path.join(CONFIGS, f'{slug}.json')
    r = subprocess.run(['python3', BUILD, cfg], capture_output=True, text=True)
    status = '✅' if r.returncode == 0 else '❌'
    line = r.stdout.strip().split('\n')[0] if r.stdout else r.stderr.strip()
    print(f'  {status} rebuilt {slug}: {line}')

# ─────────────────────────────────────────────────────────────────
# Step 4 — Main fix logic
# ─────────────────────────────────────────────────────────────────

def fix_orphans():
    configs = load_configs()
    parent_to_children, child_to_parent = build_hierarchy(configs)
    dirty = set()   # slugs whose configs were changed → need rebuild

    print(f'Loaded {len(configs)} configs')
    print(f'Hub→city relationships: {sum(len(v) for v in parent_to_children.values())} pairs\n')

    # ── A: Hub must link to all its city pages ──────────────────
    print('── A: Ensuring hubs link to all city pages ──')
    for hub_slug, children in parent_to_children.items():
        if hub_slug not in configs:
            continue
        hub = configs[hub_slug]
        hub_svc = service_name(hub)
        for child_slug in children:
            if child_slug not in configs:
                continue
            child = configs[child_slug]
            child_city = city_of(child)
            title = f'{hub_svc} {child_city}' if child_city else service_name(child)
            desc  = f'خدمة {hub_svc} في {child_city}' if child_city else f'خدمة {hub_svc}'
            changed = ensure_link(hub, child_slug, title, desc)
            if changed:
                print(f'  + {hub_slug} → {child_slug}')
                save(hub_slug, hub)
                dirty.add(hub_slug)

    # ── B: City/spoke pages must link back to their hub ────────
    print('\n── B: Ensuring city pages link back to their hub ──')
    for child_slug, hub_slug in child_to_parent.items():
        if hub_slug not in configs or child_slug not in configs:
            continue
        child   = configs[child_slug]
        hub     = configs[hub_slug]
        hub_svc = service_name(hub)
        title   = hub_svc
        desc    = f'جميع خدمات {hub_svc} في الإمارات'
        changed = ensure_link(child, hub_slug, title, desc)
        if changed:
            print(f'  + {child_slug} → {hub_slug}')
            save(child_slug, child)
            dirty.add(child_slug)

    # ── C: Hub pages (parent_slug='') must appear somewhere ────
    # Link top-level hubs to each other via related_services if isolated
    print('\n── C: Ensuring top-level hubs are cross-linked ──')
    top_hubs = [s for s, d in configs.items() if d.get('parent_slug', '') == '']

    # Group hubs by theme for smart cross-linking
    AC_HUBS      = {s for s in top_hubs if any(w in s for w in ['مكيف','فريون','تصليح','اصلاح','تنظيف-م'])}
    FLOOR_HUBS   = {s for s in top_hubs if any(w in s for w in ['سيراميك','باركيه','رخام','إيبوكسي','إنترلوك'])}
    WATER_HUBS   = {s for s in top_hubs if any(w in s for w in ['سباكة','تسليك','حمامات'])}
    DECOR_HUBS   = {s for s in top_hubs if any(w in s for w in ['دهان','ستائر','ورق','جبس','نجارة','ديكور'])}

    theme_groups = [AC_HUBS, FLOOR_HUBS, WATER_HUBS, DECOR_HUBS]

    # Build incoming link count from current links_cards
    incoming_count = {s: 0 for s in top_hubs}
    for slug, d in configs.items():
        for lc in d.get('links_cards', []):
            target = lc.get('href', '').strip('/')
            if target in incoming_count:
                incoming_count[target] += 1

    # Add isolated hubs to related hubs' links_cards
    for hub_slug in top_hubs:
        if incoming_count.get(hub_slug, 0) > 0:
            continue  # already has incoming links
        hub = configs[hub_slug]
        hub_svc = service_name(hub)

        # Find theme siblings
        siblings = []
        for group in theme_groups:
            if hub_slug in group:
                siblings = [s for s in group if s != hub_slug]
                break

        if not siblings:
            siblings = [s for s in top_hubs if s != hub_slug][:3]

        # Add this hub to 2 sibling pages' links_cards
        linked_from = 0
        for sibling_slug in siblings[:4]:
            if linked_from >= 2:
                break
            if sibling_slug not in configs:
                continue
            sibling = configs[sibling_slug]
            title   = hub_svc
            desc    = f'خدمة {hub_svc} في الإمارات'
            changed = ensure_link(sibling, hub_slug, title, desc)
            if changed:
                print(f'  + {sibling_slug} → {hub_slug} (cross-link)')
                save(sibling_slug, sibling)
                dirty.add(sibling_slug)
                incoming_count[hub_slug] = incoming_count.get(hub_slug, 0) + 1
                linked_from += 1

    # ── D: Rebuild all dirty pages ─────────────────────────────
    print(f'\n── D: Rebuilding {len(dirty)} modified pages ──')
    if not dirty:
        print('  Nothing to rebuild.')
    else:
        for slug in sorted(dirty):
            rebuild(slug)

    # ── E: Final orphan check ──────────────────────────────────
    print('\n── E: Final orphan check ──')
    # Re-scan built HTML files for actual links
    built_pages = {}
    for path in glob.glob(os.path.join(DIR, '*/index.html')):
        slug = os.path.relpath(path, DIR).split(os.sep)[0]
        with open(path, encoding='utf-8') as f:
            html = f.read()
        hrefs = re.findall(r'href=["\']/([\w\u0600-\u06FF\-]+)/', html)
        built_pages[slug] = set(hrefs)

    incoming = {s: [] for s in built_pages}
    for src, links in built_pages.items():
        for target in links:
            if target in incoming:
                incoming[target].append(src)

    remaining_orphans = [s for s, sources in incoming.items() if len(sources) == 0]
    # Exclude city landing pages (أبوظبي/دبي/etc) which are index pages, not content
    remaining_orphans = [s for s in remaining_orphans if s not in CITY_NAMES]

    if remaining_orphans:
        print(f'  ⚠️  {len(remaining_orphans)} orphans still remain:')
        for o in sorted(remaining_orphans):
            print(f'    - {o}')
    else:
        print(f'  ✅ Zero orphans — all {len(built_pages)} pages have incoming links!')

    print(f'\n✅ Done. {len(dirty)} configs patched, {len(dirty)} pages rebuilt.')

if __name__ == '__main__':
    fix_orphans()
