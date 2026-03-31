#!/usr/bin/env python3
"""
Promote existing mid-level service configs to proper top-level hubs.
Changes parent_slug="" and adds hub-specific fields.
Run: python3 _promote_to_hub.py
"""
import json, os, subprocess

CONFIGS_DIR = os.path.join(os.path.dirname(__file__), '_configs')
BUILD_SCRIPT = os.path.join(os.path.dirname(__file__), '_build_page.py')

# ══════════════════════════════════════════════════════════════════
# Hub data for each service being promoted
# ══════════════════════════════════════════════════════════════════

PROMOTIONS = {
    "تركيب-مكيفات": {
        "parent_slug": "",
        "parent_name": "الرئيسية",
        "intro_answer": "تركيب مكيفات في الإمارات من رفيق — فنيون معتمدون يركّبون جميع أنواع المكيفات السبليت والمركزي والشباك بضمان سنة وكفالة على قطع الغيار. وصول نفس اليوم في أبوظبي ودبي والشارقة وعجمان بأسعار تبدأ من 280 درهم.",
        "hub_city_links": [
            {"city": "أبوظبي", "slug": "تركيب-مكيفات-أبوظبي", "price_from": "300", "price_to": "700", "response_time": "نفس اليوم", "coverage": "الريم، الخالدية، مصفح، المرور", "icon": "🌆"},
            {"city": "دبي",    "slug": "تركيب-مكيفات-دبي",    "price_from": "350", "price_to": "750", "response_time": "نفس اليوم", "coverage": "مارينا، داونتاون، JBR، نخلة", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تركيب-مكيفات-الشارقة","price_from": "280", "price_to": "650", "response_time": "نفس اليوم", "coverage": "التعاون، النهدة، الخان", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تركيب-مكيفات-عجمان",  "price_from": "260", "price_to": "600", "response_time": "نفس اليوم", "coverage": "النعيمية، الراشدية، كورنيش", "icon": "🏗️"}
        ],
        "service_types": [
            {"label": "تركيب مكيف سبليت",     "href": "/تركيب-مكيفات-دبي/",    "icon": "❄️"},
            {"label": "تركيب مكيف مركزي",     "href": "/تركيب-مكيفات-أبوظبي/", "icon": "🌬️"},
            {"label": "تركيب مكيف شباك",      "href": "/تركيب-مكيفات-الشارقة/","icon": "🪟"},
            {"label": "تركيب مكيف كاسيت",     "href": "/تركيب-مكيفات-عجمان/",  "icon": "⚙️"},
            {"label": "نقل وتركيب مكيفات",    "href": "/فك-وتركيب-مكيفات/",    "icon": "🔄"},
            {"label": "ضمان تركيب سنة كاملة", "href": "/تركيب-مكيفات-دبي/",    "icon": "🛡️"}
        ],
        "city_compare_rows": [
            {"city": "أبوظبي", "slug": "تركيب-مكيفات-أبوظبي", "price_from": "300", "price_to": "700", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🌆"},
            {"city": "دبي",    "slug": "تركيب-مكيفات-دبي",    "price_from": "350", "price_to": "750", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تركيب-مكيفات-الشارقة","price_from": "280", "price_to": "650", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تركيب-مكيفات-عجمان",  "price_from": "260", "price_to": "600", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏗️"}
        ]
    },
    "تركيب-ستائر": {
        "parent_slug": "",
        "parent_name": "الرئيسية",
        "intro_answer": "تركيب ستائر في الإمارات من رفيق — فنيون متخصصون يركّبون جميع أنواع الستائر والرول بلاند والبلاكاوت بدقة ونظافة تامة. وصول نفس اليوم مع ضمان التركيب بأسعار تبدأ من 56 درهم للستارة.",
        "hub_city_links": [
            {"city": "أبوظبي", "slug": "تركيب-ستائر-أبوظبي", "price_from": "60", "price_to": "200", "response_time": "نفس اليوم", "coverage": "الريم، الخالدية، مصفح، شاطئ الراحة", "icon": "🌆"},
            {"city": "دبي",    "slug": "تركيب-ستائر-دبي",    "price_from": "70", "price_to": "220", "response_time": "نفس اليوم", "coverage": "مارينا، داونتاون، JBR، البرشاء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تركيب-ستائر-الشارقة","price_from": "56", "price_to": "180", "response_time": "نفس اليوم", "coverage": "التعاون، النهدة، الخان", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تركيب-ستائر-عجمان",  "price_from": "50", "price_to": "160", "response_time": "نفس اليوم", "coverage": "النعيمية، الراشدية، المويهات", "icon": "🏗️"}
        ],
        "service_types": [
            {"label": "ستائر رول بلاند",    "href": "/تركيب-ستائر-دبي/",    "icon": "🎞️"},
            {"label": "ستائر بلاكاوت",      "href": "/تركيب-ستائر-أبوظبي/", "icon": "🌑"},
            {"label": "ستائر كلاسيك",       "href": "/تركيب-ستائر-الشارقة/","icon": "👑"},
            {"label": "ستائر زيبرا",        "href": "/تركيب-ستائر-عجمان/",  "icon": "🦓"},
            {"label": "ستائر مجالس",        "href": "/تركيب-ستائر-دبي/",    "icon": "🛋️"},
            {"label": "إزالة وتركيب ستائر", "href": "/تركيب-ستائر-أبوظبي/", "icon": "🔧"}
        ],
        "city_compare_rows": [
            {"city": "أبوظبي", "slug": "تركيب-ستائر-أبوظبي", "price_from": "60", "price_to": "200", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🌆"},
            {"city": "دبي",    "slug": "تركيب-ستائر-دبي",    "price_from": "70", "price_to": "220", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تركيب-ستائر-الشارقة","price_from": "56", "price_to": "180", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تركيب-ستائر-عجمان",  "price_from": "50", "price_to": "160", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏗️"}
        ]
    },
    "تنظيف-مكيفات": {
        "parent_slug": "",
        "parent_name": "الرئيسية",
        "intro_answer": "تنظيف مكيفات في الإمارات من رفيق — فنيون معتمدون يغسلون المكيف من الداخل والخارج بمعدات ضغط متخصصة ومواد تعقيم آمنة. تنظيف شامل يزيد كفاءة التبريد ويمنع الروائح في نفس اليوم بأسعار تبدأ من 64 درهم.",
        "hub_city_links": [
            {"city": "أبوظبي", "slug": "تنظيف-مكيفات-أبوظبي", "price_from": "70", "price_to": "200", "response_time": "نفس اليوم", "coverage": "الريم، الخالدية، مصفح، المرور", "icon": "🌆"},
            {"city": "دبي",    "slug": "تنظيف-مكيفات-دبي",    "price_from": "80", "price_to": "220", "response_time": "نفس اليوم", "coverage": "مارينا، داونتاون، JBR، نخلة", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تنظيف-مكيفات-الشارقة","price_from": "64", "price_to": "180", "response_time": "نفس اليوم", "coverage": "التعاون، النهدة، الخان", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تنظيف-مكيفات-عجمان",  "price_from": "60", "price_to": "160", "response_time": "نفس اليوم", "coverage": "النعيمية، الراشدية", "icon": "🏗️"}
        ],
        "service_types": [
            {"label": "تنظيف مكيف سبليت",      "href": "/تنظيف-مكيفات-دبي/",        "icon": "❄️"},
            {"label": "تنظيف دكتات مركزي",     "href": "/تنظيف-دكتات-مكيفات/",      "icon": "🌬️"},
            {"label": "تعقيم وتطهير مكيفات",   "href": "/تنظيف-مكيفات-أبوظبي/",     "icon": "🧪"},
            {"label": "تنظيف فلاتر مكيفات",    "href": "/تنظيف-مكيفات-الشارقة/",    "icon": "🔧"},
            {"label": "إزالة روائح المكيف",    "href": "/تنظيف-مكيفات-عجمان/",      "icon": "✨"},
            {"label": "عقود صيانة دورية",      "href": "/صيانة-مكيفات/",             "icon": "📋"}
        ],
        "city_compare_rows": [
            {"city": "أبوظبي", "slug": "تنظيف-مكيفات-أبوظبي", "price_from": "70", "price_to": "200", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🌆"},
            {"city": "دبي",    "slug": "تنظيف-مكيفات-دبي",    "price_from": "80", "price_to": "220", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تنظيف-مكيفات-الشارقة","price_from": "64", "price_to": "180", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تنظيف-مكيفات-عجمان",  "price_from": "60", "price_to": "160", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏗️"}
        ]
    },
    "تركيب-جبس-بورد": {
        "parent_slug": "",
        "parent_name": "الرئيسية",
        "intro_answer": "تركيب جبس بورد في الإمارات من رفيق — فنيون متخصصون في تركيب الجبس بورد للأسقف المعلقة والجدران الفاصلة والديكورات الهندسية. تنفيذ احترافي بالمواد الأصلية وضمان سنتين بأسعار تبدأ من 35 درهم للمتر.",
        "hub_city_links": [
            {"city": "أبوظبي", "slug": "تركيب-جبس-بورد-أبوظبي", "price_from": "38", "price_to": "200", "response_time": "يوم عمل",  "coverage": "الريم، الخالدية، مصفح، شاطئ الراحة", "icon": "🌆"},
            {"city": "دبي",    "slug": "تركيب-جبس-بورد-دبي",    "price_from": "42", "price_to": "220", "response_time": "يوم عمل",  "coverage": "مارينا، داونتاون، JBR، نخلة",     "icon": "🏙️"},
            {"city": "الشارقة","slug": "تركيب-جبس-بورد-الشارقة","price_from": "35", "price_to": "180", "response_time": "2-3 أيام", "coverage": "التعاون، النهدة، الخان",            "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تركيب-جبس-بورد-عجمان",  "price_from": "32", "price_to": "160", "response_time": "2-3 أيام", "coverage": "النعيمية، الراشدية، المويهات",     "icon": "🏗️"}
        ],
        "service_types": [
            {"label": "سقف معلق جبس بورد",    "href": "/تركيب-جبس-بورد-دبي/",    "icon": "🏠"},
            {"label": "جدران فاصلة جبس",      "href": "/تركيب-جبس-بورد-أبوظبي/", "icon": "🧱"},
            {"label": "ديكور جبس هندسي",      "href": "/تركيب-جبس-بورد-الشارقة/","icon": "✨"},
            {"label": "جبس بورد للحمامات",    "href": "/تركيب-جبس-بورد-عجمان/",  "icon": "🚿"},
            {"label": "إصلاح جبس بورد",       "href": "/تركيب-جبس-بورد-دبي/",    "icon": "🔧"},
            {"label": "طلاء جبس بورد",        "href": "/تركيب-جبس-بورد-أبوظبي/", "icon": "🎨"}
        ],
        "city_compare_rows": [
            {"city": "أبوظبي", "slug": "تركيب-جبس-بورد-أبوظبي", "price_from": "38", "price_to": "200", "response_time": "يوم عمل",  "coverage": "جميع الأحياء", "icon": "🌆"},
            {"city": "دبي",    "slug": "تركيب-جبس-بورد-دبي",    "price_from": "42", "price_to": "220", "response_time": "يوم عمل",  "coverage": "جميع الأحياء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "تركيب-جبس-بورد-الشارقة","price_from": "35", "price_to": "180", "response_time": "2-3 أيام","coverage": "جميع الأحياء", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "تركيب-جبس-بورد-عجمان",  "price_from": "32", "price_to": "160", "response_time": "2-3 أيام","coverage": "جميع الأحياء", "icon": "🏗️"}
        ]
    },
    "اصلاح-مكيفات": {
        "parent_slug": "",
        "parent_name": "الرئيسية",
        "intro_answer": "إصلاح مكيفات في الإمارات من رفيق — فنيون معتمدون يشخّصون ويصلحون أي عطل في مكيفك في نفس اليوم. نعمل مع جميع الماركات — LG، Samsung، Gree، Daikin، Mitsubishi — بضمان 90 يوماً على كل إصلاح.",
        "hub_city_links": [
            {"city": "أبوظبي", "slug": "اصلاح-مكيفات-أبوظبي", "price_from": "120", "price_to": "500", "response_time": "نفس اليوم", "coverage": "الريم، الخالدية، مصفح، المرور", "icon": "🌆"},
            {"city": "دبي",    "slug": "اصلاح-مكيفات-دبي",    "price_from": "140", "price_to": "550", "response_time": "نفس اليوم", "coverage": "مارينا، داونتاون، JBR، نخلة", "icon": "🏙️"},
            {"city": "الشارقة","slug": "اصلاح-مكيفات-الشارقة","price_from": "110", "price_to": "450", "response_time": "نفس اليوم", "coverage": "التعاون، النهدة، الخان", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "اصلاح-مكيفات-عجمان",  "price_from": "100", "price_to": "400", "response_time": "نفس اليوم", "coverage": "النعيمية، الراشدية، كورنيش", "icon": "🏗️"}
        ],
        "service_types": [
            {"label": "مكيف لا يبرد",       "href": "/مكيف-لا-يبرد/",          "icon": "🌡️"},
            {"label": "مكيف يقطر ماء",      "href": "/اصلاح-مكيفات-دبي/",      "icon": "💧"},
            {"label": "شحن فريون",           "href": "/شحن-فريون-مكيفات/",       "icon": "❄️"},
            {"label": "تبديل كمبروسر",      "href": "/اصلاح-مكيفات-أبوظبي/",   "icon": "⚙️"},
            {"label": "إصلاح ريموت وبورد",  "href": "/اصلاح-مكيفات-الشارقة/",  "icon": "🎮"},
            {"label": "طوارئ إصلاح 24/7",   "href": "/اصلاح-مكيفات-عجمان/",    "icon": "🚨"}
        ],
        "city_compare_rows": [
            {"city": "أبوظبي", "slug": "اصلاح-مكيفات-أبوظبي", "price_from": "120", "price_to": "500", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🌆"},
            {"city": "دبي",    "slug": "اصلاح-مكيفات-دبي",    "price_from": "140", "price_to": "550", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "اصلاح-مكيفات-الشارقة","price_from": "110", "price_to": "450", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "اصلاح-مكيفات-عجمان",  "price_from": "100", "price_to": "400", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏗️"}
        ]
    },
    "شحن-فريون-مكيفات": {
        "parent_slug": "",
        "parent_name": "الرئيسية",
        "intro_answer": "شحن فريون مكيفات في الإمارات من رفيق — فنيون معتمدون يشحنون الفريون بالنوع الأصلي المناسب لمكيفك مع فحص كامل لنظام التبريد. خدمة في نفس اليوم بأسعار شفافة تبدأ من 96 درهم وضمان 90 يوماً.",
        "hub_city_links": [
            {"city": "أبوظبي", "slug": "شحن-فريون-مكيفات-أبوظبي", "price_from": "100", "price_to": "280", "response_time": "نفس اليوم", "coverage": "الريم، الخالدية، مصفح، المرور", "icon": "🌆"},
            {"city": "دبي",    "slug": "شحن-فريون-مكيفات-دبي",    "price_from": "120", "price_to": "300", "response_time": "نفس اليوم", "coverage": "مارينا، داونتاون، JBR، نخلة", "icon": "🏙️"},
            {"city": "الشارقة","slug": "شحن-فريون-مكيفات-الشارقة","price_from": "96",  "price_to": "260", "response_time": "نفس اليوم", "coverage": "التعاون، النهدة، الخان", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "شحن-فريون-مكيفات-عجمان",  "price_from": "90",  "price_to": "240", "response_time": "نفس اليوم", "coverage": "النعيمية، الراشدية", "icon": "🏗️"}
        ],
        "service_types": [
            {"label": "شحن فريون R410A",    "href": "/شحن-فريون-مكيفات-دبي/",    "icon": "❄️"},
            {"label": "شحن فريون R22",      "href": "/شحن-فريون-مكيفات-أبوظبي/", "icon": "🌡️"},
            {"label": "فحص تسرب فريون",     "href": "/شحن-فريون-مكيفات-الشارقة/","icon": "🔍"},
            {"label": "شحن مكيف مركزي",     "href": "/شحن-فريون-مكيفات-عجمان/",  "icon": "🌬️"},
            {"label": "شحن + تنظيف مكيف",  "href": "/تنظيف-مكيفات/",             "icon": "✨"},
            {"label": "طوارئ شحن 24/7",     "href": "/شحن-فريون-مكيفات-دبي/",    "icon": "🚨"}
        ],
        "city_compare_rows": [
            {"city": "أبوظبي", "slug": "شحن-فريون-مكيفات-أبوظبي", "price_from": "100", "price_to": "280", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🌆"},
            {"city": "دبي",    "slug": "شحن-فريون-مكيفات-دبي",    "price_from": "120", "price_to": "300", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏙️"},
            {"city": "الشارقة","slug": "شحن-فريون-مكيفات-الشارقة","price_from": "96",  "price_to": "260", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏘️"},
            {"city": "عجمان",  "slug": "شحن-فريون-مكيفات-عجمان",  "price_from": "90",  "price_to": "240", "response_time": "نفس اليوم","coverage": "جميع الأحياء", "icon": "🏗️"}
        ]
    },
}


def promote():
    for slug, hub in PROMOTIONS.items():
        config_path = os.path.join(CONFIGS_DIR, f'{slug}.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        changed = False
        # Update parent fields
        if data.get('parent_slug') != '':
            data['parent_slug'] = hub['parent_slug']
            data['parent_name'] = hub['parent_name']
            changed = True

        # Add hub fields if missing
        for field in ['intro_answer', 'hub_city_links', 'service_types', 'city_compare_rows']:
            if field not in data:
                data[field] = hub[field]
                changed = True

        if changed:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'✅ Promoted: {slug}.json')
        else:
            print(f'✓  Already done: {slug}.json')

        # Rebuild page
        result = subprocess.run(
            ['python3', BUILD_SCRIPT, config_path],
            capture_output=True, text=True
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f'   ⚠️  {result.stderr.strip()}')

    print(f'\n✅ Done — {len(PROMOTIONS)} hubs promoted and rebuilt.')


if __name__ == '__main__':
    promote()
