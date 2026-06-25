import re
from faker import Faker
from playwright.sync_api import Page, expect
from pages.settings_page import SettingsPage
from pages.profile_page import ProfilePage

FAKE = Faker()


def test_settings_page_loads(logged_in_page: Page):
    """The Settings page should display the 'Your Settings' heading."""
    settings = SettingsPage(logged_in_page)
    settings.load()
    expect(settings.header).to_be_visible()


def test_update_bio(logged_in_page: Page, create_test_user: dict):
    """Updating the bio field in Settings should persist on the profile page."""
    new_bio = FAKE.sentence()

    settings = SettingsPage(logged_in_page)
    settings.load()
    settings.update_settings(bio=new_bio)

    # Navigate to the user's profile and assert the bio is visible
    profile = ProfilePage(logged_in_page)
    profile.load(create_test_user["username"])
    expect(logged_in_page.get_by_text(new_bio)).to_be_visible()


def test_logout(logged_in_page: Page):
    """Clicking the logout button should sign the user out and redirect home."""
    settings = SettingsPage(logged_in_page)
    settings.load()
    settings.logout_btn.click()

    # After logout the URL should be the home page
    expect(logged_in_page).to_have_url(re.compile(r"^.*/$"))

    # 'New Post' and 'Settings' nav links should no longer be visible
    expect(logged_in_page.get_by_role("link", name="New Post")).not_to_be_visible()
