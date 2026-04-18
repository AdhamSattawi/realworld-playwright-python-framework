from playwright.sync_api import Page
from pages.base_page import BasePage

class ArticlePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def load(self, title: str) -> None:
        self.navigate(f"/article/{title}")