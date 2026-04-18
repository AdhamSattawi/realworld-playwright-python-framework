from pages.base_page import BasePage
from playwright.sync_api import Page

class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.logo = page.locator(".navbar-brand")
        self.feed = page.get_by_role("link", name="Your Feed")
        self.global_feed = page.get_by_role("link", name="Global Feed")

    def load(self) -> None:
        self.navigate("/")

    def goto_feed(self) -> None:
        self.feed.click()

    def goto_global_feed(self) -> None:
        self.global_feed.click()
