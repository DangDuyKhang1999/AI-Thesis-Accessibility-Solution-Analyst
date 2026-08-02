import subprocess
import sys
from pathlib import Path


def main() -> int:
    root_dir = Path(__file__).resolve().parent
    script = root_dir / "scripts" / "legacy" / "run_happy_case.py"

    if not script.is_file():
        print(f"[ERROR] Script not found: {script}")
        return 1

    # Resolve user-provided relative paths from the documented project root.
    command = [sys.executable, str(script), *sys.argv[1:]]
    result = subprocess.run(command, cwd=root_dir)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
