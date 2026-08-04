import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TESTDATA_DIR = BASE_DIR / "testdata"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

for directory in [SCREENSHOT_DIR, REPORT_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "file://")
CI_ENV = os.getenv("CI", "").lower() in {"1", "true", "yes", "on"}
HEADLESS_ENV = os.getenv("HEADLESS")
HEADLESS = str(HEADLESS_ENV).lower() == "true" if HEADLESS_ENV is not None else CI_ENV
