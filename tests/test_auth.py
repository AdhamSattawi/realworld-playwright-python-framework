import pytest
import re
from playwright.sync_api import Page, expect
from pages.sign_in_page import SignInPage
from pages.sign_up_page import SignUpPage
from utils.file_load import load_user_data

# ---------------------------------------------------------------------------
# Sign-In Tests
# ---------------------------------------------------------------------------

def test_sign_in(page: Page, create_test_user):
    """Happy-path sign-in with a freshly-created user."""
    sign_in_page = SignInPage(page)
    sign_in_page.load()
    sign_in_page.sign_in(create_test_user["email"], create_test_user["password"])
    expect(page).to_have_url("/?feed=feed")


LOGIN_SCENARIOS = load_user_data("data/user_login.json")

@pytest.mark.parametrize("data", LOGIN_SCENARIOS, ids=lambda d: d["scenario"])
def test_negative_logins(page: Page, data: dict):
    """Negative login scenarios should redirect to the NextAuth error page."""
    sign_in_page = SignInPage(page)
    sign_in_page.load()
    sign_in_page.sign_in(data["email"], data["password"])
    expect(page).to_have_url(re.compile(r"/login/error"))
    expect(page.get_by_text("This page could not be found.")).to_be_visible()
    home_btn = page.get_by_role("button", name="Return Home")
    expect(home_btn).to_be_visible()
    home_btn.click()
    expect(page).to_have_url(re.compile(r"/"))


def test_sign_up_link_from_sign_in(page: Page):
    """Clicking 'Need an account?' on the sign-in page navigates to /register."""
    sign_in_page = SignInPage(page)
    sign_in_page.load()
    sign_in_page.goto_sign_up()
    expect(page).to_have_url(re.compile(r"/register"))


# ---------------------------------------------------------------------------
# Sign-Up Tests
# ---------------------------------------------------------------------------

def test_sign_up(page: Page):
    """Happy-path registration: a new random user should land on the feed."""
    from faker import Faker
    fake = Faker()
    sign_up_page = SignUpPage(page)
    sign_up_page.load()
    sign_up_page.sign_up(
        username=fake.user_name(),
        email=fake.email(),
        password="ValidPassword123!",
    )
    expect(page).to_have_url(re.compile(r"/"))


def test_sign_in_link_from_sign_up(page: Page):
    """Clicking 'Have an account?' on the sign-up page navigates to /login."""
    sign_up_page = SignUpPage(page)
    sign_up_page.load()
    sign_up_page.goto_sign_in()
    expect(page).to_have_url(re.compile(r"/login"))


SIGNUP_SCENARIOS = load_user_data("data/test_users.json")

@pytest.mark.parametrize("data", SIGNUP_SCENARIOS, ids=lambda d: d["scenario"])
def test_negative_sign_ups(page: Page, data: dict):
    """Negative sign-up scenarios should stay on /register and not proceed."""
    sign_up_page = SignUpPage(page)
    sign_up_page.load()
    sign_up_page.sign_up(data["username"], data["email"], data["password"])
    # Should not successfully navigate away to the feed
    expect(page).not_to_have_url(re.compile(r"/\?feed=feed"))
