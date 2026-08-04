import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TESTDATA_DIR = BASE_DIR / "testdata"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
TRACE_DIR = BASE_DIR / "traces"
VIDEO_DIR = BASE_DIR / "videos"
ENV_DIR = BASE_DIR / "config" / "environments"

for directory in [SCREENSHOT_DIR, REPORT_DIR, LOG_DIR, TRACE_DIR, VIDEO_DIR, ENV_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

CI_ENV = os.getenv("CI", "").lower() in {"1", "true", "yes", "on"}
HEADLESS_ENV = os.getenv("HEADLESS")
HEADLESS = str(HEADLESS_ENV).lower() == "true" if HEADLESS_ENV is not None else CI_ENV

BASE_URL = os.getenv("BASE_URL", "file://")
BROWSER_NAME = os.getenv("BROWSER", "chromium").lower()
ACTION_TIMEOUT = int(os.getenv("ACTION_TIMEOUT", "10000"))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "0"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")


def load_environment_config(environment_name: str | None = None) -> dict:
    env_name = environment_name or ENVIRONMENT
    config_path = ENV_DIR / f"{env_name}.json"
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


ENV_CONFIG = load_environment_config()
