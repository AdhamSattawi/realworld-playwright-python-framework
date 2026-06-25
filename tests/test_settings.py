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


def test_update_bio(logged_in_page: Page):
    """Updating the bio field in Settings should persist on the auth user's profile page."""
    new_bio = FAKE.sentence()

    settings = SettingsPage(logged_in_page)
    settings.load()

    # Resolve the current user's username from the profile link in the navbar
    username_link = logged_in_page.locator("nav a[href*='/profile/@']").first
    href = username_link.get_attribute("href")
    username = href.split("@")[-1].rstrip("/")

    settings.update_settings(bio=new_bio)

    # After saving, SettingForm redirects to /profile/@<username>
    logged_in_page.wait_for_load_state("networkidle")

    # Navigate to the user's profile and assert the bio is visible
    profile = ProfilePage(logged_in_page)
    profile.load(username)
    expect(logged_in_page.get_by_text(new_bio)).to_be_visible()


def test_logout(logged_in_page: Page):
    """Clicking the logout button should sign the user out and redirect home."""
    settings = SettingsPage(logged_in_page)
    settings.load()
    settings.logout_btn.click()
    logged_in_page.wait_for_load_state("networkidle")

    # After logout the URL should be the home page (may have locale prefix)
    expect(logged_in_page).to_have_url(re.compile(r"/$"))

    # Authenticated nav links should no longer be visible
    expect(logged_in_page.get_by_role("link", name="New Post")).not_to_be_visible()
