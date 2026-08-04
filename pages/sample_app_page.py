from core.base_page import BasePage
from locators.sample_app_locators import SampleAppLocators


class SampleAppPage(BasePage):
    def open(self) -> None:
        self.goto("file://" + str(__import__('pathlib').Path(__file__).resolve().parents[1] / "testdata" / "sample_app.html"))

    def enter_name(self, name: str) -> None:
        self.fill(SampleAppLocators.NAME_INPUT, name)

    def submit(self) -> None:
        self.click(SampleAppLocators.SUBMIT_BUTTON)

    def message(self) -> str:
        return self.get_text(SampleAppLocators.MESSAGE)
