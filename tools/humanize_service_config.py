#!/usr/bin/env python3
"""
humanize_service_config.py — Humanize body_content_html + FAQ answers in a service config

Reads the service Python config, humanizes text sections via Claude haiku,
writes updated text back, then rebuilds the pages.

Usage:
    python3 tools/humanize_service_config.py floor_ceramic
    python3 tools/humanize_service_config.py kitchen_ceramic
"""

import os, sys, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

# Auto-load .env
def _load_env():
    candidates = [BASE / ".env", BASE.parent / ".env"]
    for p in candidates:
        if p.is_file():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if not os.environ.get(k):
                        os.environ[k] = v
            break

_load_env()

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic", file=sys.stderr)
    sys.exit(1)

MODEL = "claude-haiku-4-5"
MAX_TOKENS = 8192

SYSTEM_PROMPT = """أنت محرر محتوى رقمي متخصص في إعادة صياغة النصوص العربية لمواقع الخدمات المنزلية في الإمارات العربية المتحدة.

مهمتك: إعادة كتابة النص المُدخل بأسلوب بشري طبيعي يتناسب مع الجمهور الخليجي.

قواعد صارمة يجب الالتزام بها:
1. احتفظ بجميع الأرقام والأسعار كما هي (30 درهم/م²، 45 د.إ، إلخ) — لا تحوّلها إلى كلمات
2. احتفظ بجميع الأسماء والأماكن والعلامات التجارية كما هي (رفيق، أبوظبي، المارينا، إلخ)
3. احتفظ بجميع الـ placeholders كما هي ({city}، {neighborhoods_full}، إلخ) — لا تحذفها أو تغيّرها
4. احتفظ بجميع وسوم HTML كما هي (<h2>، <li>، <strong>، إلخ) — فقط أعد صياغة النصوص بين الوسوم
5. لا تستخدم ضمير المتكلم المفرد (أنا، أرى، أعتقد)
6. لا تضف معلومات أو أسعار جديدة غير موجودة في النص الأصلي
7. أسلوب الكتابة: معياري خليجي، تجاري مباشر، ثقة عالية
8. الطول: حافظ على نفس طول النص تقريباً
9. أعد النص المُعاد صياغته فقط — بدون مقدمات أو تعليقات"""


def _clean(text: str) -> str:
    """Remove preambles, markdown bold, and collapse newlines injected by Haiku."""
    # Strip preamble lines like "إليك النص معاد الصياغة:" or "النص المُعاد صياغته:"
    text = re.sub(r'^[^\n]{0,60}[:：]\s*\n+', '', text.strip())
    # Remove markdown bold (**text**) — keep the inner text
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Collapse multiple newlines / carriage returns into a single space
    text = re.sub(r'\r?\n+', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def humanize(text: str, client) -> str:
    msg = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"أعد صياغة النص التالي بأسلوب بشري طبيعي:\n\n{text}"}],
    )
    return _clean(msg.content[0].text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/humanize_service_config.py <service_name>")
        print("Example: python3 tools/humanize_service_config.py floor_ceramic")
        sys.exit(1)

    service_name = sys.argv[1]
    service_path = BASE / "services" / f"{service_name}.py"

    if not service_path.exists():
        print(f"ERROR: {service_path} not found")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Import the service module to get configs
    import importlib.util
    spec = importlib.util.spec_from_file_location(service_name, service_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    svc = mod.SERVICE_CONFIG
    source = service_path.read_text(encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Humanizing: {service_name}")
    print(f"{'='*60}\n")

    # ── 1. Humanize body_content_html ────────────────────────────
    body_html = svc.get("body_content_html", "")
    if body_html.strip():
        print(f"  [1/2] body_content_html ({len(body_html)} chars)...", end=" ", flush=True)
        humanized_body = humanize(body_html, client)
        print("done!")

        # Replace in source file — find the exact string between triple-quote block
        old_body = re.escape(body_html)
        source = source.replace(body_html, humanized_body)
    else:
        print("  [1/2] body_content_html — not found, skipping")

    # ── 2. Humanize FAQ answers ──────────────────────────────────
    faqs = svc.get("faqs", [])
    print(f"\n  [2/2] FAQs ({len(faqs)} questions)...")
    for i, faq in enumerate(faqs, 1):
        answer = faq.get("a", "")
        if not answer:
            continue
        print(f"    FAQ {i}/{len(faqs)} ({len(answer)} chars)...", end=" ", flush=True)
        humanized_answer = humanize(answer, client)
        print("done!")
        # Replace in source
        source = source.replace(answer, humanized_answer)

    # ── 3. Write updated source ──────────────────────────────────
    service_path.write_text(source, encoding="utf-8")
    print(f"\n  ✓ Updated: {service_path}")

    # ── 4. Rebuild all cities ────────────────────────────────────
    print(f"\n  Rebuilding all cities...\n")
    import subprocess
    result = subprocess.run(
        [sys.executable, str(BASE / "build.py"), service_name],
        capture_output=True, text=True, cwd=str(BASE)
    )
    print(result.stdout)
    if result.returncode != 0:
        print("  BUILD ERROR:", result.stderr)
        sys.exit(1)

    print(f"\n  ✅ Done! All pages humanized and rebuilt.")


if __name__ == "__main__":
    main()
