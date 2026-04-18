from playwright.sync_api import Page
from pages.base_page import BasePage

class SignUpPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_header = page.get_by_role("heading", name="Sign up")
        self.register_link = page.get_by_role("link", name="Have an account?")
        self.username_input = page.get_by_test_id("input-username")
        self.email_input = page.get_by_test_id("input-email")
        self.pass_input = page.get_by_test_id("input-password")
        self.submit_btn = page.get_by_test_id("submit-btn")

    def load(self) -> None:
        self.navigate("http://localhost:3000/register")

    def goto_sign_in(self) -> None:
        """Go to account login page"""
        self.register_link.click()

    def sign_up(self, username: str, email: str, password: str) -> None:
        """Fill and submit the sign up form"""
        self.username_input.fill(username)
        self.email_input.fill(email)
        self.pass_input.fill(password)
        self.submit_btn.click()
