import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def main() -> int:
    app_path = PROJECT_ROOT / "archive" / "happy-case-mvp" / "streamlit_app.py"

    if not app_path.is_file():
        print(f"[ERROR] Streamlit app not found: {app_path}")
        return 1

    command = [sys.executable, "-m", "streamlit", "run", str(app_path), *sys.argv[1:]]
    result = subprocess.run(command, cwd=PROJECT_ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
