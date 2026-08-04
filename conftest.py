import pytest
from playwright.sync_api import Error as PlaywrightError, sync_playwright

from config.settings import SCREENSHOT_DIR
from utils.logger import get_logger

LOGGER = get_logger(__name__)


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_context):
    try:
        browser = playwright_context.chromium.launch(headless=True)
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
def context(browser, browser_context_args):
    ctx = browser.new_context(**browser_context_args)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(autouse=True)
def attach_test_artifacts(request, page):
    yield
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        screenshot_path = SCREENSHOT_DIR / f"{request.node.name}.png"
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            LOGGER.warning("Saved failure screenshot: %s", screenshot_path)
        except PlaywrightError as exc:
            LOGGER.warning("Unable to save screenshot: %s", exc)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep
