#!/usr/bin/env python3
"""
Phase 1 — Build v2 category (hub) pages for 5 core AC services.
Run: python3 build_category_v2.py
Phase 2 will add AC keyword pages; Phase 3 adds general home services.
"""
import os
from pathlib import Path

BASE = Path("/Users/khamis/Documents/Active Projects/Claude/Rafeeg SEO/html_v2")

# ── DATA ────────────────────────────────────────────────────────────────────

SERVICES = [

  # ── 1. تركيب مكيفات ──────────────────────────────────────────────────────
  {
    "slug": "تركيب-مكيفات",
    "title": "تركيب مكيفات في الإمارات | رفيق — تركيب احترافي بضمان",
    "meta_desc": "احجز تركيب مكيفات في أبوظبي، دبي، الشارقة وعجمان مع رفيق. تركيب سبليت وشباك ومركزي، فنيون معتمدون، ضمان 12 شهر، أسعار تبدأ من 200 درهم.",
    "h1": "تركيب مكيفات في الإمارات",
    "lead": "فنيون معتمدون لتركيب جميع أنواع المكيفات — سبليت، شباك، ومركزي. ضمان كامل، أسعار شفافة، نصل إليك في نفس اليوم.",
    "hero_bullets": ["فنيون معتمدون في أبوظبي ودبي والشارقة وعجمان", "ضمان 12 شهر على كل تركيب", "أسعار شفافة تبدأ من 200 درهم", "خدمة نفس اليوم متاحة"],
    "trust": [("4,500+", "فني مرخّص نشط"), ("200 د.إ", "تبدأ من — سبليت"), ("12 شهر", "ضمان على التركيب"), ("نفس اليوم", "حجز فوري متاح")],
    "city_cards": [
      {"city": "دبي", "emoji": "🌆", "areas": "مارينا • النخلة • داونتاون", "desc": "تركيب سبليت وشباك في جميع مناطق دبي. فنيون بتغطية كاملة وحجز فوري.", "price": "من 320 درهم", "slug": "تركيب-مكيفات-دبي"},
      {"city": "أبوظبي", "emoji": "🏛️", "areas": "الريم • مصفح • الخالدية", "desc": "خبرة واسعة في المباني السكنية والتجارية. أعلى معايير الجودة.", "price": "من 350 درهم", "slug": "تركيب-مكيفات-أبوظبي"},
      {"city": "الشارقة", "emoji": "🏙️", "areas": "التعاون • النهدة • الخان", "desc": "تركيب سبليت وشباك في المناطق السكنية والصناعية. أسعار تنافسية.", "price": "من 280 درهم", "slug": "تركيب-مكيفات-الشارقة"},
      {"city": "عجمان", "emoji": "🏡", "areas": "النعيمية • الراشدية • الكورنيش", "desc": "أفضل أسعار تركيب المكيفات في الإمارات الشمالية.", "price": "من 250 درهم", "slug": "تركيب-مكيفات-عجمان"},
    ],
    "sub_services": [
      {"icon": "🛠️", "name": "صيانة دورية", "desc": "فحص شامل لإطالة عمر المكيف", "link_text": "من 150 درهم", "slug": "صيانة-مكيفات"},
      {"icon": "🫧", "name": "تنظيف عميق", "desc": "تنظيف بالبخار يحسن التبريد 40%", "link_text": "من 100 درهم", "slug": "تنظيف-مكيفات"},
      {"icon": "⚙️", "name": "إصلاح الأعطال", "desc": "كمبروسر، موتور، وأعطال الكهرباء", "link_text": "من 180 درهم", "slug": "اصلاح-مكيفات"},
      {"icon": "❄️", "name": "شحن فريون", "desc": "فريون R32 وR410A أصلي مع فحص التسريب", "link_text": "من 200 درهم", "slug": "شحن-فريون-مكيفات"},
      {"icon": "📦", "name": "فك وتركيب (نقل)", "desc": "نقل مكيفك لمكانه الجديد بأمان تام", "link_text": "من 250 درهم", "slug": "فك-وتركيب-مكيفات"},
      {"icon": "🌡️", "name": "مكيف لا يبرد", "desc": "تشخيص ضعف التبريد وإصلاحه فوراً", "link_text": "من 160 درهم", "slug": "مكيف-لا-يبرد"},
    ],
    "pricing_rows": [
      ("سبليت 1 طن", "وحدة داخلية + خارجية", "200 د.إ"),
      ("سبليت 1.5 طن", "تركيب + فارق الطن", "250 د.إ"),
      ("سبليت 2 طن", "تركيب + فارق الطن", "300 د.إ"),
      ("سبليت 3 طن+", "تركيب + فارق الطن", "350 د.إ"),
      ("مكيف شباك", "تركيب وحدة كاملة", "150 د.إ"),
      ("أنبوب نحاسي", "إضافي لكل متر", "40 د.إ/م"),
      ("كابل كهربائي", "إضافي لكل متر", "20 د.إ/م"),
    ],
    "pricing_example": "مثال: سبليت 2 طن + 20م نحاس + 20م كابل = 300 + 800 + 400 = <strong>1,500 درهم</strong>",
    "compare_rows": [
      ("🌆 دبي", "320 درهم", "pill-green", "أقل من ساعة", "1,800+"),
      ("🏛️ أبوظبي", "350 درهم", "pill-green", "1–2 ساعة", "1,200+"),
      ("🏙️ الشارقة", "280 درهم", "pill-blue", "1–2 ساعة", "900+"),
      ("🏡 عجمان", "250 درهم", "pill-blue", "1–3 ساعات", "600+"),
    ],
    "faqs": [
      ("كم تكلفة تركيب مكيف سبليت في الإمارات؟", "تبدأ من 200 درهم في عجمان والشارقة، و320 درهم في دبي، و350 درهم في أبوظبي. يشمل التركيب الكامل لوحدتي الداخل والخارج. الأنابيب النحاسية 40 درهم/م والكابلات 20 درهم/م."),
      ("ما الفرق بين مكيف السبليت ومكيف الشباك؟", "السبليت وحدتان منفصلتان تربطهما أنابيب — أهدأ وأكفأ. الشباك وحدة واحدة في فتحة الحائط — أرخص لكن أعلى صوتاً."),
      ("كم ساعة يستغرق تركيب مكيف سبليت؟", "من ساعتين إلى 3 ساعات، يشمل الوحدة الداخلية والخارجية والأنابيب والكابلات وملء الفريون واختبار التشغيل."),
      ("هل يوجد ضمان على تركيب المكيف؟", "نعم، ضمان 12 شهراً على التركيب والتوصيلات. أي مشكلة ناتجة عن التركيب يأتي الفني مجاناً لإصلاحها."),
      ("هل يمكن تركيب مكيف في نفس اليوم؟", "نعم، خدمة نفس اليوم متاحة في دبي وأبوظبي والشارقة وعجمان إذا طلبت قبل الظهيرة."),
    ],
    "cta_h2": "احجز تركيب مكيفك الآن",
    "cta_p": "فنيون معتمدون يصلونك في نفس اليوم — أسعار شفافة — ضمان 12 شهر",
    "wa_msg": "أهلاً،+أريد+حجز+تركيب+مكيف",
    "service_name_ar": "تركيب مكيفات",
  },

  # ── 2. صيانة مكيفات ──────────────────────────────────────────────────────
  {
    "slug": "صيانة-مكيفات",
    "title": "صيانة مكيفات في الإمارات | رفيق — فحص شامل وضمان",
    "meta_desc": "صيانة مكيفات في أبوظبي، دبي، الشارقة وعجمان. فحص شامل، تنظيف وإصلاح جميع الأعطال. فنيون معتمدون، أسعار تبدأ من 150 درهم.",
    "h1": "صيانة مكيفات في الإمارات",
    "lead": "صيانة دورية وطارئة لجميع أنواع المكيفات. فحص شامل، تنظيف، وإصلاح الأعطال من فنيين معتمدين في أبوظبي، دبي، الشارقة وعجمان.",
    "hero_bullets": ["فحص شامل لجميع مكونات المكيف", "تنظيف الفلاتر والكويل وتراكمات الغبار", "اكتشاف الأعطال مبكراً قبل أن تتفاقم", "ضمان 3 أشهر على الصيانة"],
    "trust": [("4,500+", "فني مرخّص نشط"), ("150 د.إ", "تبدأ من — صيانة دورية"), ("3 أشهر", "ضمان على الصيانة"), ("نفس اليوم", "حجز فوري متاح")],
    "city_cards": [
      {"city": "دبي", "emoji": "🌆", "areas": "مارينا • ديرة • جميرا", "desc": "صيانة شاملة لجميع ماركات المكيفات في دبي. استجابة سريعة وفنيون معتمدون.", "price": "من 180 درهم", "slug": "صيانة-مكيفات-دبي"},
      {"city": "أبوظبي", "emoji": "🏛️", "areas": "الريم • مصفح • العين", "desc": "صيانة دورية وطارئة في أبوظبي والعين. غطاء كامل لجميع المناطق.", "price": "من 200 درهم", "slug": "صيانة-مكيفات-أبوظبي"},
      {"city": "الشارقة", "emoji": "🏙️", "areas": "التعاون • النهدة • القاسمية", "desc": "صيانة احترافية بأسعار اقتصادية في الشارقة. ضمان على جميع الأعمال.", "price": "من 160 درهم", "slug": "صيانة-مكيفات-الشارقة"},
      {"city": "عجمان", "emoji": "🏡", "areas": "النعيمية • الراشدية • المويهات", "desc": "أفضل صيانة مكيفات في عجمان. أسعار منافسة وخدمة سريعة.", "price": "من 150 درهم", "slug": "صيانة-مكيفات-عجمان"},
    ],
    "sub_services": [
      {"icon": "🔧", "name": "تركيب مكيفات", "desc": "تركيب سبليت وشباك جديد", "link_text": "من 200 درهم", "slug": "تركيب-مكيفات"},
      {"icon": "🫧", "name": "تنظيف عميق", "desc": "تنظيف بالبخار يحسن التبريد 40%", "link_text": "من 100 درهم", "slug": "تنظيف-مكيفات"},
      {"icon": "⚙️", "name": "إصلاح الأعطال", "desc": "كمبروسر، موتور، وأعطال الكهرباء", "link_text": "من 180 درهم", "slug": "اصلاح-مكيفات"},
      {"icon": "❄️", "name": "شحن فريون", "desc": "فريون R32 وR410A أصلي", "link_text": "من 200 درهم", "slug": "شحن-فريون-مكيفات"},
      {"icon": "🌡️", "name": "مكيف لا يبرد", "desc": "تشخيص ضعف التبريد وإصلاحه", "link_text": "من 160 درهم", "slug": "مكيف-لا-يبرد"},
      {"icon": "💨", "name": "تنظيف دكتات", "desc": "تنظيف قنوات الهواء المركزي", "link_text": "من 300 درهم", "slug": "تنظيف-دكتات-مكيفات"},
    ],
    "pricing_rows": [
      ("صيانة دورية سبليت", "فحص + تنظيف فلاتر", "150 د.إ"),
      ("صيانة شاملة سبليت", "فحص + تنظيف كامل + تقرير", "250 د.إ"),
      ("صيانة مكيف شباك", "فحص + تنظيف", "120 د.إ"),
      ("صيانة مكيف مركزي", "فحص شامل لكل وحدة", "350 د.إ"),
      ("كشف عطل", "تشخيص وتقرير مفصّل", "80 د.إ"),
      ("طوارئ خارج الدوام", "رسوم إضافية", "+100 د.إ"),
    ],
    "pricing_example": "مثال: صيانة شاملة لشقة بها 3 مكيفات سبليت = 3 × 250 = <strong>750 درهم</strong>",
    "compare_rows": [
      ("🌆 دبي", "180 درهم", "pill-green", "أقل من ساعة", "1,800+"),
      ("🏛️ أبوظبي", "200 درهم", "pill-green", "1–2 ساعة", "1,200+"),
      ("🏙️ الشارقة", "160 درهم", "pill-blue", "1–2 ساعة", "900+"),
      ("🏡 عجمان", "150 درهم", "pill-blue", "1–3 ساعات", "600+"),
    ],
    "faqs": [
      ("كم مرة يجب صيانة المكيف في السنة؟", "يُنصح بصيانة دورية مرة واحدة على الأقل كل 6 أشهر في الإمارات بسبب الغبار والرطوبة. للمكيفات المستخدمة باستمرار، صيانة كل 3 أشهر مثالية."),
      ("ما الذي يشمله فحص الصيانة الشامل؟", "يشمل: فحص الضغط والفريون، تنظيف الفلاتر والكويل والمروحة، فحص الكهرباء والتوصيلات، قياس درجة حرارة الهواء، وتقرير مفصّل بحالة المكيف."),
      ("هل الصيانة الدورية توفر الكهرباء فعلاً؟", "نعم، المكيف غير المنظّف يستهلك حتى 40% طاقة إضافية. الصيانة الدورية تحافظ على الكفاءة وتوفر فاتورة الكهرباء."),
      ("هل يمكن عمل صيانة لجميع الماركات؟", "نعم، فنيو رفيق مدرّبون على جميع الماركات: Daikin، Samsung، LG، Gree، Midea، Carrier وغيرها."),
      ("ماذا يحدث إذا اكتشف الفني عطلاً أثناء الصيانة؟", "يُقدّم الفني تقريراً بالعطل وتكلفة الإصلاح قبل البدء. لك حق الموافقة أو الرفض. لا توجد رسوم إضافية مخفية."),
    ],
    "cta_h2": "احجز صيانة مكيفك الآن",
    "cta_p": "فنيون معتمدون يصلونك في نفس اليوم — فحص شامل — ضمان 3 أشهر",
    "wa_msg": "أهلاً،+أريد+حجز+صيانة+مكيف",
    "service_name_ar": "صيانة مكيفات",
  },

  # ── 3. تنظيف مكيفات ──────────────────────────────────────────────────────
  {
    "slug": "تنظيف-مكيفات",
    "title": "تنظيف مكيفات في الإمارات | رفيق — تنظيف بالبخار بضمان",
    "meta_desc": "تنظيف مكيفات في أبوظبي، دبي، الشارقة وعجمان. تنظيف بالبخار والكيماويات، يحسّن التبريد ويوفر الكهرباء. أسعار تبدأ من 100 درهم.",
    "h1": "تنظيف مكيفات في الإمارات",
    "lead": "تنظيف احترافي بالبخار والمواد المتخصصة لجميع أنواع المكيفات. يحسّن التبريد حتى 40% ويوفر فاتورة الكهرباء.",
    "hero_bullets": ["تنظيف بالبخار يزيل 99% من الجراثيم والعفن", "يحسّن كفاءة التبريد حتى 40%", "يوفر من 10–25% في فاتورة الكهرباء", "ضمان على جودة التنظيف"],
    "trust": [("4,500+", "فني مرخّص نشط"), ("100 د.إ", "تبدأ من — تنظيف سبليت"), ("40%", "تحسّن كفاءة التبريد"), ("نفس اليوم", "حجز فوري متاح")],
    "city_cards": [
      {"city": "دبي", "emoji": "🌆", "areas": "مارينا • ديرة • سبيا", "desc": "تنظيف مكيفات سبليت وشباك ومركزي في جميع مناطق دبي. فنيون متخصصون.", "price": "من 120 درهم", "slug": "تنظيف-مكيفات-دبي"},
      {"city": "أبوظبي", "emoji": "🏛️", "areas": "الريم • مصفح • شخبوط", "desc": "تنظيف احترافي بالبخار في أبوظبي. نصل لجميع المناطق.", "price": "من 130 درهم", "slug": "تنظيف-مكيفات-أبوظبي"},
      {"city": "الشارقة", "emoji": "🏙️", "areas": "التعاون • النهدة • الخان", "desc": "أسعار تنافسية لتنظيف المكيفات في الشارقة مع ضمان الجودة.", "price": "من 110 درهم", "slug": "تنظيف-مكيفات-الشارقة"},
      {"city": "عجمان", "emoji": "🏡", "areas": "النعيمية • الراشدية • العامرة", "desc": "تنظيف سريع واحترافي في عجمان بأقل الأسعار.", "price": "من 100 درهم", "slug": "تنظيف-مكيفات-عجمان"},
    ],
    "sub_services": [
      {"icon": "🔧", "name": "تركيب مكيفات", "desc": "تركيب سبليت وشباك جديد", "link_text": "من 200 درهم", "slug": "تركيب-مكيفات"},
      {"icon": "🛠️", "name": "صيانة دورية", "desc": "فحص شامل لإطالة عمر المكيف", "link_text": "من 150 درهم", "slug": "صيانة-مكيفات"},
      {"icon": "⚙️", "name": "إصلاح الأعطال", "desc": "كمبروسر، موتور، وأعطال الكهرباء", "link_text": "من 180 درهم", "slug": "اصلاح-مكيفات"},
      {"icon": "❄️", "name": "شحن فريون", "desc": "فريون أصلي مع فحص التسريب", "link_text": "من 200 درهم", "slug": "شحن-فريون-مكيفات"},
      {"icon": "💨", "name": "تنظيف دكتات", "desc": "تنظيف قنوات الهواء المركزي", "link_text": "من 300 درهم", "slug": "تنظيف-دكتات-مكيفات"},
      {"icon": "🌡️", "name": "مكيف لا يبرد", "desc": "تشخيص ضعف التبريد وإصلاحه", "link_text": "من 160 درهم", "slug": "مكيف-لا-يبرد"},
    ],
    "pricing_rows": [
      ("سبليت — وحدة داخلية", "تنظيف بالبخار + مواد", "100 د.إ"),
      ("سبليت — وحدة خارجية", "تنظيف الكويل والمروحة", "80 د.إ"),
      ("تنظيف سبليت كامل", "داخلية + خارجية", "160 د.إ"),
      ("مكيف شباك", "تنظيف كامل", "90 د.إ"),
      ("مكيف مركزي/وحدة", "تنظيف + مواد", "200 د.إ"),
      ("تعقيم وتطهير", "مواد مضادة للبكتيريا", "+40 د.إ"),
    ],
    "pricing_example": "مثال: تنظيف شقة بها 3 مكيفات سبليت (داخلية فقط) = 3 × 100 = <strong>300 درهم</strong>",
    "compare_rows": [
      ("🌆 دبي", "120 درهم", "pill-green", "أقل من ساعة", "1,800+"),
      ("🏛️ أبوظبي", "130 درهم", "pill-green", "1–2 ساعة", "1,200+"),
      ("🏙️ الشارقة", "110 درهم", "pill-blue", "1–2 ساعة", "900+"),
      ("🏡 عجمان", "100 درهم", "pill-blue", "1–3 ساعات", "600+"),
    ],
    "faqs": [
      ("كم مرة يجب تنظيف المكيف في الإمارات؟", "كل 3 أشهر في الصيف وكل 6 أشهر في الشتاء بسبب الغبار والرطوبة العالية. المكيفات في مناطق غبارية تحتاج تنظيفاً أكثر."),
      ("ما الفرق بين تنظيف الفلتر وتنظيف الكويل؟", "تنظيف الفلتر سهل ويمكنك عمله بنفسك كل أسبوعين. تنظيف الكويل (المبخّر) يحتاج معدات متخصصة وكيماويات آمنة — يجب أن يقوم به فني."),
      ("هل التنظيف بالبخار آمن للمكيف؟", "نعم، البخار يزيل الغبار والعفن والبكتيريا دون إتلاف الأجزاء الإلكترونية. فنيو رفيق مدرّبون على استخدامه بأمان."),
      ("كم يستغرق تنظيف المكيف؟", "تنظيف سبليت واحد يستغرق 45 دقيقة إلى ساعة. وحدة مركزية من 1.5 إلى 2 ساعة."),
      ("هل يجب إفراغ الغرفة أثناء التنظيف؟", "لا حاجة لإفراغها، لكن يُنصح بتغطية الأثاث القريب. الفني يحمي المنطقة المحيطة قبل البدء."),
    ],
    "cta_h2": "احجز تنظيف مكيفك الآن",
    "cta_p": "تنظيف احترافي بالبخار — أسعار شفافة — يحسّن التبريد فوراً",
    "wa_msg": "أهلاً،+أريد+حجز+تنظيف+مكيف",
    "service_name_ar": "تنظيف مكيفات",
  },

  # ── 4. اصلاح مكيفات ──────────────────────────────────────────────────────
  {
    "slug": "اصلاح-مكيفات",
    "title": "إصلاح مكيفات في الإمارات | رفيق — تصليح سريع بضمان",
    "meta_desc": "إصلاح مكيفات في أبوظبي، دبي، الشارقة وعجمان. تصليح كمبروسر وموتور وأعطال التبريد. فنيون معتمدون، أسعار تبدأ من 180 درهم.",
    "h1": "إصلاح مكيفات في الإمارات",
    "lead": "تشخيص دقيق وإصلاح سريع لجميع أعطال المكيفات — كمبروسر، موتور، لوحة تحكم، تسريب فريون. فنيون معتمدون في 4 إمارات.",
    "hero_bullets": ["تشخيص العطل خلال 30 دقيقة", "إصلاح كمبروسر وموتور ولوحة تحكم", "قطع غيار أصلية مع ضمان", "الدفع بعد الإصلاح فقط"],
    "trust": [("4,500+", "فني مرخّص نشط"), ("180 د.إ", "تبدأ من — إصلاح"), ("ضمان", "على قطع الغيار"), ("30 دقيقة", "تشخيص العطل")],
    "city_cards": [
      {"city": "دبي", "emoji": "🌆", "areas": "مارينا • ديرة • عود ميثاء", "desc": "إصلاح جميع أعطال المكيفات في دبي. فنيون متخصصون بجميع الماركات.", "price": "من 220 درهم", "slug": "اصلاح-مكيفات-دبي"},
      {"city": "أبوظبي", "emoji": "🏛️", "areas": "الريم • مصفح • البطين", "desc": "تصليح سريع ومضمون لمكيفات أبوظبي. قطع غيار أصلية.", "price": "من 240 درهم", "slug": "اصلاح-مكيفات-أبوظبي"},
      {"city": "الشارقة", "emoji": "🏙️", "areas": "التعاون • النهدة • المجاز", "desc": "إصلاح احترافي بالشارقة. ضمان على جميع أعمال الإصلاح.", "price": "من 200 درهم", "slug": "اصلاح-مكيفات-الشارقة"},
      {"city": "عجمان", "emoji": "🏡", "areas": "النعيمية • الراشدية • الحميدية", "desc": "تصليح سريع وأسعار تنافسية في عجمان.", "price": "من 180 درهم", "slug": "اصلاح-مكيفات-عجمان"},
    ],
    "sub_services": [
      {"icon": "🔧", "name": "تركيب مكيفات", "desc": "تركيب سبليت وشباك جديد", "link_text": "من 200 درهم", "slug": "تركيب-مكيفات"},
      {"icon": "🛠️", "name": "صيانة دورية", "desc": "فحص شامل لمنع الأعطال", "link_text": "من 150 درهم", "slug": "صيانة-مكيفات"},
      {"icon": "❄️", "name": "شحن فريون", "desc": "فريون أصلي مع فحص التسريب", "link_text": "من 200 درهم", "slug": "شحن-فريون-مكيفات"},
      {"icon": "🔩", "name": "تصليح سبليت", "desc": "متخصصون في مكيفات السبليت", "link_text": "من 180 درهم", "slug": "تصليح-مكيفات-سبلت"},
      {"icon": "🌡️", "name": "مكيف لا يبرد", "desc": "تشخيص ضعف التبريد وإصلاحه", "link_text": "من 160 درهم", "slug": "مكيف-لا-يبرد"},
      {"icon": "📦", "name": "فك وتركيب (نقل)", "desc": "نقل مكيفك بأمان تام", "link_text": "من 250 درهم", "slug": "فك-وتركيب-مكيفات"},
    ],
    "pricing_rows": [
      ("كشف وتشخيص العطل", "تقرير مفصّل", "80 د.إ"),
      ("إصلاح تسريب فريون", "سد التسريب + شحن", "300 د.إ"),
      ("استبدال موتور مروحة", "قطعة + تركيب", "من 350 د.إ"),
      ("إصلاح لوحة التحكم", "تشخيص + برمجة أو استبدال", "من 250 د.إ"),
      ("استبدال كمبروسر", "قطعة أصلية + تركيب", "من 800 د.إ"),
      ("إصلاح تصريف المياه", "تنظيف + إصلاح", "150 د.إ"),
    ],
    "pricing_example": "مثال: إصلاح موتور المروحة الداخلية (قطعة + تركيب + ضمان 6 أشهر) = <strong>من 350 درهم</strong>",
    "compare_rows": [
      ("🌆 دبي", "220 درهم", "pill-green", "أقل من ساعة", "1,800+"),
      ("🏛️ أبوظبي", "240 درهم", "pill-green", "1–2 ساعة", "1,200+"),
      ("🏙️ الشارقة", "200 درهم", "pill-blue", "1–2 ساعة", "900+"),
      ("🏡 عجمان", "180 درهم", "pill-blue", "1–3 ساعات", "600+"),
    ],
    "faqs": [
      ("كيف أعرف إذا كان المكيف يحتاج إصلاحاً؟", "علامات تحتاج إصلاح: المكيف لا يبرد، يصدر أصواتاً غريبة، يسرّب ماءً كثيراً، يرفع رسائل خطأ، أو يتوقف تلقائياً بعد دقائق."),
      ("هل يجدر إصلاح مكيف قديم أم شراء جديد؟", "إذا كان عمر المكيف أقل من 8 سنوات والإصلاح أقل من 50% من سعر جديد، الإصلاح أفضل. إذا تجاوز العمر 10 سنوات أو الكمبروسر تالف، الاستبدال أوفر."),
      ("هل توجد قطع غيار أصلية متاحة؟", "نعم، رفيق يوفر قطع أصلية لجميع الماركات الرئيسية مع ضمان المصنع. يمكن توفير القطعة خلال 24 ساعة في حالات الطلب الخاص."),
      ("هل يشمل الكشف تشخيص جميع الأعطال؟", "نعم، الفحص يشمل جميع أجزاء المكيف. يحصل العميل على تقرير كامل بجميع الأعطال وتكلفة إصلاح كل منها قبل البدء."),
      ("ما ضمان الإصلاح؟", "ضمان 3 أشهر على أعمال الإصلاح، و6–12 شهر على قطع الغيار المستبدَلة حسب نوع القطعة والماركة."),
    ],
    "cta_h2": "احجز إصلاح مكيفك الآن",
    "cta_p": "تشخيص خلال 30 دقيقة — قطع أصلية — الدفع بعد الإصلاح فقط",
    "wa_msg": "أهلاً،+أريد+حجز+إصلاح+مكيف",
    "service_name_ar": "إصلاح مكيفات",
  },

  # ── 5. شحن فريون مكيفات ──────────────────────────────────────────────────
  {
    "slug": "شحن-فريون-مكيفات",
    "title": "شحن فريون مكيفات في الإمارات | رفيق — فريون أصلي بضمان",
    "meta_desc": "شحن فريون مكيفات في أبوظبي، دبي، الشارقة وعجمان. فريون R32 وR410A أصلي، فحص تسريب مجاني، أسعار تبدأ من 200 درهم.",
    "h1": "شحن فريون مكيفات في الإمارات",
    "lead": "شحن فريون أصلي معتمد لجميع أنواع المكيفات مع فحص تسريب مجاني. استعيد قوة التبريد الكاملة مع فنيين معتمدين.",
    "hero_bullets": ["فريون R32 وR410A وR22 أصلي معتمد", "فحص تسريب مجاني مع كل شحن", "تبريد كامل خلال ساعة من الشحن", "ضمان على عمل الشحن"],
    "trust": [("4,500+", "فني مرخّص نشط"), ("200 د.إ", "تبدأ من — شحن"), ("مجاني", "فحص التسريب"), ("نفس اليوم", "حجز فوري متاح")],
    "city_cards": [
      {"city": "دبي", "emoji": "🌆", "areas": "مارينا • ديرة • الكرامة", "desc": "شحن فريون في دبي بفنيين معتمدين. نصل لجميع المناطق خلال ساعة.", "price": "من 220 درهم", "slug": "شحن-فريون-مكيفات-دبي"},
      {"city": "أبوظبي", "emoji": "🏛️", "areas": "الريم • مصفح • الوثبة", "desc": "شحن فريون في أبوظبي مع ضمان الجودة والفريون الأصلي.", "price": "من 230 درهم", "slug": "شحن-فريون-مكيفات-أبوظبي"},
      {"city": "الشارقة", "emoji": "🏙️", "areas": "التعاون • النهدة • الصجعة", "desc": "شحن فريون بأسعار تنافسية في الشارقة. فريون معتمد وأصلي.", "price": "من 210 درهم", "slug": "شحن-فريون-مكيفات-الشارقة"},
      {"city": "عجمان", "emoji": "🏡", "areas": "النعيمية • الراشدية • الزورا", "desc": "أرخص شحن فريون في الإمارات الشمالية مع ضمان الجودة.", "price": "من 200 درهم", "slug": "شحن-فريون-مكيفات-عجمان"},
    ],
    "sub_services": [
      {"icon": "🔧", "name": "تركيب مكيفات", "desc": "تركيب سبليت وشباك جديد", "link_text": "من 200 درهم", "slug": "تركيب-مكيفات"},
      {"icon": "🛠️", "name": "صيانة دورية", "desc": "فحص شامل يشمل الفريون", "link_text": "من 150 درهم", "slug": "صيانة-مكيفات"},
      {"icon": "⚙️", "name": "إصلاح الأعطال", "desc": "إصلاح تسريب الفريون", "link_text": "من 180 درهم", "slug": "اصلاح-مكيفات"},
      {"icon": "🌡️", "name": "مكيف لا يبرد", "desc": "تشخيص نقص الفريون وإصلاحه", "link_text": "من 160 درهم", "slug": "مكيف-لا-يبرد"},
      {"icon": "🫧", "name": "تنظيف مكيفات", "desc": "تنظيف يحسّن كفاءة الفريون", "link_text": "من 100 درهم", "slug": "تنظيف-مكيفات"},
      {"icon": "💨", "name": "تنظيف دكتات", "desc": "تنظيف قنوات الهواء المركزي", "link_text": "من 300 درهم", "slug": "تنظيف-دكتات-مكيفات"},
    ],
    "pricing_rows": [
      ("كشف وقياس ضغط الفريون", "تشخيص + تقرير", "80 د.إ"),
      ("شحن R410A — 1 طن", "للمكيفات الحديثة", "200 د.إ"),
      ("شحن R410A — 1.5 طن", "للمكيفات الحديثة", "250 د.إ"),
      ("شحن R410A — 2 طن+", "للمكيفات الحديثة", "300 د.إ"),
      ("شحن R32 (أخضر)", "جيل جديد موفّر للطاقة", "220 د.إ"),
      ("سد تسريب فريون", "إصلاح + إعادة شحن", "من 350 د.إ"),
    ],
    "pricing_example": "مثال: شحن فريون R410A لمكيف 2 طن + فحص تسريب = <strong>300 + مجاني = 300 درهم</strong>",
    "compare_rows": [
      ("🌆 دبي", "220 درهم", "pill-green", "أقل من ساعة", "1,800+"),
      ("🏛️ أبوظبي", "230 درهم", "pill-green", "1–2 ساعة", "1,200+"),
      ("🏙️ الشارقة", "210 درهم", "pill-blue", "1–2 ساعة", "900+"),
      ("🏡 عجمان", "200 درهم", "pill-blue", "1–3 ساعات", "600+"),
    ],
    "faqs": [
      ("كيف أعرف أن مكيفي يحتاج شحن فريون؟", "علامات نقص الفريون: التبريد ضعيف رغم تشغيل المكيف، الوحدة الداخلية تتجمد، تصدر صوت فقاعات، أو الكمبروسر يعمل باستمرار بدون إيقاف."),
      ("ما الفرق بين R22 وR410A وR32؟", "R22 قديم وممنوع في المباني الجديدة. R410A الأكثر شيوعاً في الإمارات حالياً. R32 أحدث وأقل ضرراً للبيئة وأكثر كفاءة — تستخدمه المكيفات الجديدة."),
      ("هل يجب إصلاح التسريب قبل الشحن؟", "نعم، شحن الفريون بدون إصلاح التسريب مضيعة للمال. الفني يكشف التسريب أولاً، يصلحه، ثم يشحن. لهذا نقدم فحص التسريب مجاناً."),
      ("كم يدوم شحن الفريون؟", "الفريون لا يُستهلك في الظروف الطبيعية — يدوم مدى الحياة. إذا احتاج المكيف شحناً متكرراً، هذا يعني وجود تسريب يجب إصلاحه."),
      ("هل الفريون المستخدم أصلي؟", "نعم، رفيق يستخدم فريوناً أصلياً معتمداً من موردين مرخّصين. الفريون المقلّد يُتلف الكمبروسر ويبطل ضمان المكيف."),
    ],
    "cta_h2": "احجز شحن فريون الآن",
    "cta_p": "فريون أصلي معتمد — فحص تسريب مجاني — يصلك الفني اليوم",
    "wa_msg": "أهلاً،+أريد+حجز+شحن+فريون+مكيف",
    "service_name_ar": "شحن فريون مكيفات",
  },

]

