#!/usr/bin/env python3
"""Generate Vietnamese MP3 from text using gTTS.

Usage:
  python generate_gtts_vi.py --in output/description_vi.txt --out output/description_vi_gtts.mp3
"""
import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Vietnamese MP3 from a text file using gTTS")
    parser.add_argument("--in", dest="infile", default="output/description_vi.txt", help="Input text file (utf-8)")
    parser.add_argument("--out", dest="outfile", default="output/description_vi_gtts.mp3", help="Output mp3 file path")
    args = parser.parse_args()

    infile = Path(args.infile)
    outfile = Path(args.outfile)

    if not infile.exists():
        print(f"[ERROR] Input text not found: {infile}")
        return 1

    try:
        from gtts import gTTS
    except Exception as e:
        print("[ERROR] gTTS not installed. Install with: pip install gTTS")
        print(f"[DEBUG] {e}")
        return 2

    text = infile.read_text(encoding="utf-8")
    if not text.strip():
        print("[ERROR] Input text is empty.")
        return 1

    try:
        tts = gTTS(text=text, lang="vi")
        outfile.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(outfile))
        print(f"[OK] Saved: {outfile}")
        return 0
    except Exception as e:
        print(f"[ERROR] gTTS generation failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
