import pytest
import re
from playwright.sync_api import Page, expect
from pages.sign_in_page import SignInPage
from pages.sign_up_page import SignUpPage
from utils.file_load import load_user_data

def test_sign_in(page: Page, create_test_user):
    sign_in_page = SignInPage(page)
    sign_in_page.load()
    sign_in_page.sign_in(create_test_user["email"], create_test_user["password"])
    expect(page).to_have_url("/?feed=feed")

LOGIN_SCENARIOS = load_user_data("data/user_login.json")

@pytest.mark.parametrize("data", LOGIN_SCENARIOS, ids= lambda d :d["scenario"])
def test_negative_logins(page: Page, data: dict):
    sign_in_page = SignInPage(page)
    sign_in_page.load()
    sign_in_page.sign_in(data["email"], data["password"])
    expect(page).to_have_url(re.compile(r"/login/error"))
    expect(page.get_by_text("This page could not be found.")).to_be_visible()
    home_btn = page.get_by_role("button", name="Return Home")
    expect(home_btn).to_be_visible()
    home_btn.click()
    expect(page).to_have_url(re.compile(r"/"))
