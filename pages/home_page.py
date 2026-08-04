from playwright.sync_api import expect

from core.base_page import BasePage
from locators.home_page_locators import HomePageLocators


class HomePage(BasePage):
    def open(self) -> None:
        self.goto("https://www.google.com", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def search(self, query: str) -> None:
        self.page.locator(HomePageLocators.SEARCH_BOX).wait_for(state="visible", timeout=15000)
        self.fill(HomePageLocators.SEARCH_BOX, query)
        self.page.keyboard.press("Enter")

    def results_visible(self) -> bool:
        return self.page.locator(HomePageLocators.RESULTS).is_visible(timeout=10000)
