#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Unified CLI for building Rafeeg service pages.

Usage:
  python build.py bathroom_ceramic                    # build ALL cities
  python build.py bathroom_ceramic أبوظبي             # build single city
  python build.py bathroom_ceramic الشارقة أبوظبي     # build specific cities
  python build.py --list                              # list available services

To create a new service type:
  1. Copy services/bathroom_ceramic.py → services/new_service.py
  2. Change SERVICE_CONFIG values (~200 lines of data)
  3. Add city configs to CITIES dict (~50 lines each)
  4. Run: python build.py new_service
"""
import os
import sys
import importlib

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from engine.shared import build_page


def get_available_services():
    """Scan services/ directory for available service modules."""
    services_dir = os.path.join(BASE, "services")
    services = []
    for f in os.listdir(services_dir):
        if f.endswith(".py") and f != "__init__.py":
            services.append(f[:-3])
    return sorted(services)


def load_service(service_name):
    """Load a service module by name. Returns (SERVICE_CONFIG, CITIES)."""
    try:
        mod = importlib.import_module(f"services.{service_name}")
    except ImportError as e:
        print(f"❌ Service '{service_name}' not found.")
        print(f"   Error: {e}")
        print(f"   Available: {', '.join(get_available_services())}")
        sys.exit(1)

    if not hasattr(mod, "SERVICE_CONFIG") or not hasattr(mod, "CITIES"):
        print(f"❌ Service '{service_name}' is missing SERVICE_CONFIG or CITIES dict.")
        sys.exit(1)

    return mod.SERVICE_CONFIG, mod.CITIES


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print(f"Available services: {', '.join(get_available_services())}")
        sys.exit(0)

    if sys.argv[1] == "--list":
        for s in get_available_services():
            print(f"  • {s}")
        sys.exit(0)

    service_name = sys.argv[1]
    requested_cities = sys.argv[2:] if len(sys.argv) > 2 else None

    service_config, cities = load_service(service_name)

    # Determine which cities to build
    if requested_cities:
        cities_to_build = {}
        for name in requested_cities:
            if name in cities:
                cities_to_build[name] = cities[name]
            else:
                print(f"⚠️  Unknown city: {name}")
                print(f"   Available: {', '.join(cities.keys())}")
                sys.exit(1)
    else:
        cities_to_build = cities

    print(f"🔨 Building {service_name} — {len(cities_to_build)} cities")
    print(f"   Service: {service_config['service_name']}")
    print()

    for city_name, city_config in cities_to_build.items():
        slug = city_config["slug"]
        out_dir = os.path.join(BASE, slug)
        os.makedirs(out_dir, exist_ok=True)

        html = build_page(service_config, city_config)
        out_path = os.path.join(out_dir, "index.html")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ {city_name} — {len(html):,} chars → {out_path}")

    print(f"\n🎉 Done! Built {len(cities_to_build)} pages.")


if __name__ == "__main__":
    main()
