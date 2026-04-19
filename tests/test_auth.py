import pytest
from playwright.sync_api import Page, expect
from pages.sign_in_page import SignInPage
from pages.sign_up_page import SignUpPage

def test_sign_in(page: Page, create_test_user):
    sign_in_page = SignInPage(page)
    sign_in_page.load()
    sign_in_page.sign_in(create_test_user["email"], create_test_user["password"])
    expect(page).to_have_url("/?feed=feed")