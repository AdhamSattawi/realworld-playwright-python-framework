"""API client helper wrapping Playwright's APIRequestContext for test setup/teardown."""
from playwright.sync_api import APIRequestContext


class APIClient:
    """Thin wrapper around Playwright's APIRequestContext for the RealWorld API."""

    def __init__(self, request: APIRequestContext) -> None:
        self._request = request

    def _auth_headers(self, token: str | None) -> dict:
        """Return an Authorization header dict, or empty dict if no token given.

        When using cookie-based auth (NextAuth), pass token=None and set the
        Cookie header on the APIRequestContext itself instead.
        """
        if token:
            return {"Authorization": f"Token {token}"}
        return {}

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
        title: str,
        description: str,
        body: str,
        tag_list: list[str] | None = None,
        token: str | None = None,
    ) -> dict:
        """Create an article. Pass token for JWT auth, or rely on cookie header
        set on the underlying APIRequestContext for session-based auth.
        Returns the response JSON.
        """
        response = self._request.post(
            "/api/articles",
            headers=self._auth_headers(token),
            data={
                "article": {
                    "title": title,
                    "description": description,
                    "body": body,
                    "tagList": tag_list or [],
                }
            },
        )
        assert response.ok, f"create_article failed ({response.status}): {response.text()}"
        return response.json()

    def delete_article(self, slug: str, token: str | None = None) -> None:
        """Delete an article by slug. Pass token for JWT auth, or rely on cookie
        header set on the underlying APIRequestContext for session-based auth.
        404 is tolerated — the test may have already deleted it via UI.
        """
        response = self._request.delete(
            f"/api/articles/{slug}",
            headers=self._auth_headers(token),
        )
        assert response.ok or response.status == 404, (
            f"delete_article failed with status {response.status}: {response.text()}"
        )
