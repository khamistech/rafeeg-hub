# -*- coding: utf-8 -*-
"""
Two-pass Arabic content humanizer for hub.rafeeg.ae pages
Pass 1: Undetectable.ai v11 — breaks AI structural patterns
Pass 2: Claude — restores Gulf MSA dialect, fixes any Egyptian/Levantine markers

Usage:
    python3 humanize.py "your arabic text here"
    python3 humanize.py --file input.txt --out output.txt
"""

import httpx, json, time, sys, os, argparse
import anthropic
from pathlib import Path

# Load .env from same directory as this script
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

UNDETECTABLE_KEY = os.environ.get("UNDETECTABLE_KEY", "02c2b10c-5a39-40c7-b471-7e35ef93802e")
ANTHROPIC_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")

# Egyptian/Levantine → Gulf MSA replacements
DIALECT_FIXES = {
    "تشتغل":  "تعمل",
    "بتشتغل": "تعمل",
    "بيشتغل": "يعمل",
    "اشتغل":  "عمل",
    "لازم":   "يجب",
    "لاز":    "يجب",
    "عشان":   "لكي",
    "عشان ما":"حتى لا",
    "خلّي":   "اجعل",
    "خلي":    "اجعل",
    "مش":     "ليس",
    "مش عارف":"لا أعرف",
    "بس":     "لكن",
    "إيه":    "ماذا",
    "ايه":    "ماذا",
    "إيش":    "ماذا",
    "بدي":    "أريد",
    "بده":    "يريد",
    "بدنا":   "نريد",
    "هيك":    "هكذا",
    "كتير":   "كثير",
    "هلق":    "الآن",
    "هلأ":    "الآن",
    "شو":     "ماذا",
    "وين":    "أين",
    "ليش":    "لماذا",
    "كيفك":   "كيف حالك",
    "تمام":   "جيد",   # keep if used in Gulf context
    "أوكي":   "",      # remove filler
    "أوك":    "",
}


def quick_dialect_fix(text: str) -> str:
    """Fast regex-free replacement of obvious dialect markers."""
    for dialect, msa in DIALECT_FIXES.items():
        text = text.replace(dialect, msa)
    return text


def undetectable_humanize(text: str, model: str = "v11") -> str:
    """Submit to Undetectable.ai and poll for result."""
    r = httpx.post(
        "https://humanize.undetectable.ai/submit",
        headers={"apikey": UNDETECTABLE_KEY, "Content-Type": "application/json"},
        json={
            "content": text,
            "readability": "High School",
            "purpose":     "General Writing",
            "strength":    "More Human",
            "model":       model,
        },
        timeout=20,
    )
    r.raise_for_status()
    doc_id = r.json().get("id")
    if not doc_id:
        print("  [undetectable] No doc ID returned, using original text")
        return text

    print(f"  [undetectable] Submitted ({model}), doc_id={doc_id}")
    for attempt in range(10):
        time.sleep(15)
        r2 = httpx.post(
            "https://humanize.undetectable.ai/document",
            headers={"apikey": UNDETECTABLE_KEY, "Content-Type": "application/json"},
            json={"id": doc_id},
            timeout=20,
        )
        result = r2.json()
        status = result.get("status")
        print(f"  [undetectable] Attempt {attempt+1}: {status}")
        if status == "done":
            output = result.get("output", "").strip()
            return output if output else text

    print("  [undetectable] Timed out, using original text")
    return text


def claude_gulf_msa_restore(text: str) -> str:
    """Claude pass: restore Gulf MSA, remove dialect, keep structure variation."""
    if not ANTHROPIC_KEY:
        print("  [claude] No ANTHROPIC_API_KEY set, skipping Gulf MSA restore")
        return text

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    prompt = f"""أنت مدقق لغوي متخصص في اللهجة الخليجية والعربية الفصحى المعاصرة.

النص التالي كُتب للجمهور الإماراتي وقد أُعيدت صياغته آلياً فأصبح فيه بعض الكلمات بالعامية المصرية أو الشامية. مهمتك:

1. استبدل أي كلمات عامية مصرية أو شامية بمقابلها الفصيح الخليجي (مثل: تشتغل → تعمل، لازم → يجب، عشان → لكي، بس → لكن، مش → ليس)
2. احتفظ بالتنوع في أسلوب الجمل الذي أضافه النص المعاد صياغته — لا تُعد النص إلى صيغته الأصلية الرتيبة
3. تأكد من أن النبرة مناسبة لموقع خدمات منزلية إماراتي — صريح، ودّي، وموثوق
4. أعد فقط النص المصحح بدون شرح أو تعليق

النص:
{text}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def humanize(text: str, skip_undetectable: bool = False) -> str:
    """
    Full two-pass humanization pipeline.
    Pass 1: Undetectable.ai v11 (breaks AI sentence patterns)
    Pass 2: Claude Gulf MSA restore (fixes dialect, keeps variation)
    """
    print(f"\n[humanize] Input: {len(text)} chars")

    if not skip_undetectable:
        print("[humanize] Pass 1: Undetectable.ai v11...")
        text = undetectable_humanize(text, model="v11")
        print(f"[humanize] After v11: {len(text)} chars")
        # Quick dialect fix before Claude
        text = quick_dialect_fix(text)

    print("[humanize] Pass 2: Claude Gulf MSA restore...")
    text = claude_gulf_msa_restore(text)
    print(f"[humanize] Final: {len(text)} chars")

    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Humanize Arabic SEO content")
    parser.add_argument("text", nargs="?", help="Text to humanize")
    parser.add_argument("--file", help="Input file path")
    parser.add_argument("--out",  help="Output file path")
    parser.add_argument("--skip-undetectable", action="store_true",
                        help="Skip Undetectable.ai, only run Claude pass")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            input_text = f.read()
    elif args.text:
        input_text = args.text
    else:
        print("Usage: python3 humanize.py 'text' OR --file input.txt")
        sys.exit(1)

    result = humanize(input_text, skip_undetectable=args.skip_undetectable)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\nSaved to {args.out}")
    else:
        print("\n--- RESULT ---")
        print(result)
