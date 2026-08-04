from __future__ import annotations

from typing import Optional

from playwright.sync_api import Page

from config.settings import SCREENSHOT_DIR
from utils.helpers import take_screenshot


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str, wait_until: str = "load") -> None:
        self.page.goto(url, wait_until=wait_until)

    def wait_for_url(self, url: str, timeout: int = 10000) -> None:
        self.page.wait_for_url(url, timeout=timeout)

    def click(self, selector: str, timeout: int = 10000) -> None:
        self.page.locator(selector).click(timeout=timeout)

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        return self.page.locator(selector).is_visible(timeout=timeout)

    def take_screenshot(self, name: Optional[str] = None) -> str:
        return take_screenshot(self.page, name=name)

    def expect_title(self, title: str) -> None:
        assert self.page.title() == title
