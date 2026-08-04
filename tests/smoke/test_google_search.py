import pytest

from pages.sample_app_page import SampleAppPage


@pytest.mark.smoke
@pytest.mark.ui
def test_google_search(page):
    sample_page = SampleAppPage(page)
    sample_page.open()
    sample_page.enter_name("Playwright")
    sample_page.submit()
    assert sample_page.message() == "Hello, Playwright!"
