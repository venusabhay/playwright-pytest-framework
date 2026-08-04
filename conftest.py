from pathlib import Path

import pytest
from playwright.sync_api import Error as PlaywrightError, sync_playwright

from config.settings import (ACTION_TIMEOUT, BROWSER_NAME, HEADLESS, SCREENSHOT_DIR,
                              TRACE_DIR, VIDEO_DIR)
from utils.logger import get_logger
from utils.report_embedder import embed_failure_screenshots

LOGGER = get_logger(__name__)


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_context):
    launch_kwargs = {"headless": HEADLESS, "args": ["--disable-dev-shm-usage"]}
    try:
        browser_launcher = getattr(playwright_context, BROWSER_NAME, None)
        if browser_launcher is None:
            raise AttributeError(f"Unsupported browser: {BROWSER_NAME}")
        browser = browser_launcher.launch(**launch_kwargs)
    except Exception as exc:
        pytest.skip(f"Playwright browser could not be launched: {exc}")
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }


@pytest.fixture
def context(browser, browser_context_args, request):
    test_name = request.node.name.replace("/", "_").replace(" ", "_")
    ctx = browser.new_context(
        **browser_context_args,
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1280, "height": 720},
    )
    setattr(request.node, "video_path", str(VIDEO_DIR / f"{test_name}.webm"))
    yield ctx
    ctx.close()


@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()


def _capture_failure_screenshot(request, page, context):
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        screenshot_path = SCREENSHOT_DIR / f"{request.node.name}.png"
        trace_path = TRACE_DIR / f"{request.node.name}.zip"
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            context.tracing.start(path=str(trace_path))
            context.tracing.stop(path=str(trace_path))
            setattr(request.node, "screenshot_path", str(screenshot_path))
            setattr(request.node, "trace_path", str(trace_path))
            LOGGER.warning("Saved failure screenshot: %s", screenshot_path)
            LOGGER.warning("Saved failure trace: %s", trace_path)
        except PlaywrightError as exc:
            LOGGER.warning("Unable to save screenshot: %s", exc)


@pytest.fixture(autouse=True)
def attach_test_artifacts(request, page, context):
    yield
    _capture_failure_screenshot(request, page, context)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and getattr(item, "screenshot_path", None) and rep.failed:
        rep.screenshot_path = item.screenshot_path

    return rep


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    embed_failure_screenshots("reports/pytest_report.html", [])
