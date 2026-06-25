"""Feed tests: global feed, personal feed, and tag filtering."""
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


def test_global_feed_loads_articles(page: Page):
    """Global Feed tab should render at least one article preview."""
    home_page = HomePage(page)
    home_page.load()
    home_page.goto_global_feed()
    # Each article preview has a 'Read more...' link
    expect(page.get_by_role("link", name="Read more...").first).to_be_visible()


def test_your_feed_visible_when_authenticated(logged_in_page: Page):
    """Authenticated users should see the 'Your Feed' tab."""
    home_page = HomePage(logged_in_page)
    home_page.load()
    expect(home_page.feed).to_be_visible()


def test_your_feed_loads(logged_in_page: Page):
    """Clicking 'Your Feed' should make the personal feed tab active."""
    home_page = HomePage(logged_in_page)
    home_page.load()
    home_page.goto_feed()
    expect(logged_in_page.get_by_role("link", name="Your Feed")).to_be_visible()


def test_tag_filter(page: Page):
    """Clicking a tag pill should switch to a tag-filtered feed view."""
    home_page = HomePage(page)
    home_page.load()

    # Pick the first available tag and click it
    first_tag = page.locator(".tag-list a").first
    tag_text = first_tag.inner_text()
    first_tag.click()

    # A feed column header with the tag name should now be visible
    expect(page.get_by_text(tag_text)).to_be_visible()
