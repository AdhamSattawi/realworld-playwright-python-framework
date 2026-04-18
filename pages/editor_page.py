from playwright.sync_api import Page
from pages.base_page import BasePage

class EditorPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.publish_btn = page.get_by_role("button", name="Publish Article")
        self.tags = page.get_by_placeholder("Enter tags")
        self.article = page.get_by_placeholder("Write your article (in markdown)")
        self.title = page.get_by_placeholder("Article Title")
        self.description = page.get_by_placeholder("What's this article about?")

    def load(self) -> None:
        self.navigate("http://localhost:3000/editor")

    def new_post(self, title: str = "", 
                 description: str = "",
                 article: str = "",
                 tags: str = "") -> None:
        """Create & publish new post."""
        self.title.fill(title)
        self.description.fill(description)
        self.article.fill(article)
        self.tags.fill(tags)
        self.publish_btn.click()