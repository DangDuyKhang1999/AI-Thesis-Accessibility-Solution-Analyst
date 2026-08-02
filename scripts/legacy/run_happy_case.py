import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
def build_prompt() -> str:
    return (
        "Ban la tro ly AI ho tro kha nang tiep can cho nguoi khiem thi trong doanh nghiep.\n"
        "Nhiem vu: Phan tich 1 hinh anh giao dien hoac tai lieu va mo ta BANG TIENG VIET, chi duoc viet van ban thuong, ro rang, de doc.\n\n"
        "Yeu cau xuat:\n"
        "- Hay viet thanh 1 doan van lien tuc, khong danh dau dau dong, khong bullet, khong numbering, khong markdown.\n"
        "- Neu can noi ve nhieu y, hay tach bang cau, khong dung dau gach dau dong.\n"
        "- Khong dung ky tu dac biet nhu *, #, -, >, `, [ ], ( ), : o dau dong.\n"
        "- Khong them tieu de. Khong in ky hieu trang tri.\n\n"
        "Rang buoc:\n"
        "- Chi viet tieng Viet.\n"
        "- Khong suy doan vo can cu.\n"
        "- Neu khong doc duoc mot vung, ghi ro: 'Khong doc ro'.\n"
        "- Van phong gon, de nghe qua TTS.\n"
        "- Dau ra phai la van ban thuong, khong co ky tu lam TTS doc ten ky hieu."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Happy case: 1 image -> Vietnamese description")
    parser.add_argument(
        "--image",
        default="archive/happy-case-mvp/assets/samples/bar.png",
        help=(
            "Path to image file (png/jpg/jpeg/webp). "
            "Default: archive/happy-case-mvp/assets/samples/bar.png"
        ),
    )
    parser.add_argument(
        "--out",
        default="output/description_vi.txt",
        help="Output text file path",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash-lite",
        help="Gemini model name (default: gemini-2.5-flash-lite)",
    )
    # Single flow only: image -> text -> speech
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("[ERROR] Chua co API key hop le.")
        print("[INFO] Dat GEMINI_API_KEY trong file .env o thu muc goc du an.")
        return 1

    image_path = Path(args.image)
    out_path = Path(args.out)

    if not image_path.exists() or not image_path.is_file():
        print(f"[ERROR] Image not found: {image_path}")
        return 1

    client = genai.Client(api_key=api_key)

    try:
        with image_path.open("rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model=args.model,
            contents=[
                build_prompt(),
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=_guess_mime_type(image_path.suffix.lower()),
                ),
            ],
        )
    except Exception as exc:
        err = str(exc)
        if "RESOURCE_EXHAUSTED" in err or "429" in err:
            print("[ERROR] Vuot quota Gemini API (429 RESOURCE_EXHAUSTED).")
            if "limit: 0" in err:
                print("[INFO] Du an/key hien tai dang co quota Free Tier = 0 cho model nay.")
                print("[INFO] Can doi key/project khac co quota, hoac bat billing de dung paid tier.")
            if "retryDelay" in err or "Please retry in" in err:
                print("[INFO] Ban co the doi mot chut roi chay lai lenh.")
            print("[INFO] Thu model khac: --model gemini-2.5-flash hoac --model gemini-2.0-flash-lite")
            return 1

        print(f"[ERROR] Gemini call failed: {exc}")
        return 1

    text = (response.text or "").strip()
    if not text:
        print("[ERROR] Empty response from model.")
        return 1

    text = _clean_plain_text(text)
    # Normalize numeric quantities to Vietnamese magnitude words to avoid digit-by-digit TTS
    text = _normalize_numbers_to_vn(text)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    print("[OK] Generated Vietnamese description.")
    print(f"[OK] Saved to: {out_path}")
    # Single-step TTS: always call Hugging Face Inference TTS and save audio
    try:
        import requests
        import base64

        tts_model = "suno/bark"
        tts_output = Path("output/description_vi_hf.mp3")
        hf_token = os.getenv("HF_TOKEN", "").strip()
        if not hf_token:
            print("[ERROR] No HF_TOKEN available for TTS. Aborting audio generation.")
            return 1

        url = f"https://api-inference.huggingface.co/models/{tts_model}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {"inputs": text}
        resp = requests.post(url, headers=headers, json=payload, timeout=120, stream=True)
        if resp.status_code != 200:
            print(f"[ERROR] HF TTS failed: status {resp.status_code}")
            try:
                print(resp.json())
            except Exception:
                print(resp.text[:1000])
            return 1

        ctype = resp.headers.get("content-type", "")
        audio_bytes = None
        if "audio" in ctype or ctype in ("application/octet-stream",):
            audio_bytes = resp.content
        else:
            j = resp.json()
            # try common base64 locations
            def _try_extract(obj):
                if isinstance(obj, dict):
                    for k in ("audio","data","mp3","wav","sound"):
                        v = obj.get(k)
                        if isinstance(v, str):
                            s = v
                            if s.startswith("data:") and ";base64," in s:
                                return base64.b64decode(s.split(";base64,",1)[1])
                            try:
                                return base64.b64decode(s)
                            except Exception:
                                pass
                    for v in obj.values():
                        res = _try_extract(v)
                        if res:
                            return res
                if isinstance(obj, list):
                    for item in obj:
                        res = _try_extract(item)
                        if res:
                            return res
                return None
            audio_bytes = _try_extract(j)

        if not audio_bytes:
            print("[ERROR] Could not extract audio from HF response.")
            return 1

        tts_output.parent.mkdir(parents=True, exist_ok=True)
        tts_output.write_bytes(audio_bytes)
        print(f"[OK] Saved audio to: {tts_output}")
    except Exception as exc:
        err_str = str(exc)
        print(f"[ERROR] TTS step failed: {err_str}")
        # If network/DNS resolution error, attempt a local Vietnamese voice first,
        # otherwise fall back to gTTS so we do not emit English audio.
        if ("Failed to resolve" in err_str) or ("getaddrinfo" in err_str) or ("NameResolution" in err_str) or ("Max retries exceeded" in err_str):
            print("[INFO] Detected network/DNS error contacting HF Inference — trying Vietnamese local voice first, then gTTS.")
            try:
                def _pyttsx3_fallback(text: str, out_path: Path) -> bool:
                    try:
                        import pyttsx3
                    except Exception:
                        print("[WARN] pyttsx3 not installed.")
                        return False
                    try:
                        engine = pyttsx3.init()
                        voices = engine.getProperty("voices") or []
                        vi_voice = None
                        for v in voices:
                            attrs = " ".join([str(getattr(v, a, "")) for a in ("id", "name", "languages")]).lower()
                            if "vietnam" in attrs or "vietnamese" in attrs or " vi" in attrs or "vi-" in attrs:
                                vi_voice = v
                                break

                        if vi_voice is None:
                            print("[INFO] No Vietnamese local voice found for pyttsx3.")
                            return False

                        engine.setProperty("voice", vi_voice.id)
                        print(f"[INFO] Using local Vietnamese voice: {getattr(vi_voice, 'name', vi_voice.id)}")

                        # save_to_file will write an audio file (typically WAV on Windows)
                        engine.save_to_file(text, str(out_path))
                        engine.runAndWait()
                        return True
                    except Exception as e2:
                        print(f"[WARN] pyttsx3 Vietnamese voice failed: {e2}")
                        return False

                def _gtts_fallback(text: str, out_path: Path) -> bool:
                    try:
                        from gtts import gTTS
                    except Exception:
                        print("[ERROR] gTTS not installed. Install with: pip install gTTS")
                        return False
                    try:
                        mp3_out = out_path.with_suffix(".mp3")
                        gTTS(text=text, lang="vi").save(str(mp3_out))
                        print(f"[OK] Saved Vietnamese gTTS audio to: {mp3_out}")
                        return True
                    except Exception as e:
                        print(f"[ERROR] gTTS failed: {e}")
                        return False

                local_out = Path("output/description_vi_local.wav")
                local_out.parent.mkdir(parents=True, exist_ok=True)
                if _pyttsx3_fallback(text, local_out):
                    print(f"[OK] Saved local fallback TTS to: {local_out}")
                    return 0

                print("[INFO] Falling back to gTTS Vietnamese MP3.")
                if _gtts_fallback(text, Path("output/description_vi_local.mp3")):
                    return 0

                print("[ERROR] Vietnamese fallback TTS also failed.")
                return 1
            except Exception as e3:
                print(f"[ERROR] Fallback attempt failed: {e3}")
                return 1
        return 1
    return 0


