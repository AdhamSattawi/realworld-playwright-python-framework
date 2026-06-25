import re
from faker import Faker
from playwright.sync_api import Page, expect
from pages.editor_page import EditorPage
from pages.article_page import ArticlePage

FAKE = Faker()


def test_create_article(logged_in_page: Page):
    """An authenticated user can create and publish a new article."""
    title = FAKE.sentence(nb_words=4).rstrip(".")
    description = FAKE.sentence()
    body = FAKE.paragraph()
    tag = "automation"

    editor = EditorPage(logged_in_page)
    editor.load()
    editor.new_post(title=title, description=description, article=body, tags=tag)

    # After publishing, the app redirects to the article detail page
    expect(logged_in_page).to_have_url(re.compile(r"/article/"))
    expect(logged_in_page.get_by_role("heading", name=title)).to_be_visible()


def test_edit_article(logged_in_page: Page, create_article: dict):
    """An authenticated user can edit the title of an existing article."""
    article_page = ArticlePage(logged_in_page)
    article_page.load(create_article["slug"])

    article_page.edit()
    expect(logged_in_page).to_have_url(re.compile(r"/editor/"))

    # Update the title in the editor
    new_title = FAKE.sentence(nb_words=3).rstrip(".")
    title_field = logged_in_page.get_by_placeholder("Article Title")
    title_field.fill(new_title)
    logged_in_page.get_by_role("button", name="Publish Article").click()

    # Redirect back to article page with the new title visible
    expect(logged_in_page).to_have_url(re.compile(r"/article/"))
    expect(logged_in_page.get_by_role("heading", name=new_title)).to_be_visible()


def test_delete_article(logged_in_page: Page, create_article: dict):
    """An authenticated user can delete their own article (accepts confirm dialog)."""
    article_page = ArticlePage(logged_in_page)
    article_page.load(create_article["slug"])

    article_page.delete()  # handles window.confirm() internally

    # After deletion the app redirects away from the article page
    expect(logged_in_page).not_to_have_url(re.compile(r"/article/"))


def test_add_comment(logged_in_page: Page, create_article: dict):
    """An authenticated user can post a comment on an article."""
    comment_text = FAKE.sentence()

    article_page = ArticlePage(logged_in_page)
    article_page.load(create_article["slug"])
    article_page.comment(comment_text)

    # The comment should appear in the comment list below
    expect(logged_in_page.get_by_text(comment_text)).to_be_visible()


def test_favorite_article(logged_in_page: Page):
    """A user can favourite an article they did not write.

    The FavoriteButton (with .ion-heart) is only rendered for non-authors.
    We navigate to the global feed and favourite the first article there.
    """
    logged_in_page.goto("/")
    logged_in_page.wait_for_load_state("networkidle")

    # Click Global Feed to ensure articles are listed
    logged_in_page.get_by_role("link", name="Global Feed").click()
    logged_in_page.wait_for_load_state("networkidle")

    # The favourite buttons in the feed are FavoriteButton components
    first_fav_btn = logged_in_page.locator(".article-preview .ion-heart").first
    expect(first_fav_btn).to_be_visible()

    # Read the current count from the sibling text node
    before_count_text = logged_in_page.locator(
        ".article-preview button.btn-outline-primary"
    ).first.inner_text()

    first_fav_btn.click()

    # After favouriting the button should switch to btn-primary (filled)
    expect(
        logged_in_page.locator(".article-preview button.btn-primary").first
    ).to_be_visible()
