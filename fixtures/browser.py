import pytest
from playwright.sync_api import Error as PlaywrightError


def _browser_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            p.chromium.launch(headless=True)
        return True
    except Exception:
        return False


def pytest_collection_modifyitems(config, items):
    if _browser_available():
        return
    skip_ui = pytest.mark.skip(reason="Playwright browser binary is not available in this environment")
    for item in items:
        if "ui" in item.keywords:
            item.add_marker(skip_ui)


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
        screenshot_path = "screenshots/" + request.node.name + ".png"
        try:
            page.screenshot(path=screenshot_path, full_page=True)
        except PlaywrightError:
            pass
