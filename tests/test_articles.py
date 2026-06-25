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
    """An authenticated user can delete their own article."""
    article_page = ArticlePage(logged_in_page)
    article_page.load(create_article["slug"])

    article_page.delete()

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


def test_favorite_article(logged_in_page: Page, create_article: dict):
    """Clicking the heart button on an article increments the favourite count."""
    article_page = ArticlePage(logged_in_page)
    article_page.load(create_article["slug"])

    like_btn = article_page.get_like_btn()
    expect(like_btn).to_be_visible()
    like_btn.click()

    # After favouriting, the button count should be 1 (was 0)
    expect(logged_in_page.locator(".favorites-count")).to_have_text(re.compile(r"[1-9]"))
