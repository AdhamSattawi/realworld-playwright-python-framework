from playwright.sync_api import Page
from pages.base_page import BasePage

class ArticlePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Edit Article is a <button> inside a <Link> — match by text
        self.edit_btn = page.get_by_role("button", name="Edit Article").first
        # Delete Article is a <button> with confirm dialog
        self.delete_btn = page.get_by_role("button", name="Delete Article").first
        self.comment_field = page.get_by_placeholder("Write a comment...")
        self.comment_btn = page.get_by_role("button", name="Post Comment")
        # Favorite button — the count lives in <span class="counter">
        self.favorite_btn = page.locator(".article-meta .ion-heart").first
        self.favorite_count = page.locator(".counter").first


    def load(self, title: str) -> None:
        self.navigate(f"/article/{title}")

    def edit(self) -> None:
        """Edit the article"""
        self.edit_btn.click()

    def delete(self) -> None:
        """Delete the article, accepting the confirmation dialog."""
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.delete_btn.click()

    def comment(self, comment: str = "") -> None:
        """Post comment on the article"""
        self.comment_field.fill(comment)
        self.comment_btn.click()

    def get_like_btn(self):
        return self.favorite_btn