# ── HTML BUILDER ─────────────────────────────────────────────────────────────

def build_page(d):
    slug = d["slug"]
    url  = f"https://hub.rafeeg.ae/{slug}/"

    # city cards HTML
    city_cards_html = ""
    for c in d["city_cards"]:
        city_cards_html += f"""
        <a href="https://hub.rafeeg.ae/{c['slug']}/" class="cat-card">
          <div class="cat-card-head">
            <div class="cat-card-icon">{c['emoji']}</div>
            <div>
              <div class="cat-card-name">{d['service_name_ar']} {c['city']}</div>
              <div class="cat-card-city">{c['areas']}</div>
            </div>
          </div>
          <p class="cat-card-desc">{c['desc']}</p>
          <div class="cat-card-footer">
            <span class="cat-card-price">{c['price']}</span>
            <span class="cat-card-cta">عرض التفاصيل</span>
          </div>
        </a>"""

    # sub-services HTML
    sub_html = ""
    for s in d["sub_services"]:
        sub_html += f"""
        <a href="https://hub.rafeeg.ae/{s['slug']}/" class="sub-card">
          <div class="sub-card-icon">{s['icon']}</div>
          <div class="sub-card-name">{s['name']}</div>
          <div class="sub-card-desc">{s['desc']}</div>
          <span class="sub-card-link">{s['link_text']}</span>
        </a>"""

    # pricing rows
    pricing_html = ""
    for row in d["pricing_rows"]:
        pricing_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n"

    # compare rows
    compare_html = ""
    for r in d["compare_rows"]:
        compare_html += f"""<tr>
          <td>{r[0]}</td><td>{r[1]}</td>
          <td><span class="pill {r[2]}">{r[3]}</span></td>
          <td>{r[4]} فني</td><td>12 شهر</td>
        </tr>\n"""

    # faq HTML
    faq_html = ""
    for q, a in d["faqs"]:
        faq_html += f"""
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">{q}<span class="faq-icon">+</span></button>
          <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
        </div>"""

    # hero bullets
    bullets_html = "".join(f"<li>{b}</li>" for b in d["hero_bullets"])

    # trust strip
    trust_html = "".join(
        f'<div class="trust-item"><div class="trust-num">{n}</div><div class="trust-label">{l}</div></div>'
        for n, l in d["trust"]
    )

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<title>{d['title']}</title>
<meta name="description" content="{d['meta_desc']}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:title" content="{d['title']}">
<meta property="og:description" content="{d['meta_desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="ar_AE">
<meta property="og:image" content="https://hub.rafeeg.ae/{slug}/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{d['title']}">
<meta name="twitter:image" content="https://hub.rafeeg.ae/{slug}/hero.jpg">
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@graph": [
    {{"@type":"LocalBusiness","@id":"https://ar.rafeeg.ae/#organization","name":"رفيق","url":"https://ar.rafeeg.ae","logo":"https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png","telephone":"+971600500200","aggregateRating":{{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"135000","bestRating":"5"}}}},
    {{"@type":"Service","name":"{d['h1']}","provider":{{"@id":"https://ar.rafeeg.ae/#organization"}},"areaServed":["أبوظبي","دبي","الشارقة","عجمان"]}},
    {{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"رفيق هاب","item":"https://hub.rafeeg.ae/"}},{{"@type":"ListItem","position":2,"name":"{d['service_name_ar']}","item":"{url}"}}]}},
    {{"@type":"FAQPage","mainEntity":[{",".join(
      '{{"@type":"Question","name":"' + q + '","acceptedAnswer":{{"@type":"Answer","text":"' + a + '"}}}}'
      for q, a in d["faqs"]
    )}]}}
  ]
}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=optional" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=optional"></noscript>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--green:#189F18;--green-dark:#117A11;--dark:#030712;--text:#1a2332;--muted:#6b7280;--border:#e5e7eb;--white:#ffffff;--grey-bg:#f1f5f9;--hero-bg:#eef9ee;--radius:16px;--radius-sm:10px;--shadow:0 2px 16px rgba(0,0,0,.08)}}
html{{scroll-behavior:smooth}}
body{{font-family:'Cairo',system-ui,sans-serif;font-size:16px;color:var(--text);background:var(--white);line-height:1.6}}
a{{text-decoration:none;color:inherit}}
img{{max-width:100%;height:auto;display:block}}
.container{{max-width:1140px;margin:0 auto;padding:0 20px}}
.site-header{{background:var(--white);position:sticky;top:0;z-index:200;border-bottom:1px solid var(--border);box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.nav-inner{{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}}
.logo img{{height:42px;width:auto}}
.nav-list{{display:flex;align-items:center;gap:6px;list-style:none;font-size:15px;font-weight:600}}
.nav-list a{{color:var(--text);transition:color .2s}}
.nav-list a:hover{{color:var(--green)}}
.has-dropdown{{position:relative}}
.nav-link-drop{{display:flex;align-items:center;gap:5px;padding:8px 14px;border-radius:8px;cursor:pointer;color:var(--text);font-weight:600;font-size:15px;transition:background .15s,color .2s;white-space:nowrap}}
.nav-link-drop:hover{{background:var(--grey-bg);color:var(--green)}}
.drop-arrow{{font-size:9px;transition:transform .2s;display:inline-block;margin-top:1px}}
.has-dropdown:hover .drop-arrow{{transform:rotate(180deg)}}
.dropdown{{display:none;position:absolute;top:calc(100% + 6px);right:0;background:var(--white);border:1px solid var(--border);border-radius:12px;min-width:185px;padding:6px 0;box-shadow:0 8px 24px rgba(0,0,0,.12);z-index:300;list-style:none}}
.has-dropdown:hover .dropdown{{display:block}}
.dropdown li a{{display:block;padding:10px 18px;color:var(--text);font-size:14px;font-weight:500;transition:background .12s,color .12s}}
.dropdown li a:hover{{background:var(--grey-bg);color:var(--green)}}
.nav-cta{{background:var(--green);color:#fff;padding:9px 20px;border-radius:10px;font-weight:700;font-size:14px;transition:background .2s;white-space:nowrap}}
.nav-cta:hover{{background:var(--green-dark)}}
.hamburger{{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:4px;background:none;border:none}}
.hamburger span{{width:24px;height:2px;background:var(--dark);border-radius:2px}}
.cat-hero{{background:var(--hero-bg);border-bottom:1px solid var(--border);overflow:hidden}}
.hero-inner{{display:grid;grid-template-columns:1fr 420px;align-items:center;gap:0;min-height:460px}}
.hero-text{{padding:52px 48px 52px 20px}}
.breadcrumb{{font-size:13px;color:var(--muted);margin-bottom:18px}}
.breadcrumb a{{color:var(--green)}}
.breadcrumb span{{margin:0 6px}}
.hero-text h1{{font-size:clamp(28px,3.5vw,42px);font-weight:900;color:var(--dark);line-height:1.2;margin-bottom:14px}}
.hero-text .lead{{font-size:17px;color:var(--muted);margin-bottom:24px;line-height:1.65}}
.hero-bullets{{list-style:none;margin-bottom:28px;display:flex;flex-direction:column;gap:10px}}
.hero-bullets li{{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:var(--text)}}
.hero-bullets li::before{{content:"✓";background:var(--green);color:#fff;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0}}
.hero-actions{{display:flex;gap:12px;flex-wrap:wrap}}
.btn-primary{{background:var(--green);color:#fff;padding:13px 24px;border-radius:12px;font-weight:700;font-size:15px;transition:background .2s;display:inline-flex;align-items:center;gap:8px}}
.btn-primary:hover{{background:var(--green-dark)}}
.btn-secondary{{background:var(--white);color:var(--text);padding:13px 24px;border-radius:12px;font-weight:700;font-size:15px;border:1.5px solid var(--border);transition:border-color .2s;display:inline-flex;align-items:center;gap:8px}}
.btn-secondary:hover{{border-color:var(--green);color:var(--green)}}
.hero-image{{position:relative;height:460px;overflow:hidden}}
.hero-image img{{width:100%;height:100%;object-fit:cover;object-position:center top}}
.hero-image-badge{{position:absolute;bottom:20px;right:20px;background:rgba(0,0,0,.65);backdrop-filter:blur(6px);color:#fff;border-radius:10px;padding:10px 14px;font-size:12px;font-weight:700;line-height:1.4}}
.hero-image-badge span{{color:#4ade80}}
.trust-strip{{background:var(--dark);padding:28px 0}}
.trust-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;text-align:center}}
.trust-item{{padding:0 20px;border-left:1px solid rgba(255,255,255,.1)}}
.trust-item:last-child{{border-left:none}}
.trust-num{{font-size:28px;font-weight:900;color:#4ade80;line-height:1;margin-bottom:5px}}
.trust-label{{font-size:12px;color:#9ca3af;font-weight:600}}
.section-label{{font-size:13px;font-weight:700;color:var(--green);letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px}}
.section-label::before{{content:"• ";color:var(--green)}}
.section-title{{font-size:clamp(22px,3vw,32px);font-weight:900;color:var(--dark);margin-bottom:8px}}
.section-sub{{font-size:15px;color:var(--muted);margin-bottom:36px}}
.cards-section{{padding:64px 0;background:var(--white)}}
.cards-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}}
.cat-card{{background:var(--white);border:1.5px solid var(--border);border-radius:var(--radius);padding:28px 24px;transition:border-color .2s,box-shadow .2s,transform .2s;display:flex;flex-direction:column;gap:10px;position:relative;overflow:hidden}}
.cat-card::before{{content:"";position:absolute;top:0;right:0;width:4px;height:100%;background:var(--border);transition:background .2s}}
.cat-card:hover{{border-color:var(--green);box-shadow:0 8px 32px rgba(24,159,24,.12);transform:translateY(-3px)}}
.cat-card:hover::before{{background:var(--green)}}
.cat-card-head{{display:flex;align-items:center;gap:14px}}
.cat-card-icon{{font-size:36px;flex-shrink:0}}
.cat-card-name{{font-size:19px;font-weight:800;color:var(--dark)}}
.cat-card-city{{font-size:12px;color:var(--muted);font-weight:600}}
.cat-card-desc{{font-size:13px;color:var(--muted);line-height:1.6;flex:1}}
.cat-card-footer{{display:flex;align-items:center;justify-content:space-between;margin-top:4px;padding-top:14px;border-top:1px solid var(--border)}}
.cat-card-price{{font-size:13px;font-weight:700;color:var(--green);background:var(--hero-bg);padding:5px 12px;border-radius:20px}}
.cat-card-cta{{color:var(--green);font-weight:700;font-size:13px;display:flex;align-items:center;gap:4px}}
.cat-card-cta::before{{content:"←"}}
.sub-section{{padding:64px 0;background:var(--grey-bg)}}
.sub-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}}
.sub-card{{background:var(--white);border:1.5px solid var(--border);border-radius:var(--radius-sm);padding:18px 16px;display:flex;flex-direction:column;gap:8px;transition:border-color .2s,box-shadow .2s}}
.sub-card:hover{{border-color:var(--green);box-shadow:0 4px 16px rgba(24,159,24,.1)}}
.sub-card-icon{{font-size:28px}}
.sub-card-name{{font-size:14px;font-weight:700;color:var(--dark);line-height:1.3}}
.sub-card-desc{{font-size:12px;color:var(--muted);line-height:1.5;flex:1}}
.sub-card-link{{font-size:12px;font-weight:700;color:var(--green);display:flex;align-items:center;gap:3px}}
.sub-card-link::before{{content:"←"}}
.how-section{{padding:64px 0;background:var(--white)}}
.steps-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;position:relative;margin-top:16px}}
.steps-grid::before{{content:"";position:absolute;top:32px;right:12.5%;left:12.5%;height:2px;background:linear-gradient(to left,var(--green),#86efac);z-index:0}}
.step{{text-align:center;padding:0 16px;position:relative;z-index:1}}
.step-num{{width:64px;height:64px;border-radius:50%;background:var(--green);color:#fff;font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;border:4px solid var(--white);box-shadow:0 0 0 2px var(--green)}}
.step-title{{font-size:15px;font-weight:800;color:var(--dark);margin-bottom:6px}}
.step-desc{{font-size:13px;color:var(--muted);line-height:1.5}}
.pricing-section{{padding:64px 0;background:var(--grey-bg)}}
.pricing-wrap{{max-width:720px;margin:0 auto}}
.pricing-table{{width:100%;border-collapse:collapse;font-size:14px;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}}
.pricing-table thead tr{{background:var(--dark)}}
.pricing-table th{{padding:14px 20px;text-align:right;font-weight:700;font-size:13px;color:#fff}}
.pricing-table th:last-child{{text-align:center}}
.pricing-table td{{padding:13px 20px;border-bottom:1px solid var(--border);font-weight:600;background:var(--white)}}
.pricing-table td:last-child{{text-align:center;color:var(--green);font-weight:800}}
.pricing-table tr:nth-child(even) td{{background:#f9fafb}}
.pricing-table tr:last-child td{{border-bottom:none}}
.pricing-example{{background:var(--hero-bg);border:1px solid #bbf7d0;border-radius:10px;padding:14px 18px;margin-top:16px;font-size:13px;color:var(--text)}}
.pricing-example strong{{color:var(--green)}}
.compare-section{{padding:64px 0;background:var(--white)}}
.compare-table{{width:100%;border-collapse:collapse;font-size:14px;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}}
.compare-table th{{background:var(--dark);color:#fff;padding:14px 18px;text-align:center;font-weight:700;font-size:13px}}
.compare-table th:first-child{{text-align:right}}
.compare-table td{{padding:13px 18px;border-bottom:1px solid var(--border);background:var(--white);text-align:center;font-weight:600}}
.compare-table td:first-child{{text-align:right;font-weight:700;color:var(--dark)}}
.compare-table tr:nth-child(even) td{{background:#f9fafb}}
.compare-table tr:last-child td{{border-bottom:none}}
.pill{{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700}}
.pill-green{{background:#dcfce7;color:#15803d}}
.pill-blue{{background:#dbeafe;color:#1d4ed8}}
.faq-section{{padding:64px 0;background:var(--grey-bg)}}
.faq-list{{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:12px}}
.faq-item{{background:var(--white);border:1.5px solid var(--border);border-radius:var(--radius-sm);overflow:hidden}}
.faq-q{{width:100%;background:none;border:none;padding:18px 20px;text-align:right;font-family:inherit;font-size:15px;font-weight:700;color:var(--dark);cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:12px;transition:color .15s}}
.faq-q:hover{{color:var(--green)}}
.faq-icon{{font-size:18px;flex-shrink:0;transition:transform .2s;color:var(--green)}}
.faq-a{{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .2s}}
.faq-a-inner{{padding:0 20px 18px;font-size:14px;color:var(--muted);line-height:1.7}}
.faq-item.open .faq-a{{max-height:300px}}
.faq-item.open .faq-icon{{transform:rotate(45deg)}}
.related-section{{padding:64px 0;background:var(--white)}}
.related-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}}
.related-card{{border:1.5px solid var(--border);border-radius:var(--radius-sm);padding:18px;text-align:center;transition:border-color .2s,transform .2s}}
.related-card:hover{{border-color:var(--green);transform:translateY(-2px)}}
.related-icon{{font-size:30px;margin-bottom:8px}}
.related-name{{font-size:14px;font-weight:700;color:var(--dark)}}
.cta-banner{{background:linear-gradient(135deg,#0a1f0a 0%,#0d3b0d 100%);padding:60px 0;text-align:center;position:relative;overflow:hidden}}
.cta-banner::before{{content:"❄️";position:absolute;font-size:200px;opacity:.04;top:-20px;left:-20px;line-height:1}}
.cta-banner h2{{font-size:clamp(22px,3vw,36px);font-weight:900;color:#fff;margin-bottom:12px}}
.cta-banner p{{color:#9ca3af;font-size:15px;margin-bottom:32px;max-width:500px;margin-left:auto;margin-right:auto}}
.cta-actions{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}}
.btn-wa{{display:inline-flex;align-items:center;gap:10px;background:#25D366;color:#fff;padding:14px 28px;border-radius:12px;font-weight:700;font-size:16px;transition:background .2s}}
.btn-wa:hover{{background:#1fba58}}
.btn-app{{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);color:#fff;padding:14px 28px;border-radius:12px;font-weight:700;font-size:16px;border:1.5px solid rgba(255,255,255,.2);transition:background .2s}}
.btn-app:hover{{background:rgba(255,255,255,.18)}}
.site-footer{{background:#050b1a;color:#9ca3af;padding:40px 0 24px;font-size:13px}}
.footer-inner{{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}}
.footer-logo-img{{height:36px;filter:brightness(0) invert(1)}}
.footer-links{{display:flex;gap:20px;flex-wrap:wrap}}
.footer-links a{{color:#9ca3af;transition:color .2s}}
.footer-links a:hover{{color:#fff}}
.footer-copy{{color:#4b5563;margin-top:20px;padding-top:20px;border-top:1px solid rgba(255,255,255,.06);text-align:center}}
.float-wa{{position:fixed;bottom:24px;left:24px;width:52px;height:52px;background:#25D366;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(37,211,102,.4);z-index:999;transition:transform .2s}}
.float-wa:hover{{transform:scale(1.1)}}
.float-wa svg{{width:26px;height:26px;fill:#fff}}
@media(max-width:900px){{
  .hero-inner{{grid-template-columns:1fr;min-height:auto}}
  .hero-text{{padding:40px 20px 32px}}
  .hero-image{{height:280px}}
  .steps-grid{{grid-template-columns:repeat(2,1fr);gap:32px}}
  .steps-grid::before{{display:none}}
  .trust-grid{{grid-template-columns:repeat(2,1fr);gap:16px}}
  .trust-item{{border-left:none;border-bottom:1px solid rgba(255,255,255,.1);padding-bottom:16px}}
  .trust-item:nth-child(3),.trust-item:nth-child(4){{border-bottom:none}}
  .cards-grid{{grid-template-columns:1fr}}
}}
@media(max-width:768px){{
  .hamburger{{display:flex}}
  .nav-list{{display:none}}
  .nav-list.open{{display:flex;flex-direction:column;position:fixed;top:68px;right:0;left:0;background:var(--white);padding:16px 20px;border-top:1px solid var(--border);box-shadow:0 8px 24px rgba(0,0,0,.12);z-index:199;gap:0}}
  .nav-list.open .has-dropdown{{width:100%}}
  .nav-list.open .nav-link-drop{{padding:12px 4px;width:100%;justify-content:space-between;border-radius:0;border-bottom:1px solid var(--border)}}
  .nav-list.open .dropdown{{display:block;position:static;box-shadow:none;border:none;border-radius:0;padding:4px 0 8px;background:var(--grey-bg)}}
}}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-1QSFZS28PT"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-1QSFZS28PT');</script>
</head>
<body>

<header class="site-header">
  <div class="container">
    <div class="nav-inner">
      <a class="logo" href="https://hub.rafeeg.ae/" aria-label="رفيق هاب">
        <img src="https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png" alt="رفيق" width="110" height="42" loading="eager">
      </a>
      <nav aria-label="التنقل الرئيسي">
        <ul class="nav-list" id="main-nav">
          <li class="has-dropdown">
            <a class="nav-link-drop" href="#" aria-haspopup="true">الإمارات <span class="drop-arrow">▾</span></a>
            <ul class="dropdown">
              <li><a href="https://hub.rafeeg.ae/أبوظبي/">أبوظبي</a></li>
              <li><a href="https://hub.rafeeg.ae/دبي/">دبي</a></li>
              <li><a href="https://hub.rafeeg.ae/الشارقة/">الشارقة</a></li>
              <li><a href="https://hub.rafeeg.ae/عجمان/">عجمان</a></li>
            </ul>
          </li>
          <li class="has-dropdown">
            <a class="nav-link-drop" href="#" aria-haspopup="true">خدمات المكيفات <span class="drop-arrow">▾</span></a>
            <ul class="dropdown">
              <li><a href="https://hub.rafeeg.ae/تركيب-مكيفات/">تركيب مكيفات</a></li>
              <li><a href="https://hub.rafeeg.ae/صيانة-مكيفات/">صيانة مكيفات</a></li>
              <li><a href="https://hub.rafeeg.ae/تنظيف-مكيفات/">تنظيف مكيفات</a></li>
              <li><a href="https://hub.rafeeg.ae/اصلاح-مكيفات/">إصلاح مكيفات</a></li>
              <li><a href="https://hub.rafeeg.ae/شحن-فريون-مكيفات/">شحن فريون</a></li>
              <li><a href="https://hub.rafeeg.ae/فك-وتركيب-مكيفات/">فك وتركيب</a></li>
            </ul>
          </li>
          <li class="has-dropdown">
            <a class="nav-link-drop" href="#" aria-haspopup="true">جميع الخدمات <span class="drop-arrow">▾</span></a>
            <ul class="dropdown">
              <li><a href="https://hub.rafeeg.ae/تسليك-مواسير/">تسليك مواسير</a></li>
              <li><a href="https://hub.rafeeg.ae/أعمال-كهربائية/">كهربائي</a></li>
              <li><a href="https://hub.rafeeg.ae/دهان/">دهان</a></li>
              <li><a href="https://hub.rafeeg.ae/صيانة-عامة/">صيانة عامة</a></li>
            </ul>
          </li>
        </ul>
      </nav>
      <a class="nav-cta" href="https://wa.me/971600500200?text={d['wa_msg']}">احجز الآن</a>
      <button class="hamburger" id="hamburger" aria-label="قائمة التنقل" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<main>

<section class="cat-hero">
  <div class="hero-inner container" style="max-width:100%;padding:0">
    <div class="hero-text" style="padding-right:max(48px, calc((100vw - 1140px)/2 + 48px))">
      <nav class="breadcrumb" aria-label="مسار التنقل">
        <a href="https://hub.rafeeg.ae/">الرئيسية</a><span>›</span><span>{d['service_name_ar']}</span>
      </nav>
      <h1>{d['h1']}</h1>
      <p class="lead">{d['lead']}</p>
      <ul class="hero-bullets">{bullets_html}</ul>
      <div class="hero-actions">
        <a class="btn-primary" href="https://wa.me/971600500200?text={d['wa_msg']}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.025.507 3.94 1.395 5.618L0 24l6.545-1.379A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.885 0-3.655-.502-5.184-1.379l-.371-.221-3.884.818.831-3.807-.242-.393A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
          احجز عبر واتساب
        </a>
        <a class="btn-secondary" href="https://rafeeggoogle.onelink.me/C8Hp/news">📱 حمّل التطبيق</a>
      </div>
    </div>
    <div class="hero-image">
      <picture>
        <source srcset="/{slug}/hero.webp" type="image/webp">
        <img src="/{slug}/hero.jpg" alt="{d['h1']}" width="420" height="460" loading="eager" fetchpriority="high">
      </picture>
      <div class="hero-image-badge">
        <div><span>4.8 ★</span> متوسط التقييم</div>
        <div>+135,000 عميل راضٍ</div>
      </div>
    </div>
  </div>
</section>

<div class="trust-strip">
  <div class="container">
    <div class="trust-grid">{trust_html}</div>
  </div>
</div>

<section class="cards-section">
  <div class="container">
    <p class="section-label">حسب المدينة</p>
    <h2 class="section-title">أسعار وفنيون حسب إمارتك</h2>
    <p class="section-sub">اختر مدينتك للاطّلاع على الأسعار التفصيلية والفنيين المتاحين</p>
    <div class="cards-grid">{city_cards_html}</div>
  </div>
</section>

<section class="sub-section">
  <div class="container">
    <p class="section-label">ماذا تريد بالضبط؟</p>
    <h2 class="section-title">جميع خدمات المكيفات</h2>
    <p class="section-sub">اختر الخدمة التي تحتاجها مباشرةً</p>
    <div class="sub-grid">{sub_html}</div>
  </div>
</section>

<section class="how-section">
  <div class="container">
    <p class="section-label">طريقة العمل</p>
    <h2 class="section-title">كيف تحجز مع رفيق؟</h2>
    <p class="section-sub">4 خطوات بسيطة من الحجز إلى الانتهاء</p>
    <div class="steps-grid">
      <div class="step"><div class="step-num">1</div><div class="step-title">اختر الخدمة</div><p class="step-desc">حدد نوع الخدمة ومدينتك عبر التطبيق أو واتساب</p></div>
      <div class="step"><div class="step-num">2</div><div class="step-title">حدد الموعد</div><p class="step-desc">اختر الوقت المناسب لك، بما في ذلك نفس اليوم</p></div>
      <div class="step"><div class="step-num">3</div><div class="step-title">الفني يصل</div><p class="step-desc">فني معتمد يصل في الموعد مع كامل الأدوات والمعدات</p></div>
      <div class="step"><div class="step-num">4</div><div class="step-title">الدفع بعد الانتهاء</div><p class="step-desc">تأكد من جودة العمل ثم ادفع — كاش أو بطاقة</p></div>
    </div>
  </div>
</section>

<section class="pricing-section">
  <div class="container">
    <div class="pricing-wrap">
      <p class="section-label" style="text-align:center">الأسعار</p>
      <h2 class="section-title" style="text-align:center">أسعار {d['service_name_ar']}</h2>
      <p class="section-sub" style="text-align:center">أسعار شفافة — لا رسوم مخفية</p>
      <table class="pricing-table">
        <thead><tr><th>الخدمة</th><th>الوصف</th><th>يبدأ من</th></tr></thead>
        <tbody>{pricing_html}</tbody>
      </table>
      <div class="pricing-example">💡 {d['pricing_example']}</div>
    </div>
  </div>
</section>

<section class="compare-section">
  <div class="container">
    <p class="section-label" style="text-align:center">مقارنة المدن</p>
    <h2 class="section-title" style="text-align:center">أسعار وتفاصيل حسب كل إمارة</h2>
    <p class="section-sub" style="text-align:center;margin-bottom:28px">مقارنة سريعة تساعدك تختار</p>
    <div style="overflow-x:auto">
      <table class="compare-table">
        <thead><tr><th>الإمارة</th><th>السعر يبدأ من</th><th>وقت الوصول</th><th>الفنيون النشطون</th><th>الضمان</th></tr></thead>
        <tbody>{compare_html}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="container">
    <p class="section-label" style="text-align:center">الأسئلة الشائعة</p>
    <h2 class="section-title" style="text-align:center">كل ما تريد معرفته</h2>
    <p class="section-sub" style="text-align:center">إجابات دقيقة لأكثر الأسئلة تكراراً</p>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>

<section class="related-section">
  <div class="container">
    <p class="section-label">خدمات أخرى</p>
    <h2 class="section-title">قد تحتاج أيضاً</h2>
    <p class="section-sub">خدمات منزلية احترافية أخرى عبر رفيق</p>
    <div class="related-grid">
      <a href="https://hub.rafeeg.ae/تسليك-مواسير/" class="related-card"><div class="related-icon">🔧</div><div class="related-name">تسليك مواسير</div></a>
      <a href="https://hub.rafeeg.ae/أعمال-كهربائية/" class="related-card"><div class="related-icon">⚡</div><div class="related-name">كهربائي</div></a>
      <a href="https://hub.rafeeg.ae/دهان/" class="related-card"><div class="related-icon">🖌️</div><div class="related-name">دهان وديكور</div></a>
      <a href="https://hub.rafeeg.ae/صيانة-عامة/" class="related-card"><div class="related-icon">🏠</div><div class="related-name">صيانة عامة</div></a>
      <a href="https://hub.rafeeg.ae/نجارة-وديكور/" class="related-card"><div class="related-icon">🪵</div><div class="related-name">نجارة وديكور</div></a>
      <a href="https://hub.rafeeg.ae/مكافحة-حشرات/" class="related-card"><div class="related-icon">🐛</div><div class="related-name">مكافحة حشرات</div></a>
    </div>
  </div>
</section>

</main>

<section class="cta-banner">
  <div class="container">
    <h2>{d['cta_h2']}</h2>
    <p>{d['cta_p']}</p>
    <div class="cta-actions">
      <a class="btn-wa" href="https://wa.me/971600500200?text={d['wa_msg']}">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="#fff"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.025.507 3.94 1.395 5.618L0 24l6.545-1.379A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.885 0-3.655-.502-5.184-1.379l-.371-.221-3.884.818.831-3.807-.242-.393A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
        تواصل عبر واتساب
      </a>
      <a class="btn-app" href="https://rafeeggoogle.onelink.me/C8Hp/news">📱 حمّل التطبيق</a>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="footer-inner">
      <img class="footer-logo-img" src="https://ar.rafeeg.ae/wp-content/uploads/2024/06/Logo-Rafeeg-Arabic.png" alt="رفيق" width="110" height="36" loading="lazy">
      <div class="footer-links">
        <a href="https://hub.rafeeg.ae/">الرئيسية</a>
        <a href="https://hub.rafeeg.ae/صيانة-مكيفات/">صيانة مكيفات</a>
        <a href="https://hub.rafeeg.ae/تنظيف-مكيفات/">تنظيف مكيفات</a>
        <a href="https://hub.rafeeg.ae/اصلاح-مكيفات/">إصلاح مكيفات</a>
        <a href="https://hub.rafeeg.ae/تركيب-مكيفات/">تركيب مكيفات</a>
        <a href="https://hub.rafeeg.ae/شحن-فريون-مكيفات/">شحن فريون</a>
      </div>
    </div>
    <p class="footer-copy">© 2026 رفيق — جميع الحقوق محفوظة | خدمات منزلية احترافية في الإمارات</p>
  </div>
</footer>

<a class="float-wa" href="https://wa.me/971600500200" aria-label="تواصل عبر واتساب">
  <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.025.507 3.94 1.395 5.618L0 24l6.545-1.379A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.885 0-3.655-.502-5.184-1.379l-.371-.221-3.884.818.831-3.807-.242-.393A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
</a>

<script>
const h=document.getElementById('hamburger'),n=document.getElementById('main-nav');
h.addEventListener('click',()=>{{const o=n.classList.toggle('open');h.setAttribute('aria-expanded',o)}});
document.querySelectorAll('.faq-q').forEach(btn=>{{
  btn.addEventListener('click',()=>{{
    const item=btn.closest('.faq-item');
    const isOpen=item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i=>i.classList.remove('open'));
    if(!isOpen) item.classList.add('open');
    btn.setAttribute('aria-expanded',!isOpen);
  }});
}});
</script>
</body>
</html>"""

# ── RUNNER ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for svc in SERVICES:
        slug = svc["slug"]
        out_dir = BASE / slug
        out_dir.mkdir(exist_ok=True)
        html = build_page(svc)
        out_path = out_dir / "index.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"✓ {slug}/index.html  ({len(html):,} bytes)")
    print(f"\nPhase 1 complete — {len(SERVICES)} pages built.")
