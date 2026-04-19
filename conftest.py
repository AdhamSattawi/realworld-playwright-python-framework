import pytest
import time
import os
from playwright.sync_api import Browser, BrowserContext, Page, expect, APIRequestContext, Playwright
from faker import Faker

#Implemented Playwright storageState because the project uses NextAuth
# Ensure the .auth directory exists so we don't get a FileNotFoundError
os.makedirs("playwright/.auth", exist_ok=True)
AUTH_FILE = "playwright/.auth/user.json"

# 1. The Global Setup: Runs exactly ONCE per test run
@pytest.fixture(scope="session", autouse=True)
def setup_auth(browser: Browser, base_url: str) -> None:
    """Logs in via UI, handles registration if needed, and saves cookies."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    page.goto("/login")
    
    # Note: I'm using the standard Conduit locators here
    page.get_by_placeholder("Email").fill("zpokerz10@hotmail.com")
    page.get_by_placeholder("Password").fill("zpokerz10")
    page.get_by_role("button", name="Sign in").click()

    # The SDET Fallback: Did the login fail because the database was wiped?
    if page.locator(".error-messages").is_visible():
        print("\n[Setup] User not found. Registering a new account...")
        page.goto("/register")
        # Generate a unique username using the current timestamp
        unique_user = f"testuser_{int(time.time())}"
        
        page.get_by_placeholder("Username").fill(unique_user)
        page.get_by_placeholder("Email").fill("zpokerz10@hotmail.com")
        page.get_by_placeholder("Password").fill("zpokerz10")
        page.get_by_role("button", name="Sign up").click()

    # Wait for the login/registration to actually finish (Profile link appears)
    expect(page.locator(".navbar a[href^='/profile/']")).to_be_visible(timeout=10000)

    # Save the NextAuth cookies to your JSON file!
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