def _guess_mime_type(ext: str) -> str:
    if ext == ".png":
        return "image/png"
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".webp":
        return "image/webp"
    return "application/octet-stream"


def _clean_plain_text(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        while line.startswith(("- ", "* ", "> ", "# ")):
            line = line[2:].lstrip()
        if len(line) > 2 and line[0].isdigit() and line[1] in {".", ")"}:
            line = line[2:].lstrip()
        lines.append(line)

    cleaned = " ".join(lines)
    for ch in ("*", "#", "`", "[", "]"):
        cleaned = cleaned.replace(ch, "")
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")
    return cleaned.strip()


def _normalize_numbers_to_vn(text: str) -> str:
    import re

    def _replace(match: re.Match) -> str:
        s = match.group(0)
        # remove grouping commas/spaces
        s_clean = s.replace(" ", "").replace(",", "")
        try:
            if "." in s_clean:
                val = float(s_clean)
            else:
                val = int(s_clean)
        except Exception:
            return s

        unit = None
        scaled = None
        if val >= 1_000_000_000:
            scaled = val / 1_000_000_000
            unit = "tỷ"
        elif val >= 1_000_000:
            scaled = val / 1_000_000
            unit = "triệu"
        elif val >= 1_000:
            scaled = val / 1_000
            unit = "nghìn"

        if unit is None:
            return s

        # show integer when exact, otherwise one decimal place
        if abs(scaled - round(scaled)) < 1e-9:
            out = f"{int(round(scaled))} {unit}"
        else:
            out = f"{scaled:.1f} {unit}"
            # strip trailing .0
            out = out.replace(".0 ", " ")
        return out

    # match numbers with optional grouping (commas/dots/spaces) and optional decimal part
    pattern = re.compile(r"(?<!\d)(\d{1,3}(?:[., ]\d{3})*(?:[.,]\d+)?)(?!\d)")
    return pattern.sub(_replace, text)


if __name__ == "__main__":
    raise SystemExit(main())
