"""API client helper wrapping Playwright's APIRequestContext for test setup/teardown."""
from playwright.sync_api import APIRequestContext


class APIClient:
    """Thin wrapper around Playwright's APIRequestContext for the RealWorld API."""

    def __init__(self, request: APIRequestContext) -> None:
        self._request = request

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def register_user(self, username: str, email: str, password: str) -> dict:
        """Create a new user. Returns the response JSON."""
        response = self._request.post(
            "/api/users",
            data={"user": {"username": username, "email": email, "password": password}},
        )
        assert response.ok, f"register_user failed: {response.text()}"
        return response.json()

    def login_user(self, email: str, password: str) -> dict:
        """Authenticate an existing user. Returns the response JSON including token."""
        response = self._request.post(
            "/api/users/login",
            data={"user": {"email": email, "password": password}},
        )
        assert response.ok, f"login_user failed: {response.text()}"
        return response.json()

    # ------------------------------------------------------------------
    # Articles
    # ------------------------------------------------------------------

    def create_article(
        self,
        token: str,
        title: str,
        description: str,
        body: str,
        tag_list: list[str] | None = None,
    ) -> dict:
        """Create an article as an authenticated user. Returns the response JSON."""
        response = self._request.post(
            "/api/articles",
            headers={"Authorization": f"Token {token}"},
            data={
                "article": {
                    "title": title,
                    "description": description,
                    "body": body,
                    "tagList": tag_list or [],
                }
            },
        )
        assert response.ok, f"create_article failed: {response.text()}"
        return response.json()

    def delete_article(self, token: str, slug: str) -> None:
        """Delete an article by slug as an authenticated user."""
        response = self._request.delete(
            f"/api/articles/{slug}",
            headers={"Authorization": f"Token {token}"},
        )
        # 404 is acceptable — the test may have already deleted it via UI
        assert response.ok or response.status == 404, (
            f"delete_article failed with status {response.status}: {response.text()}"
        )
