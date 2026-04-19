from playwright.sync_api import Page
from pages.base_page import BasePage

class SignInPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_header = page.get_by_role("heading", name="Sign in")
        self.register_link = page.get_by_role("link", name="Need an account?")
        self.email_input = page.get_by_test_id("input-email")
        self.pass_input = page.get_by_test_id("input-password")
        self.submit_btn = page.get_by_test_id("btn-submit")

    def load(self) -> None:
        self.navigate("/login")

    def goto_sign_up(self) -> None:
        """Go to new account registeration page"""
        self.register_link.click()

    def sign_in(self, email: str, password: str) -> None:
        """Fill and submit the sign in form"""
        self.email_input.fill(email)
        self.pass_input.fill(password)
        self.submit_btn.click()
