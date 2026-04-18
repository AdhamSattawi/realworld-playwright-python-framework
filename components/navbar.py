"""Navbar class to inject it in the base page (composition)"""
from playwright.sync_api import Page

class NavBar:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.container = page.locator(".navbar navbar-light")
        self.conduit = self.container.get_by_role("link", name="conduit", exact=True)
        self.home = self.container.get_by_role("link", name="Home")
        self.new_post = self.container.get_by_role("link", name="New Post")
        self.settings = self.container.get_by_role("link", name="Settings")

    def click_profile(self, username: str) -> None:
        self.container.get_by_role("link", name=username, exact=True).click()

    def select_language(self, language: str = "English") -> None:
        list = self.container.get_by_role("combobox")
        list.select_option(label=language)

    def click_conduit(self) -> None:
        self.conduit.click()

    def click_home(self) -> None:
        self.home.click()

    def click_new_post(self) -> None:
        self.new_post.click()

    def click_settings(self) -> None:
        self.settings.click()