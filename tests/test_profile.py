from playwright.sync_api import Page, expect
from pages.profile_page import ProfilePage
from pages.settings_page import SettingsPage


def test_profile_page_loads(logged_in_page: Page, create_test_user: dict):
    """Navigating to the user's own profile should display their username."""
    profile = ProfilePage(logged_in_page)
    profile.load(create_test_user["username"])

    # The profile username heading should be visible
    expect(logged_in_page.get_by_role("heading", name=create_test_user["username"])).to_be_visible()


def test_edit_profile_button_navigates_to_settings(logged_in_page: Page, create_test_user: dict):
    """Clicking 'Edit Profile Settings' on the profile page navigates to /settings."""
    profile = ProfilePage(logged_in_page)
    profile.load(create_test_user["username"])
    profile.edit()

    settings = SettingsPage(logged_in_page)
    expect(settings.header).to_be_visible()


def test_my_articles_tab(logged_in_page: Page, create_test_user: dict, create_article: dict):
    """The 'My Articles' tab on the profile page should list the user's articles."""
    profile = ProfilePage(logged_in_page)
    profile.load(create_test_user["username"])
    profile.goto_my_articles()

    # The article created by the fixture should appear in the list
    expect(logged_in_page.get_by_text(create_article["title"])).to_be_visible()


def test_favorited_articles_tab(logged_in_page: Page, create_test_user: dict):
    """Clicking 'Favorited Articles' should switch to that tab without error."""
    profile = ProfilePage(logged_in_page)
    profile.load(create_test_user["username"])
    profile.goto_fav_articles()

    # The tab link itself should now be active / visible
    expect(logged_in_page.get_by_role("link", name="Favorited Articles")).to_be_visible()
