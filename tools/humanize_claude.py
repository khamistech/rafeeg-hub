#!/usr/bin/env python3
"""
humanize_claude.py — Humanize Arabic SEO content via Claude API

Rewrites AI-generated Arabic text into natural Gulf-inflected MSA.
Better Arabic quality than undetectable.ai (which is English-first).

Usage:
    python tools/humanize_claude.py --text "النص هنا" --api-key sk-ant-...
    python tools/humanize_claude.py --file input.txt --api-key KEY --output out.txt
    python tools/humanize_claude.py --file input.txt --api-key KEY --output out.txt --chunks
    python tools/humanize_claude.py --service wall-ceramic --city أبوظبي --api-key KEY

    # Use ANTHROPIC_API_KEY env var to skip --api-key flag:
    export ANTHROPIC_API_KEY=sk-ant-...
    python tools/humanize_claude.py --file input.txt
"""

import argparse
import os
import re
import sys

try:
    import anthropic
except ImportError:
    print("  ERROR  anthropic SDK not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

# Auto-load .env — search from script location upward
def _load_env():
    # Try: same dir as script, parent (project root), cwd
    candidates = []
    try:
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
        candidates.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    except NameError:
        pass
    candidates.append(os.path.join(os.getcwd(), ".env"))

    for env_path in candidates:
        if os.path.isfile(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip()
                        if not os.environ.get(k):   # overwrite blank placeholders
                            os.environ[k] = v
            break

_load_env()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL = "claude-haiku-4-5"          # Fast + cheap for rewriting (~$0.001 per page)
MAX_TOKENS = 8192
CHUNK_SIZE = 3000                    # chars per chunk (auto-chunked above this)

# Service configs (for --service + --city mode)
SERVICE_CONFIGS = {
    "wall-ceramic":      {"slug_prefix": "تركيب-سيراميك-جدران"},
    "bathroom-ceramic":  {"slug_prefix": "تركيب-سيراميك-حمامات"},
    "floor-ceramic":     {"slug_prefix": "تركيب-سيراميك-أرضيات"},
    "kitchen-ceramic":   {"slug_prefix": "تركيب-سيراميك-مطابخ"},
    "parquet":           {"slug_prefix": "تركيب-باركيه"},
    "curtains":          {"slug_prefix": "تركيب-ستائر"},
    "ac":                {"slug_prefix": "تكييف"},
}

# ---------------------------------------------------------------------------
# System prompt — Gulf Arabic humanization
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """أنت محرر محتوى رقمي متخصص في إعادة صياغة النصوص العربية لمواقع الخدمات المنزلية في الإمارات العربية المتحدة.

مهمتك: إعادة كتابة النص المُدخل بأسلوب بشري طبيعي يتناسب مع الجمهور الخليجي.

قواعد صارمة يجب الالتزام بها:
1. احتفظ بجميع الأرقام والأسعار كما هي (30 درهم/م²، 45 د.إ، إلخ) — لا تحوّلها إلى كلمات
2. احتفظ بجميع الأسماء والأماكن والعلامات التجارية كما هي (رفيق، أبوظبي، المارينا، إلخ)
3. لا تستخدم ضمير المتكلم المفرد (أنا، أرى، أعتقد، من خبرتي، شخصياً)
4. لا تضف معلومات أو أسعار أو ادعاءات جديدة غير موجودة في النص الأصلي
5. حافظ على جميع الروابط والـ slugs كما هي
6. أسلوب الكتابة: معياري خليجي (لهجة الإمارات والخليج)، تجاري مباشر، ثقة عالية
7. الطول: حافظ على نفس طول النص تقريباً — لا تختصر ولا تطوّل كثيراً
8. أعد النص المُعاد صياغته فقط — بدون مقدمات أو تعليقات"""

USER_PROMPT_TEMPLATE = """أعد صياغة النص التالي بأسلوب بشري طبيعي:

{text}"""


# ---------------------------------------------------------------------------
# Core humanization
# ---------------------------------------------------------------------------
def humanize_chunk(text: str, client: anthropic.Anthropic, model: str = MODEL) -> str:
    """Humanize a single chunk of text via Claude."""
    message = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)}
        ],
    )
    return message.content[0].text.strip()


