from pages.home_page import HomePage
from playwright.sync_api import Page

def test_home_page_loading(page: Page):
    home_page = HomePage(page)
    home_page.load()

    assert home_page.logo.is_visible()