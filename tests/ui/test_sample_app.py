import pytest

from pages.sample_app_page import SampleAppPage


@pytest.mark.ui
def test_sample_app_form(page):
    sample_page = SampleAppPage(page)
    sample_page.open()
    sample_page.enter_name("Ava")
    sample_page.submit()
    assert sample_page.message() == "Hello, Ava!"
