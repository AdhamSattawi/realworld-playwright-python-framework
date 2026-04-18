from playwright.sync_api import Page
from components.navbar import NavBar

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.navbar = NavBar(page)

    def navigate(self, url):
        self.page.goto(url)
