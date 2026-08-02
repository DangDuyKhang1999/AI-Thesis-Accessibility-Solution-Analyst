#!/usr/bin/env python3
"""Call Hugging Face Inference API to convert text -> speech and save audio file.

Usage:
  python hf_inference_tts.py --model <model-id> [--input file] [--output file]

Requires: set environment variable HF_TOKEN or pass --token
"""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from typing import Any

import requests


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Hugging Face Inference TTS")
    p.add_argument("--model", default="suno/bark", help="Hugging Face model id (e.g. suno/bark)")
    p.add_argument("--input", default="output/description_vi.txt", help="Input text file")
    p.add_argument("--output", default="output/description_vi_hf.mp3", help="Output audio file")
    p.add_argument("--token", default=None, help="Hugging Face token or set HF_TOKEN env var")
    p.add_argument("--timeout", type=int, default=120, help="Request timeout seconds")
    return p.parse_args()


def save_bytes(content: bytes, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        f.write(content)


def try_extract_audio_from_json(obj: Any) -> bytes | None:
    # Common patterns: {'audio': '<base64>'} or {'data': '<base64>'} or {'mp3': '<base64>'}
    if isinstance(obj, dict):
        for key in ("audio", "data", "mp3", "wav", "sound"):
            if key in obj and isinstance(obj[key], str):
                s = obj[key]
                # If it's a data URL like data:audio/mpeg;base64,AAA...
                if s.startswith("data:") and ";base64," in s:
                    return base64.b64decode(s.split(";base64,", 1)[1])
                # If it's raw base64
                try:
                    return base64.b64decode(s)
                except Exception:
                    pass
        # Some APIs return nested structures
        for v in obj.values():
            res = try_extract_audio_from_json(v)
            if res:
                return res
    if isinstance(obj, list):
        for item in obj:
            res = try_extract_audio_from_json(item)
            if res:
                return res
    return None


def main() -> int:
    args = parse_args()
    token = args.token or os.getenv("HF_TOKEN")
    if not token:
        print("[ERROR] HF_TOKEN not set and --token not provided.")
        print("Set environment variable HF_TOKEN or pass --token.")
        return 2

    text_path = Path(args.input)
    if not text_path.exists():
        print(f"[ERROR] Input text not found: {text_path}")
        return 3

    text = text_path.read_text(encoding="utf-8").strip()
    if not text:
        print("[ERROR] Input text is empty.")
        return 4

    url = f"https://api-inference.huggingface.co/models/{args.model}"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"inputs": text}
    print(f"Calling HF Inference API model={args.model} ...")
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=args.timeout, stream=True)
    except Exception as exc:
        print("[ERROR] Request failed:", exc)
        return 5

    if resp.status_code != 200:
        print(f"[ERROR] HF API returned status {resp.status_code}")
        # try to print message
        try:
            print(resp.json())
        except Exception:
            print(resp.text[:1000])
        return 6

    ctype = resp.headers.get("content-type", "")
    out_path = Path(args.output)

    if "audio" in ctype or ctype in ("application/octet-stream", "application/vnd.apple.mpegurl"):
        save_bytes(resp.content, out_path)
        print(f"[OK] Saved audio to: {out_path}")
        return 0

    # If response is JSON, try extract base64 audio
    try:
        j = resp.json()
    except Exception:
        print("[ERROR] Unexpected response content-type and failed to parse JSON.")
        return 7

    audio_bytes = try_extract_audio_from_json(j)
    if audio_bytes:
        save_bytes(audio_bytes, out_path)
        print(f"[OK] Saved audio to: {out_path}")
        return 0

    print("[ERROR] Could not extract audio from HF response. Response JSON preview:")
    print(json.dumps(j)[:2000])
    return 8


if __name__ == "__main__":
    raise SystemExit(main())