def humanize(text: str, client: anthropic.Anthropic,
             use_chunks: bool = False, model: str = MODEL) -> str:
    """Full humanization pipeline — single pass or chunked."""
    if not use_chunks or len(text) <= CHUNK_SIZE:
        print(f"  Sending to Claude ({len(text)} chars)...", end=" ", flush=True)
        result = humanize_chunk(text, client, model)
        print("done!")
        return result

    # Chunked mode — split on paragraph breaks
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) > CHUNK_SIZE and current:
            chunks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current.strip():
        chunks.append(current.strip())

    print(f"  Chunked into {len(chunks)} parts ({len(text)} chars total)")
    results = []
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}/{len(chunks)} ({len(chunk)} chars)...", end=" ", flush=True)
        results.append(humanize_chunk(chunk, client, model))
        print("done!")

    return "\n\n".join(results)


# ---------------------------------------------------------------------------
# Run modes
# ---------------------------------------------------------------------------
def run_text_mode(text: str, client: anthropic.Anthropic,
                  output_path: str = None, use_chunks: bool = False,
                  model: str = MODEL) -> None:
    print(f"\n  Input : {len(text)} chars\n")
    result = humanize(text, client, use_chunks, model)
    print(f"\n  Output: {len(result)} chars")
    print(f"  --- Before (first 150 chars) ---")
    print(f"  {text[:150]}...")
    print(f"  --- After  (first 150 chars) ---")
    print(f"  {result[:150]}...")
    print()

    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"  Saved to: {output_path}\n")
    else:
        print("  --- Full output ---")
        print(result)
        print()


def run_service_mode(service: str, city: str, client: anthropic.Anthropic,
                     use_chunks: bool = False, model: str = MODEL) -> None:
    if service not in SERVICE_CONFIGS:
        print(f"  ERROR  Unknown service '{service}'. Available: {', '.join(SERVICE_CONFIGS.keys())}",
              file=sys.stderr)
        sys.exit(1)

    slug_prefix = SERVICE_CONFIGS[service]["slug_prefix"]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    slug_dir = os.path.join(base_dir, f"{slug_prefix}-{city}")

    if not os.path.isdir(slug_dir):
        candidates = [d for d in os.listdir(base_dir)
                      if d.startswith(slug_prefix) and os.path.isdir(os.path.join(base_dir, d))]
        print(f"  ERROR  Directory not found: {slug_dir}", file=sys.stderr)
        if candidates:
            print(f"  Available: {', '.join(candidates)}")
        sys.exit(1)

    body_file = os.path.join(slug_dir, "body_content.txt")
    if not os.path.isfile(body_file):
        print(f"  ERROR  body_content.txt not found in {slug_dir}", file=sys.stderr)
        print(f"  Tip: extract it first with the build script or manually.", file=sys.stderr)
        sys.exit(1)

    with open(body_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("  ERROR  body_content.txt is empty", file=sys.stderr)
        sys.exit(1)

    print(f"\n  Service   : {service}")
    print(f"  City      : {city}")
    print(f"  Directory : {slug_dir}")
    print(f"  Length    : {len(text)} chars\n")

    result = humanize(text, client, use_chunks, model)

    out_file = os.path.join(slug_dir, "body_humanized.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\n  Output: {len(result)} chars")
    print(f"  Saved : {out_file}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Humanize Arabic SEO content via Claude API"
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--text",    help="Raw Arabic text to humanize")
    input_group.add_argument("--file",    help="Path to .txt file to humanize")
    input_group.add_argument("--service", help=f"Service key ({', '.join(SERVICE_CONFIGS.keys())})")

    parser.add_argument("--city",     help="City name (required with --service)")
    parser.add_argument("--api-key",  help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--output",   help="Output file path (for --text or --file mode)")
    parser.add_argument("--chunks",   action="store_true",
                        help="Split long text into ~2000-char chunks (for texts >4000 chars)")
    parser.add_argument("--model",    default=MODEL,
                        help=f"Claude model to use (default: {MODEL})")

    args = parser.parse_args()

    # Resolve API key
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        parser.error("Provide --api-key or set ANTHROPIC_API_KEY environment variable")

    # Validate input
    if not args.text and not args.file and not args.service:
        parser.error("One of --text, --file, or --service is required")
    if args.service and not args.city:
        parser.error("--city is required when using --service")

    # Override model if specified
    model = args.model

    client = anthropic.Anthropic(api_key=api_key)

    # Dispatch
    if args.service:
        run_service_mode(args.service, args.city, client, args.chunks, model)
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"  ERROR  File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            print(f"  ERROR  File is empty: {args.file}", file=sys.stderr)
            sys.exit(1)
        run_text_mode(text, client, args.output, args.chunks, model)
    else:
        run_text_mode(args.text, client, args.output, args.chunks, model)


if __name__ == "__main__":
    main()
