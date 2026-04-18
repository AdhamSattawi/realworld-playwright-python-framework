from playwright.sync_api import Page
from pages.base_page import BasePage

class ProfilePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.edit_profile_btn = page.get_by_role("button", name="Edit Profile Settings")
        self.my_articles = page.get_by_role("link", name="My Articles")
        self.fav_articles = page.get_by_role("link", name="Favorited Articles")
        self.heart_btn = page.locator(".ion-heart")


    def load(self, username: str) -> None:
        self.navigate(f"/profile/@{username}")

    def edit(self) -> None:
        """Edit the profile (go to settings page)"""
        self.edit_profile_btn.click()

    def goto_my_articles(self) -> None:
        """Show user articles"""
        self.my_articles.click()

    def goto_fav_articles(self) -> None:
        """Show favourite articles"""
        self.fav_articles.click()

