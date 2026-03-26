"""
Shared CSS for ALL Rafeeg service pages.
This file is NEVER modified when creating new service types.
120+ inline CSS classes matching the design system.
"""


def get_css():
    """Return the complete CSS string for inline <style> tag."""
    return """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--green:#189F18;--green-dark:#117A11;--blue:#2B5DF5;--dark:#030712;--text:#1a1a2e;--muted:#6b7280;--border:#e5e7eb;--hero-bg:#eef9ee;--hero-circle:#c8e6c8;--white:#ffffff;--grey-bg:#f1f5f9;--shadow-sm:0 2px 8px rgba(0,0,0,.06);--shadow:0 4px 20px rgba(0,0,0,.08);--radius:16px;--radius-sm:10px;--wa-green:#25D366}
html{scroll-behavior:smooth}
body{font-family:'Cairo','Segoe UI',system-ui,sans-serif;font-size:16px;color:var(--text);background:var(--white);direction:rtl;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
img{max-width:100%;height:auto;display:block}
.container{max-width:1080px;margin:0 auto;padding:0 20px}
.btn-green{display:inline-flex;align-items:center;gap:8px;background:var(--green);color:#fff;padding:14px 28px;border-radius:var(--radius-sm);font-size:16px;font-weight:700;font-family:'Cairo',sans-serif;border:none;cursor:pointer;transition:background .2s,transform .15s,box-shadow .15s;white-space:nowrap}
.btn-green:hover{background:var(--green-dark);transform:translateY(-2px);box-shadow:0 6px 20px rgba(24,159,24,.35)}
.btn-whatsapp{display:inline-flex;align-items:center;gap:8px;background:transparent;color:var(--wa-green);border:2px solid var(--wa-green);padding:13px 28px;border-radius:var(--radius-sm);font-size:16px;font-weight:700;font-family:'Cairo',sans-serif;cursor:pointer;transition:all .2s;white-space:nowrap}
.btn-whatsapp:hover{background:var(--wa-green);color:#fff}
.btn-whatsapp-solid{display:inline-flex;align-items:center;gap:8px;background:var(--wa-green);color:#fff;padding:14px 28px;border-radius:var(--radius-sm);font-size:16px;font-weight:700;font-family:'Cairo',sans-serif;border:none;cursor:pointer;transition:background .2s,transform .15s;white-space:nowrap}
.btn-whatsapp-solid:hover{background:#1fba58;transform:translateY(-2px)}
.btn-outline{display:inline-flex;align-items:center;gap:8px;background:transparent;color:var(--green);border:2px solid var(--green);padding:12px 26px;border-radius:var(--radius-sm);font-size:15px;font-weight:700;font-family:'Cairo',sans-serif;cursor:pointer;transition:all .2s}
.btn-outline:hover{background:var(--green);color:#fff}
.site-header{position:sticky;top:0;z-index:200;background:var(--white);border-bottom:1px solid var(--border);box-shadow:var(--shadow-sm)}
.header-inner{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.logo img{height:42px;width:auto}
.nav-list{display:flex;align-items:center;gap:6px;list-style:none;font-size:15px;font-weight:600}
.nav-list a{color:var(--text);transition:color .2s}
.nav-list a:hover{color:var(--green)}
.has-dropdown{position:relative}
.nav-link-drop{display:flex;align-items:center;gap:5px;padding:8px 14px;border-radius:8px;cursor:pointer;color:var(--text);font-weight:600;font-size:15px;transition:background .15s,color .2s;white-space:nowrap}
.nav-link-drop:hover{background:var(--grey-bg);color:var(--green)}
.drop-arrow{font-size:9px;transition:transform .2s;display:inline-block;margin-top:1px}
.has-dropdown:hover .drop-arrow{transform:rotate(180deg)}
.dropdown{display:none;position:absolute;top:calc(100% + 6px);right:0;background:var(--white);border:1px solid var(--border);border-radius:12px;min-width:180px;padding:6px 0;box-shadow:0 8px 24px rgba(0,0,0,.12);z-index:300;list-style:none;margin:0}
.has-dropdown:hover .dropdown{display:block}
.dropdown li a{display:block;padding:10px 18px;color:var(--text);font-size:14px;font-weight:500;transition:background .12s,color .12s}
.dropdown li a:hover{background:var(--grey-bg);color:var(--green)}
.header-actions{display:flex;align-items:center;gap:12px}
.phone-link{display:flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--text);direction:ltr;white-space:nowrap}
.btn-lang{background:var(--blue);color:#fff;padding:8px 18px;border-radius:8px;font-size:14px;font-weight:700;font-family:'Cairo',sans-serif;white-space:nowrap;transition:opacity .2s}
.btn-lang:hover{opacity:.88}
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:4px;background:none;border:none}
.hamburger span{width:24px;height:2px;background:var(--dark);border-radius:2px}
.breadcrumb{background:#f3f4f8;padding:10px 0;font-size:13px;color:var(--muted);border-bottom:1px solid var(--border)}
.breadcrumb-inner{display:flex;align-items:center;justify-content:space-between;gap:16px}
.breadcrumb a{color:var(--muted);transition:color .2s}
.breadcrumb a:hover{color:var(--green)}
.breadcrumb .sep{margin:0 6px}
.reading-time{display:flex;align-items:center;gap:5px;font-size:12px;font-weight:600;color:var(--muted);white-space:nowrap}
.hero-wrap{padding:16px 20px 8px;max-width:1080px;margin:0 auto}
.hero{background:var(--hero-bg);border-radius:var(--radius);overflow:hidden;display:grid;grid-template-columns:1fr 340px;min-height:380px;align-items:center}
.hero-text{padding:48px 40px 48px 20px}
.hero-badge{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.9);border-radius:20px;padding:5px 14px;font-size:13px;font-weight:700;color:var(--text);margin-bottom:18px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.hero-badge svg{width:14px;height:14px;fill:#f59e0b}
.hero h2{font-size:clamp(26px,3.5vw,40px);font-weight:900;line-height:1.2;color:var(--dark);margin-bottom:10px;letter-spacing:-.02em;text-wrap:balance}
.hero-sub{font-size:clamp(15px,1.8vw,20px);font-weight:700;color:var(--green);margin-bottom:22px}
.hero-bullets{list-style:none;display:flex;flex-direction:column;gap:9px;margin-bottom:28px;align-items:flex-start}
.hero-bullets li{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:600}
.chk{width:20px;height:20px;background:var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:900;flex-shrink:0}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap}
.hero-image{position:relative;height:380px;display:flex;align-items:flex-end;justify-content:center;overflow:hidden}
.hero-image::before{content:'';position:absolute;bottom:-20px;left:50%;transform:translateX(-50%);width:300px;height:300px;background:var(--hero-circle);border-radius:50%}
.hero-image img{position:relative;height:100%;width:auto;object-fit:cover;object-position:top center}
.sec-label{text-align:center;font-size:12px;font-weight:700;color:var(--green);letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px}
.sec-label::before{content:'◆ ';font-size:7px;vertical-align:2px}
.sec-title{text-align:center;font-size:clamp(22px,2.6vw,28px);font-weight:800;color:var(--dark);margin-bottom:8px;letter-spacing:-.02em}
.sec-sub{text-align:center;color:var(--muted);font-size:15px;margin-bottom:36px}
.features-section{padding:52px 0 44px;background:var(--white)}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.feat-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:22px 20px;display:flex;align-items:center;gap:16px;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s}
.feat-card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.feat-icon{width:48px;height:48px;background:var(--grey-bg);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
.feat-title{font-size:15px;font-weight:700;margin-bottom:3px}
.feat-desc{font-size:13px;color:var(--muted);line-height:1.5}
.pricing-section{padding:56px 0;background:var(--grey-bg)}
.pricing-box{background:var(--white);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);max-width:580px;margin:0 auto 20px}
.pricing-table{width:100%;border-collapse:collapse;font-size:15px}
.pricing-table th{background:var(--dark);color:#fff;padding:15px 22px;text-align:center;font-size:14px;font-weight:700}
.pricing-table td{padding:14px 22px;text-align:center;border-bottom:1px solid var(--border);font-weight:600}
.pricing-table tr:last-child td{border-bottom:none}
.pricing-table tr:nth-child(even) td{background:#f9fafb}
.pricing-note{text-align:center;font-size:13px;color:var(--muted);margin-top:10px;margin-bottom:24px}
.pricing-cta{text-align:center}
.calc-section{padding:56px 0;background:var(--white)}
.calc-box{max-width:580px;margin:0 auto;background:var(--grey-bg);border:1px solid var(--border);border-radius:var(--radius);padding:32px 28px}
.calc-field{margin-bottom:22px}
.calc-label{display:block;font-size:14px;font-weight:700;margin-bottom:10px;color:var(--dark)}
.calc-select{width:100%;padding:12px 16px;border:1px solid var(--border);border-radius:var(--radius-sm);font-family:'Cairo',sans-serif;font-size:15px;font-weight:600;color:var(--dark);background:var(--white);cursor:pointer;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%236b7280' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:left 16px center}
.calc-slider-wrap{display:flex;align-items:center;gap:12px}
.calc-slider{flex:1;-webkit-appearance:none;appearance:none;height:6px;background:var(--border);border-radius:3px;direction:ltr;cursor:pointer}
.calc-slider::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;background:var(--green);border-radius:50%;cursor:pointer;box-shadow:0 2px 6px rgba(24,159,24,.4)}
.calc-units-val{min-width:36px;text-align:center;font-size:20px;font-weight:900;color:var(--dark)}
.calc-result{background:var(--dark);color:#fff;border-radius:var(--radius-sm);padding:20px 24px;text-align:center;margin-top:8px}
.calc-result-label{font-size:13px;color:#9ca3af;margin-bottom:6px}
.calc-result-range{font-size:26px;font-weight:900;color:var(--green)}
.calc-result-note{font-size:12px;color:#6b7280;margin-top:6px}
.persona-section{padding:56px 0;background:var(--grey-bg)}
.persona-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.persona-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:22px 20px;display:flex;flex-direction:column;gap:8px;transition:box-shadow .2s,transform .2s}
.persona-card:hover{box-shadow:var(--shadow);transform:translateY(-2px)}
.persona-top{display:flex;align-items:center;gap:12px;margin-bottom:4px}
.persona-emoji{font-size:28px;flex-shrink:0}
.persona-name{font-size:15px;font-weight:800;color:var(--dark);line-height:1.2}
.persona-role{font-size:12px;color:var(--green);font-weight:600}
.persona-scenario{font-size:13px;color:var(--text);line-height:1.65;flex:1}
.persona-price-row{display:flex;align-items:center;justify-content:space-between;margin-top:8px;padding-top:10px;border-top:1px solid var(--border)}
.persona-price-tag{background:var(--dark);color:var(--green);font-size:15px;font-weight:900;padding:5px 14px;border-radius:8px}
.persona-price-what{font-size:11px;color:var(--muted);text-align:left;max-width:55%;line-height:1.4}
.proof-section{padding:56px 0;background:var(--grey-bg)}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:48px}
.stat-card{text-align:center;padding:28px 16px;background:var(--white);border-radius:var(--radius);border:1px solid var(--border)}
.stat-num{font-size:38px;font-weight:900;color:var(--dark);line-height:1;margin-bottom:6px}
.stat-num em{color:var(--green);font-style:normal}
.stat-label{font-size:13px;color:var(--muted);font-weight:600}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.review-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:24px}
.review-top{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.review-avatar{width:44px;height:44px;border-radius:50%;object-fit:cover;flex-shrink:0}
.review-name{font-weight:700;font-size:15px}
.review-stars{color:#f59e0b;font-size:13px;letter-spacing:1px}
.review-text{font-size:14px;color:var(--text);line-height:1.65}
.providers-section{padding:56px 0;background:var(--white)}
.providers-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.provider-card{background:var(--white);border:1.5px solid var(--border);border-radius:var(--radius);padding:24px 22px;transition:border-color .2s,box-shadow .2s}
.provider-card:hover{border-color:var(--green);box-shadow:0 6px 24px rgba(24,159,24,.1)}
.provider-badge{display:inline-flex;align-items:center;gap:5px;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;margin-bottom:12px}
.provider-name{font-size:18px;font-weight:800;color:var(--dark);margin-bottom:4px}
.provider-stars{color:#f59e0b;font-size:13px;letter-spacing:1px;margin-bottom:10px}
.provider-rating-num{font-size:12px;color:var(--muted);font-weight:600;margin-right:4px}
.provider-desc{font-size:13px;color:var(--text);line-height:1.7;margin-bottom:14px}
.provider-meta{display:flex;flex-direction:column;gap:6px}
.provider-address{font-size:12px;color:var(--muted);display:flex;align-items:flex-start;gap:6px;line-height:1.4}
.provider-jobs{font-size:12px;font-weight:700;color:var(--green);display:flex;align-items:center;gap:5px}
.provider-tag{font-size:11px;background:var(--hero-bg);color:var(--green);padding:2px 8px;border-radius:20px;font-weight:600;display:inline-block;margin-top:6px}
.compare-section{padding:56px 0;background:var(--white)}
.compare-table-wrap{max-width:680px;margin:0 auto;background:var(--white);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}
.compare-table{width:100%;border-collapse:collapse;font-size:15px}
.compare-table th{padding:14px 20px;font-size:14px;font-weight:700;text-align:center}
.compare-table th:first-child{background:#f1f5f9;color:var(--dark);text-align:right}
.compare-table th.pro{background:var(--green);color:#fff}
.compare-table th.diy{background:#64748b;color:#fff}
.compare-table td{padding:13px 20px;border-top:1px solid var(--border);text-align:center;font-weight:600}
.compare-table td:first-child{text-align:right;font-weight:700;color:var(--dark)}
.compare-table tr:nth-child(even) td{background:#fafafa}
.ico-yes{color:var(--green);font-size:18px}
.ico-no{color:#64748b;font-size:18px}
.infographic-section{padding:56px 0;background:var(--dark);color:#fff;border-top:4px solid var(--green)}
.infographic-section .sec-label{color:#fff}
.infographic-section .sec-title{color:#fff}
.infographic-section .sec-sub{color:#9ca3af}
.infographic-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.info-card{text-align:center;padding:28px 16px;background:rgba(255,255,255,.06);border-radius:var(--radius);border:1px solid rgba(255,255,255,.1)}
.info-icon{font-size:36px;margin-bottom:12px;display:block}
.info-num{font-size:42px;font-weight:900;color:var(--green);line-height:1;margin-bottom:8px}
.info-label{font-size:13px;color:#9ca3af;font-weight:600;line-height:1.5}
.city-section{padding:56px 0;background:var(--white)}
.city-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.city-card{border:2px solid var(--border);border-radius:var(--radius);padding:22px 20px;background:var(--white);transition:border-color .2s,box-shadow .2s}
.city-card.active{border-color:var(--green);box-shadow:0 0 0 3px rgba(24,159,24,.12)}
.city-card-name{font-size:18px;font-weight:800;color:var(--dark);margin-bottom:4px}
.city-card-tag{font-size:12px;font-weight:700;color:var(--green);margin-bottom:12px;display:block}
.city-card.active .city-card-tag::before{content:'● ';font-size:9px;vertical-align:1px}
.city-card-areas{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:10px}
.city-card-price{font-size:15px;font-weight:700;color:var(--dark)}
.content-section{padding:64px 0;background:var(--grey-bg)}
.content-body h2{font-size:clamp(20px,2.5vw,26px);font-weight:800;color:var(--dark);margin:36px 0 12px;letter-spacing:-.02em}
.content-body h2:first-child{margin-top:0}
.content-body h3{font-size:18px;font-weight:700;color:var(--text);margin:24px 0 8px}
.content-body p{font-size:15px;color:var(--text);line-height:1.8;margin-bottom:14px}
.content-body ul{margin:10px 0 16px;padding-right:22px}
.content-body ul li{font-size:15px;color:var(--text);margin-bottom:8px;line-height:1.6}
.content-body strong{color:var(--dark)}
.steps-section{padding:56px 0;background:var(--white)}
.steps-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;position:relative}
.steps-grid::before{content:'';position:absolute;top:50px;right:10%;left:10%;height:2px;background:repeating-linear-gradient(to left,#e5e7eb 0,#e5e7eb 8px,transparent 8px,transparent 16px);z-index:0}
.step-card{text-align:center;padding:24px 12px;position:relative;z-index:1}
.step-num{width:52px;height:52px;background:var(--dark);color:#fff;border-radius:50%;font-size:20px;font-weight:900;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;position:relative;z-index:1;box-shadow:0 0 0 4px var(--white)}
.step-title{font-size:15px;font-weight:700;margin-bottom:7px;color:var(--dark)}
.step-desc{font-size:14px;color:var(--muted);line-height:1.55}
.media-section{padding:56px 0;background:var(--grey-bg)}
.ba-card{background:var(--white);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}
.ba-split{display:grid;grid-template-columns:1fr auto 1fr}
.ba-side{padding:20px 16px}
.ba-before{background:#fff5f5}
.ba-after{background:#f0faf0}
.ba-label-badge{display:inline-block;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;margin-bottom:12px;background:#fee2e2;color:#b91c1c}
.ba-label-badge.after{background:#dcfce7;color:#15803d}
.ba-icon-row{display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
.ba-stat{display:flex;align-items:center;gap:8px;font-size:13px}
.ba-stat strong{font-size:15px;font-weight:700}
.ba-stat small{color:var(--muted);font-size:11px;line-height:1.3}
.ba-stat.bad strong{color:#dc2626}
.ba-stat.good strong{color:var(--green)}
.ba-ico{font-size:18px;width:24px;flex-shrink:0}
.ba-desc{font-size:11px;color:var(--muted);line-height:1.5}
.ba-divider{display:flex;align-items:center;justify-content:center;padding:0 10px;font-size:20px;color:var(--muted);background:var(--border)}
.ba-footer{display:flex;justify-content:space-around;gap:12px;padding:12px 16px;background:var(--grey-bg);font-size:12px;color:var(--muted);border-top:1px solid var(--border)}
.ba-footer strong{color:var(--dark)}
.ba-img-wrap{position:relative}
.ba-img-labels{position:absolute;top:10px;left:0;right:0;display:flex;justify-content:space-between;padding:0 16px;pointer-events:none}
.ba-img-label{font-size:12px;font-weight:700;padding:4px 12px;border-radius:20px}
.ba-img-label.bad{background:#fee2e2;color:#b91c1c}
.ba-img-label.good{background:#dcfce7;color:#15803d}
.map-section{padding:56px 0;background:var(--white)}
.map-wrap{border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}
.map-wrap iframe{display:block;width:100%;height:360px;border:0}
.faq-section{padding:56px 0;background:var(--grey-bg)}
.faq-list{max-width:740px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
details{background:var(--white);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:border-color .2s}
details[open]{border-color:var(--green)}
summary{padding:18px 22px;font-size:16px;font-weight:700;cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;user-select:none}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';font-size:22px;color:var(--green);font-weight:400;flex-shrink:0;line-height:1}
details[open] summary::after{content:'−'}
.faq-answer{padding:0 22px 18px;font-size:15px;color:var(--muted);line-height:1.75}
.whatsapp-share-section{padding:40px 0;background:var(--white)}
.whatsapp-share-box{max-width:560px;margin:0 auto;background:var(--grey-bg);border:1px solid var(--border);border-radius:var(--radius);padding:28px 24px;text-align:center}
.whatsapp-share-box h3{font-size:18px;font-weight:700;color:var(--dark);margin-bottom:8px}
.whatsapp-share-box p{font-size:14px;color:var(--muted);margin-bottom:18px}
.links-section{padding:48px 0;background:var(--grey-bg)}
.links-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.link-card{display:block;background:var(--white);border:1px solid var(--border);border-radius:12px;padding:18px 20px;transition:border-color .2s,transform .2s,box-shadow .2s}
.link-card:hover{border-color:var(--green);transform:translateY(-2px);box-shadow:var(--shadow-sm)}
.link-card-title{font-weight:700;font-size:15px;color:var(--dark);margin-bottom:5px}
.link-card-desc{font-size:13px;color:var(--muted);line-height:1.5}
.cta-banner{background:#0d2b0d;padding:56px 0;text-align:center}
.cta-banner h2{font-size:clamp(22px,3vw,34px);font-weight:800;color:#fff;margin-bottom:12px}
.cta-banner p{color:#9ca3af;font-size:16px;margin-bottom:28px}
.cta-buttons{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.cta-banner .btn-whatsapp{color:var(--wa-green);border-color:var(--wa-green);background:transparent}
.cta-banner .btn-whatsapp:hover{background:var(--wa-green);color:#fff}
.site-footer{background:#050b1a;color:#9ca3af;padding:52px 0 24px}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;margin-bottom:40px}
.footer-logo-img{height:40px;width:auto;margin-bottom:16px;filter:brightness(0) invert(1)}
.footer-about{font-size:14px;line-height:1.7;margin-bottom:20px}
.footer-col-title{font-size:13px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:.06em;margin-bottom:16px}
.footer-links{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-links a{font-size:14px;color:#9ca3af;transition:color .2s}
.footer-links a:hover{color:var(--green)}
.footer-bottom{border-top:1px solid #111827;padding-top:20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
.footer-copy{font-size:13px}
.social-links{display:flex;gap:16px}
.social-links a{color:#6b7280;transition:color .2s}
.social-links a:hover{color:var(--green)}
.social-links svg{width:20px;height:20px;fill:currentColor;display:block}
.float-wa{position:fixed;bottom:90px;right:24px;z-index:999;width:56px;height:56px;background:var(--wa-green);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(37,211,102,.5);transition:transform .2s,box-shadow .2s;cursor:pointer}
.float-wa:hover{transform:scale(1.1);box-shadow:0 6px 24px rgba(37,211,102,.6)}
.float-wa svg{width:28px;height:28px;fill:#fff}
.float-wa-label{position:absolute;left:66px;right:auto;top:50%;transform:translateY(-50%);background:var(--dark);color:#fff;font-size:12px;font-weight:700;padding:6px 12px;border-radius:8px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .2s;font-family:'Cairo',sans-serif}
.float-wa:hover .float-wa-label{opacity:1}
@media(max-width:900px){.stats-grid{grid-template-columns:repeat(2,1fr)}.steps-grid{grid-template-columns:repeat(3,1fr)}.infographic-grid{grid-template-columns:repeat(2,1fr)}.links-grid{grid-template-columns:repeat(2,1fr)}.steps-grid::before{display:none}}
@media(max-width:768px){.nav-list{display:none}.hamburger{display:flex}.nav-list.open{display:flex;flex-direction:column;position:fixed;top:68px;right:0;left:0;background:var(--white);padding:16px 20px;border-top:1px solid var(--border);box-shadow:0 8px 24px rgba(0,0,0,.12);z-index:199;gap:0}.hero{grid-template-columns:1fr;min-height:auto}.hero-text{padding:28px 20px 16px}.hero-image{height:220px}.footer-grid{grid-template-columns:1fr;gap:28px}.steps-grid{grid-template-columns:repeat(2,1fr)}.links-grid{grid-template-columns:1fr}.float-wa{bottom:16px;right:16px}.providers-grid{grid-template-columns:1fr}}
@media(max-width:480px){.stats-grid{grid-template-columns:repeat(2,1fr)}.hero-image{height:190px}}
.sticky-cta{display:none;position:fixed;bottom:0;left:0;right:0;z-index:998;background:var(--dark);padding:12px 20px;gap:10px;align-items:center;justify-content:center;box-shadow:0 -4px 20px rgba(0,0,0,.25)}
.sticky-cta .btn-whatsapp-solid{flex:1;max-width:220px;justify-content:center;font-size:15px;padding:12px 16px}
.sticky-cta .btn-green{flex:1;max-width:200px;justify-content:center;font-size:15px;padding:12px 16px}
@media(max-width:768px){.sticky-cta{display:flex}body{padding-bottom:72px}}
.ai-summary{background:linear-gradient(135deg,#c6f6d5,#b2f5ea);border:2px solid #68d391;border-radius:var(--radius);padding:20px 24px;max-width:740px;margin:16px auto 8px}
.ai-summary-title{font-size:13px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px}
.ai-summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px}
.ai-fact{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:600;color:var(--dark)}
.ai-fact span{font-size:16px;flex-shrink:0}
.urgency-strip{background:#fef3c7;border-bottom:2px solid #f59e0b;padding:8px 0;text-align:center;font-size:13px;font-weight:700;color:#92400e}
.urgency-strip strong{color:#78350f}
.guarantee-seal{display:inline-flex;align-items:center;gap:8px;background:#dcfce7;border:2px solid var(--green);border-radius:12px;padding:10px 18px;font-size:14px;font-weight:700;color:var(--green-dark);margin-top:12px}
.guarantee-seal svg{width:20px;height:20px;fill:var(--green);flex-shrink:0}
.calc-cta-reveal{display:none;margin-top:16px;text-align:center}
.calc-cta-reveal.show{display:block}
.calc-cta-reveal .price-confirm{font-size:14px;color:#9ca3af;margin-bottom:10px}
.calc-cta-reveal .price-confirm strong{color:#fff}"""
