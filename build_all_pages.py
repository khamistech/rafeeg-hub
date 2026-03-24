#!/usr/bin/env python3
"""
Build all 28 new service pages
"""
import subprocess
import os
import glob

os.chdir("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

configs = sorted(glob.glob("_configs/*.json"))

# Exclude the 9 AC configs already built
exclude = [
    "_configs/تركيب-مكيفات-الشارقة.json",
    "_configs/تركيب-مكيفات-أبوظبي.json",
    "_configs/تركيب-مكيفات-دبي.json",
    "_configs/تنظيف-مكيفات-أبوظبي.json",
    "_configs/شحن-فريون-مكيفات-أبوظبي.json",
    "_configs/شحن-فريون-مكيفات-الشارقة.json",
    "_configs/شحن-فريون-مكيفات-دبي.json",
    "_configs/صيانة-مكيفات-أبوظبي.json",
    "_configs/صيانة-مكيفات-دبي.json",
]

new_configs = [c for c in configs if c not in exclude]

print(f"Building {len(new_configs)} pages...\n")

for i, config_path in enumerate(new_configs, 1):
    print(f"[{i}/{len(new_configs)}] Building {config_path}...")
    result = subprocess.run(["python3", "_build_page.py", config_path],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Error: {result.stderr}")
    else:
        print(f"  ✅ Built")

print(f"\n✅ Completed building {len(new_configs)} pages")
