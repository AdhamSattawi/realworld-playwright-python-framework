from playwright.sync_api import Page
from pages.base_page import BasePage

class ArticlePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.edit_btn = page.get_by_role("button", name="Edit Article")
        self.delete_btn = page.get_by_role("button", name="Delete Article")
        self.comment_field = page.get_by_placeholder("Write a comment...")
        self.comment_btn = page.get_by_role("button", name="Post Comment")

    def load(self, title: str) -> None:
        self.navigate(f"/article/{title}")

    def edit(self) -> None:
        """Edit the article"""
        self.edit_btn.click()

    def delete(self) -> None:
        """Delete the article"""
        self.delete_btn.click()

    def comment(self, comment: str = "") -> None:
        """Post comment on the article"""
        self.comment_field.fill(comment)
        self.comment_btn.click()
