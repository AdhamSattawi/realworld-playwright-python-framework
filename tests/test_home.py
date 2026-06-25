"""Home page smoke tests (logo, tabs visible)."""
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


def test_home_page_loading(page: Page):
    """The Conduit logo should be visible on the public home page."""
    home_page = HomePage(page)
    home_page.load()

    assert home_page.logo.is_visible()


def test_global_feed_tab_visible(page: Page):
    """The Global Feed tab should be visible to unauthenticated users."""
    home_page = HomePage(page)
    home_page.load()
    expect(home_page.global_feed).to_be_visible()