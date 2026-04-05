#!/usr/bin/env python3
"""
Humanize body_content for تركيب-سيراميك city pages via undetectable.ai
Then rebuild and push to GitHub.
"""

import json, os, re, subprocess, sys, time, urllib.request

API_KEY = "02c2b10c-5a39-40c7-b471-7e35ef93802e"
SUBMIT_URL = "https://humanize.undetectable.ai/submit"
POLL_URL   = "https://humanize.undetectable.ai/document"
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(BASE_DIR, "_configs")

SLUGS = [
    "تركيب-سيراميك-دبي",
    "تركيب-سيراميك-أبوظبي",
    "تركيب-سيراميك-الشارقة",
    "تركيب-سيراميك-عجمان",
]

STRIP_PHRASES = [
    "من وجهة نظري", "أستعمل", "في رأيي", "شخصياً",
    "من خبرتي،", "من خبرتي", "من تجربتي،", "من تجربتي",
    "أنا أرى أن", "أنا أختار", "أعتقد أن", "أجد أن",
    "حيثما أمكن،", "حيثما أمكن",
    "مدخلات المستخدم:", "وهنا مدخلات المستخدم:",
]


def strip_html(html):
    return re.sub(r"<[^>]+>", " ", html)


def submit_text(text):
    payload = json.dumps({
        "content": text,
        "readability": "University",
        "purpose": "General Writing",
        "strength": "More Human",
    }).encode("utf-8")
    req = urllib.request.Request(
        SUBMIT_URL,
        data=payload,
        headers={"apikey": API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
    return resp["id"]


def poll_result(doc_id, timeout=180):
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(
            POLL_URL,
            data=json.dumps({"id": doc_id}).encode(),
            headers={"apikey": API_KEY, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        output = data.get("output")
        if output:
            return output
        time.sleep(6)
    raise TimeoutError(f"Timed out after {timeout}s for doc {doc_id}")


def clean_output(text):
    for phrase in STRIP_PHRASES:
        text = text.replace(phrase, "")
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def reintegrate_humanized(original_html, humanized_plain):
    """
    Replace paragraph text content in original HTML with the humanized version,
    preserving all HTML tags and headings structure.
    We split by sentence-chunks and reintegrate intelligently.
    """
    # Extract text blocks from original HTML (between tags)
    text_blocks = re.findall(r">([^<]{30,})<", original_html)
    humanized_sentences = re.split(r"(?<=[.!?؟])\s+", humanized_plain)

    result_html = original_html
    h_idx = 0
    for block in text_blocks:
        block_stripped = block.strip()
        if not block_stripped or len(block_stripped) < 20:
            continue
        if h_idx >= len(humanized_sentences):
            break
        # Collect enough sentences to approximately match the block length
        replacement = ""
        while h_idx < len(humanized_sentences) and len(replacement) < len(block_stripped) * 0.6:
            replacement += (" " if replacement else "") + humanized_sentences[h_idx]
            h_idx += 1
        replacement = replacement.strip()
        if replacement:
            result_html = result_html.replace(block_stripped, replacement, 1)

    return result_html


print("=" * 60)
print("  Humanizing تركيب-سيراميك city pages")
print("=" * 60)

updated_slugs = []

for slug in SLUGS:
    config_path = os.path.join(CONFIGS_DIR, f"{slug}.json")
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)

    body_html = cfg.get("body_content", "").strip()
    if not body_html:
        print(f"  SKIP  {slug} — empty body_content")
        continue

    plain_text = strip_html(body_html)
    plain_text = re.sub(r"\s+", " ", plain_text).strip()

    print(f"\n  [{slug}]")
    print(f"    Submitting {len(plain_text)} chars to undetectable.ai...")

    try:
        doc_id = submit_text(plain_text)
        print(f"    Doc ID: {doc_id} — polling...")
        humanized = poll_result(doc_id)
        humanized = clean_output(humanized)
        print(f"    Received {len(humanized)} chars")

        # Reintegrate humanized text back into original HTML structure
        new_body_html = reintegrate_humanized(body_html, humanized)
        cfg["body_content"] = new_body_html

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        print(f"    ✅ Config updated")
        updated_slugs.append(slug)

    except Exception as e:
        print(f"    ❌ ERROR: {e}", file=sys.stderr)

# Rebuild updated pages
if updated_slugs:
    print(f"\n  Rebuilding {len(updated_slugs)} pages...")
    for slug in updated_slugs:
        result = subprocess.run(
            [sys.executable, "_build_page.py", f"_configs/{slug}.json"],
            capture_output=True, text=True, cwd=BASE_DIR
        )
        if "✅" in result.stdout:
            print(f"    ✅ Built {slug}")
        else:
            print(f"    ❌ Build failed for {slug}: {result.stderr}")

print("\nDone.")
