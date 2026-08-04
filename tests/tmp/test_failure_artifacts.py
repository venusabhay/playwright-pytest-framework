import pytest
from pages.sample_app_page import SampleAppPage

def test_failure_artifact(page):
    sample_page = SampleAppPage(page)
    sample_page.open()
    sample_page.enter_name("Ava")
    sample_page.submit()
    assert sample_page.message() == "Wrong message"
