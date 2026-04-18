from playwright.sync_api import Page
from pages.base_page import BasePage

class SettingsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.get_by_role("heading", name="Your Settings")
        self.logout_btn = page.get_by_role("button", name="Or click here to logout.")
        self.profile_pic_url = page.get_by_placeholder("URL of profile picture")
        self.name = page.get_by_placeholder("Your Name")
        self.bio = page.get_by_placeholder("Short bio about you")
        self.email = page.get_by_placeholder("Email")
        self.password = page.get_by_placeholder("Password")
        self.submit_btn = page.get_by_role("button", name="Update Settings")

    def load(self) -> None:
        self.navigate("/settings")

    def update_settings(self, 
                        profile_pic_url: str | None = None,
                        name: str| None = None, 
                        bio: str| None = None,
                        email: str| None = None, 
                        password: str| None = None) -> None:
        """Updates user settings."""
        if profile_pic_url is not None:
            self.profile_pic_url.fill(profile_pic_url)
        if name is not None:
            self.name.fill(name)
        if bio is not None:
            self.bio.fill(bio)
        if email is not None:
            self.email.fill(email)
        if password is not None:
            self.password.fill(password)
        self.submit_btn.click()