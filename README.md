# AI Thesis Accessibility Solution Analyst

Streamlit app for a single flow:

upload image -> generate Vietnamese plain-text description -> play audio directly in the browser.

## Files

- `streamlit_app.py`: the web UI MVP.
- `docs/`: specification, roadmap, progress snapshot, and research references.
- `assets/samples/`: sample dashboard images.
- `scripts/legacy/`: preserved CLI and standalone TTS experiments.
- `tests/`: repository-level safety and structure checks.

## Run

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Mở .env và điền GEMINI_API_KEY; HF_TOKEN có thể để trống.
streamlit run streamlit_app.py
```

Create `.env` from `.env.example` and put the real values there. The application
loads this file automatically. `.env` and the local backup directory are ignored
by Git; never put real credentials in `.env.example` or source code.

See `docs/index.md` for the documentation index and `docs/process.md` for the
current progress estimate, detailed setup, test command, and legacy CLI usage.

## Behavior

- No output text file is required for the web flow.
- If Hugging Face inference is unavailable, the app falls back to a Vietnamese local voice when available, then to `gTTS`.
