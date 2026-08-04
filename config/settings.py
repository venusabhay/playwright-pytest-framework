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
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
