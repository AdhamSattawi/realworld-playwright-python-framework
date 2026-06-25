import pytest
import time
import os
from pathlib import Path
from playwright.sync_api import Browser, BrowserContext, Page, expect, APIRequestContext, Playwright, Route, Request
from faker import Faker
from utils.api_client import APIClient

# Get the project root directory (where conftest.py is located)
PROJECT_ROOT = Path(__file__).parent

#Implemented Playwright storageState because the project uses NextAuth
# Ensure the .auth directory exists so we don't get a FileNotFoundError
os.makedirs(str(PROJECT_ROOT / "playwright/.auth"), exist_ok=True)
AUTH_FILE = "playwright/.auth/user.json"


def _rewrite_localhost_request(route: Route, request: Request, base_url: str) -> None:
    """Map localhost redirects to the configured test base URL in CI containers."""
    target_base = base_url.rstrip("/")
    request_url = request.url

    for localhost_prefix in ("http://localhost:3000", "https://localhost:3000"):
        if request_url.startswith(localhost_prefix):
            route.continue_(url=f"{target_base}{request_url[len(localhost_prefix):]}")
            return

    route.continue_()


@pytest.fixture(autouse=True)
def route_localhost_to_base_url(page: Page, base_url: str):
    """Prevent NextAuth callback redirects to localhost from breaking CI runs."""
    if "localhost:3000" in base_url:
        yield
        return

    handler = lambda route, request: _rewrite_localhost_request(route, request, base_url)
    page.route("http://localhost:3000/**", handler)
    page.route("https://localhost:3000/**", handler)
    yield
    page.unroute("http://localhost:3000/**", handler)
    page.unroute("https://localhost:3000/**", handler)

@pytest.fixture(scope="session", autouse=True)
def setup_auth(browser: Browser, base_url: str) -> None:
    """Logs in via UI and handles registration if the user doesn't exist."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    print(f"\n[Setup] Attempting login at {base_url}/login")
    page.goto("/login")
    
    page.get_by_placeholder("Email").fill("zpokerz10@hotmail.com")
    page.get_by_placeholder("Password").fill("zpokerz10")
    page.get_by_role("button", name="Sign in").click()

    try:
        # Check if login worked
        expect(page.locator(".navbar")).to_contain_text("zpokerz10", timeout=5000)
        print("[Setup] Login successful.")
    except AssertionError:
        # If the navbar didn't show the user, check if it's because they don't exist
        print("[Setup] Login failed or timed out. Checking for registration need...")
        
        # We check for error messages. If they exist, we register.
        if page.locator(".error-messages").count() > 0 or page.url.endswith("/login"):
            print("[Setup] User not found. Registering a new account...")
            page.goto("/register")
            
            # Use a timestamp to keep it unique, but consistent for this session
            unique_user = f"user_{int(time.time())}"
            page.get_by_placeholder("Username").fill(unique_user)
            page.get_by_placeholder("Email").fill("zpokerz10@hotmail.com")
            page.get_by_placeholder("Password").fill("zpokerz10")
            page.get_by_role("button", name="Sign up").click()
            
            # Final verification that registration worked
            expect(page.locator(".navbar")).to_be_visible(timeout=10000)

    # Save the state for all other tests
    context.storage_state(path=AUTH_FILE)
    context.close()


# 2. The Context Fixture: Injects the cookies into tests
@pytest.fixture
def logged_in_context(browser: Browser, base_url: str, setup_auth) -> BrowserContext:
    """Creates a fresh context PRE-LOADED with our NextAuth cookies."""
    context = browser.new_context(
        base_url=base_url,
        storage_state=AUTH_FILE 
    )
    yield context
    context.close()


# 3. The Page Fixture: What your tests will actually request
@pytest.fixture
def logged_in_page(logged_in_context: BrowserContext) -> Page:
    """Provides an authenticated page ready for testing."""
    page = logged_in_context.new_page()
    yield page



@pytest.fixture
def api_client(playwright: Playwright, base_url: str) -> APIRequestContext:
    request_context = playwright.request.new_context(base_url=base_url)
    yield request_context
    request_context.dispose()

FAKE = Faker()

@pytest.fixture
def create_test_user(api_client: APIRequestContext) -> dict:
    """Create a new user before the test run"""

    user_data = {
        "user": {
            "username": FAKE.user_name(),
            "email": FAKE.email(),
            "password": "ValidPassword123!"
        }
    }
    response = api_client.post(
        "/api/users",
        data=user_data
    )
    if not response.ok:
        print(f"DEBUG API ERROR: {response.text()}")
    assert response.ok
    yield user_data["user"]


@pytest.fixture
def create_article(playwright: Playwright, base_url: str, setup_auth):
    """Create an article via API before the test and delete it afterwards.

    Uses the session cookies saved by ``setup_auth`` (NextAuth does not expose
    a REST login endpoint that returns a JWT, so we piggyback on the stored
    browser state instead).

    Yields a dict with keys: ``slug``, ``title``.
    """
    import json as _json

    # Load the saved NextAuth session cookies from the auth file
    with open(AUTH_FILE) as f:
        storage = _json.load(f)
    cookies = {
        c["name"]: c["value"]
        for c in storage.get("cookies", [])
    }
    cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())

    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"Cookie": cookie_header},
    )
    client = APIClient(request_context)

    fake = Faker()
    title = fake.sentence(nb_words=4).rstrip(".")
    article_resp = client.create_article(
        token=None,  # auth via cookie header, not Bearer token
        title=title,
        description=fake.sentence(),
        body=fake.paragraph(),
        tag_list=["automation", "test"],
    )
    slug = article_resp["article"]["slug"]

    yield {"slug": slug, "title": title}

    # Cleanup — tolerates 404 if the test already deleted it via UI
    client.delete_article(token=None, slug=slug)
    request_context.dispose()
