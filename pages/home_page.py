from pages.base_page import BasePage
from playwright.sync_api import Page

class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.logo = page.locator(".navbar-brand")

    def load(self) -> None:
        self.navigate("http://localhost:3000")
