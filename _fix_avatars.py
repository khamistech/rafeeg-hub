#!/usr/bin/env python3
"""Replace placeholder api.example.com avatar URLs in all configs
with real hub.rafeeg.ae/assets/ SVG avatars."""
import json, glob, os

CONFIGS = os.path.join(os.path.dirname(__file__), '_configs')

REPLACEMENTS = {
    'https://api.example.com/avatar1.jpg': 'https://hub.rafeeg.ae/assets/avatar1.svg',
    'https://api.example.com/avatar2.jpg': 'https://hub.rafeeg.ae/assets/avatar2.svg',
    'https://api.example.com/avatar3.jpg': 'https://hub.rafeeg.ae/assets/avatar3.svg',
}

patched = 0
for f in sorted(glob.glob(os.path.join(CONFIGS, '*.json'))):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print(f'⚠️  Bad JSON: {f}: {e}')
        continue

    changed = False
    for review in d.get('reviews', []):
        old = review.get('avatar', '')
        if old in REPLACEMENTS:
            review['avatar'] = REPLACEMENTS[old]
            changed = True

    if changed:
        with open(f, 'w', encoding='utf-8') as fp:
            json.dump(d, fp, ensure_ascii=False, indent=2)
        patched += 1

print(f'✅ Patched {patched} config files.')
