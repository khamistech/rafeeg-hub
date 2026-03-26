#!/usr/bin/env python3
"""
humanize.py - Humanize Arabic text via undetectable.ai API (v2)

Usage:
    python tools/humanize.py --text "Arabic text here" --api-key KEY
    python tools/humanize.py --file input.txt --api-key KEY --output output.txt
    python tools/humanize.py --service bathroom-ceramic --city أبوظبي --api-key KEY
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SUBMIT_URL = "https://humanize.undetectable.ai/submit"
POLL_URL = "https://humanize.undetectable.ai/document"
POLL_INTERVAL = 5       # seconds between polls
POLL_TIMEOUT = 120      # max seconds to wait

# Phrases the API tends to inject -- stripped in post-processing
FIRST_PERSON_PHRASES = [
    "من وجهة نظري",
    "أستعمل",
    "في رأيي",
    "شخصياً",
    "من خبرتي،",
    "من خبرتي",
    "من تجربتي،",
    "من تجربتي",
    "أنا أرى أن",
    "أنا أختار",
    "أنا أريد أن أعرف",
    "أحب أن أذكرك",
    "أعتقد أن",
    "أجد أن",
    "حيثما أمكن،",
    "حيثما أمكن",
    "مدخلات المستخدم:",
    "وهنا مدخلات المستخدم:",
]

# ---------------------------------------------------------------------------
# Service configs (for --service + --city mode)
# ---------------------------------------------------------------------------
SERVICE_CONFIGS = {
    "bathroom-ceramic": {
        "slug_prefix": "تركيب-سيراميك-حمامات",
    },
    # Future services can be added here
}


def _headers(api_key: str) -> dict:
    return {
        "apikey": api_key,
        "Content-Type": "application/json",
    }


def _post(url: str, body: dict, api_key: str) -> dict:
    """POST JSON and return parsed response."""
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=_headers(api_key), method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR  HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"  ERROR  Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def submit_text(text: str, api_key: str) -> str:
    """Submit text for humanization. Returns the document ID."""
    body = {
        "content": text,
        "strength": "More Human",
        "readability": "University",
        "purpose": "General Writing",
    }

    print("  Submitting text for humanization...")
    data = _post(SUBMIT_URL, body, api_key)

    doc_id = data.get("id")
    if not doc_id:
        print(f"  ERROR  No document ID in response: {json.dumps(data, ensure_ascii=False)[:300]}",
              file=sys.stderr)
        sys.exit(1)

    print(f"  Document ID: {doc_id}")
    return doc_id


def poll_result(doc_id: str, api_key: str) -> str:
    """Poll until the document is complete. Returns humanized text."""
    body = {"id": doc_id}
    elapsed = 0

    print("  Waiting for humanization", end="", flush=True)
    while elapsed < POLL_TIMEOUT:
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
        print(".", end="", flush=True)

        data = _post(POLL_URL, body, api_key)
        status = data.get("status", "")

        if status == "complete" or data.get("output"):
            output = data.get("output", "")
            if output:
                print(" done!")
                return output

        if status == "error":
            print()
            print(f"  ERROR  Humanization failed: {json.dumps(data, ensure_ascii=False)[:300]}",
                  file=sys.stderr)
            sys.exit(1)

    print()
    print(f"  ERROR  Timed out after {POLL_TIMEOUT}s", file=sys.stderr)
    sys.exit(1)


def post_process(text: str) -> str:
    """Remove common first-person phrases injected by the API."""
    result = text
    for phrase in FIRST_PERSON_PHRASES:
        # Remove the phrase and any trailing comma/space
        result = re.sub(rf"\s*{re.escape(phrase)}\s*[,،]?\s*", " ", result)
    # Collapse multiple spaces
    result = re.sub(r"  +", " ", result).strip()
    return result


def humanize(text: str, api_key: str) -> str:
    """Full pipeline: submit -> poll -> post-process."""
    doc_id = submit_text(text, api_key)
    raw_output = poll_result(doc_id, api_key)
    cleaned = post_process(raw_output)
    return cleaned


def run_text_mode(text: str, api_key: str, output_path=None) -> None:
    """Humanize raw text from --text or --file."""
    print(f"\n  Input length: {len(text)} chars\n")

    result = humanize(text, api_key)

    print(f"\n  Output length: {len(result)} chars")
    print(f"  ------- Before (first 200 chars) -------")
    print(f"  {text[:200]}...")
    print(f"  ------- After  (first 200 chars) -------")
    print(f"  {result[:200]}...")
    print()

    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"  Saved to: {output_path}\n")
    else:
        print(f"  ------- Full output -------")
        print(result)
        print()


def run_service_mode(service: str, city: str, api_key: str) -> None:
    """Read body content from service page directory, humanize, save back."""
    if service not in SERVICE_CONFIGS:
        print(f"  ERROR  Unknown service '{service}'. Available: {', '.join(SERVICE_CONFIGS.keys())}",
              file=sys.stderr)
        sys.exit(1)

    cfg = SERVICE_CONFIGS[service]
    slug_prefix = cfg["slug_prefix"]

    # Determine the slug directory -- city can be Arabic or English slug
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # html_v2/

    # Try direct match first (Arabic city name as slug)
    slug_dir = os.path.join(base_dir, f"{slug_prefix}-{city}")
    if not os.path.isdir(slug_dir):
        # List matching directories
        candidates = [
            d for d in os.listdir(base_dir)
            if d.startswith(slug_prefix) and os.path.isdir(os.path.join(base_dir, d))
        ]
        print(f"  WARNING  Directory not found: {slug_dir}")
        if candidates:
            print(f"  Available directories: {', '.join(candidates)}")
        sys.exit(1)

    # Look for body content file
    body_file = os.path.join(slug_dir, "body_content.txt")
    if not os.path.isfile(body_file):
        # Try index.html as fallback
        index_file = os.path.join(slug_dir, "index.html")
        if os.path.isfile(index_file):
            print(f"  INFO  No body_content.txt found. Use --file with extracted body text.")
            print(f"  Page directory: {slug_dir}")
            sys.exit(1)
        else:
            print(f"  ERROR  No content files found in {slug_dir}", file=sys.stderr)
            sys.exit(1)

    with open(body_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"  ERROR  body_content.txt is empty", file=sys.stderr)
        sys.exit(1)

    print(f"\n  Service   : {service}")
    print(f"  City      : {city}")
    print(f"  Directory : {slug_dir}")
    print(f"  File      : {body_file}")
    print(f"  Length    : {len(text)} chars\n")

    result = humanize(text, api_key)

    # Save humanized version
    humanized_file = os.path.join(slug_dir, "body_content_humanized.txt")
    with open(humanized_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\n  Output length: {len(result)} chars")
    print(f"  ------- Before (first 200 chars) -------")
    print(f"  {text[:200]}...")
    print(f"  ------- After  (first 200 chars) -------")
    print(f"  {result[:200]}...")
    print(f"\n  Saved to: {humanized_file}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Humanize Arabic text via undetectable.ai API"
    )

    # Input modes (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--text", help="Raw Arabic text to humanize")
    input_group.add_argument("--file", help="Path to text file to humanize")
    input_group.add_argument("--service",
                             help=f"Service key for page mode ({', '.join(SERVICE_CONFIGS.keys())})")

    parser.add_argument("--city", help="City name (required with --service)")
    parser.add_argument("--api-key", required=True, help="undetectable.ai API key")
    parser.add_argument("--output", help="Output file path (for --text or --file mode)")

    args = parser.parse_args()

    # Validate input
    if not args.text and not args.file and not args.service:
        parser.error("One of --text, --file, or --service is required")

    if args.service and not args.city:
        parser.error("--city is required when using --service")

    # Dispatch
    if args.service:
        run_service_mode(args.service, args.city, args.api_key)
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"  ERROR  File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            print(f"  ERROR  File is empty: {args.file}", file=sys.stderr)
            sys.exit(1)
        run_text_mode(text, args.api_key, args.output)
    else:
        run_text_mode(args.text, args.api_key, args.output)


if __name__ == "__main__":
    main()
