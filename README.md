# RealWorld Conduit E2E Automation Framework
[![Playwright Tests](https://github.com/AdhamSattawi/realworld-playwright-python-framework/actions/workflows/playwright.yml/badge.svg)](https://github.com/AdhamSattawi/realworld-playwright-python-framework/actions)

## 📌 Overview
An enterprise-grade End-to-End (E2E) testing framework built to validate the [RealWorld (Conduit) Next.js application](https://github.com/AdhamSattawi/next-fullstack-realworld-app). 

This framework demonstrates scalable test architecture, utilizing the **Page Object Model (POM)** design pattern, **Component Objects**, and seamless **State Injection** to optimize test execution speed and reliability.

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.10+
* **Framework:** Playwright & Pytest
* **Design Pattern:** Page Object Model (POM) + Composition
* **CI/CD:** GitHub Actions (with Docker Compose integration)
* **Reporting:** Playwright HTML Reporter

## 🚀 Key Features
* **Strict Separation of Concerns:** Complete decoupling of UI locators, test scripts, and business logic.
* **Authentication Bypass (Fast Login):** Leverages Playwright's `storageState` and Pytest fixtures to handle NextAuth sessions natively. UI login is performed once per test suite, and the resulting session cookies are injected into all subsequent tests to drastically reduce execution time and flakiness.
* **API-Backed Test Setup:** A dedicated `APIClient` utility class creates and tears down test data (users, articles) via the RealWorld REST API, keeping tests fast and fully independent of one another.
* **Data-Driven Testing (DDT):** Negative scenarios for login and registration are driven from JSON payloads, making it trivial to add or update edge cases without touching test code.
* **Environment Agnostic:** Configuration is managed via `pytest.ini`, allowing seamless execution against local, staging, or production environments without requiring code changes.
* **Fully Containerized CI/CD:** The GitHub Actions pipeline automatically spins up the target Next.js + Postgres application via Docker Compose before executing the test suite against the ephemeral environment.
* **Automated HTML Reporting:** Detailed HTML reports with trace viewers and failure screenshots are automatically uploaded as artifacts to every CI/CD run.

---

## ☁️ Running via CI/CD (No Local Setup Required)

For code reviewers and hiring managers, you do not need to pull this repository locally to see the framework in action. 

1. Navigate to the **[Actions tab](../../actions)** of this repository.
2. Select the **Playwright Tests** workflow on the left sidebar.
3. Click the **Run workflow** dropdown on the right side and execute it against the `main` branch.
4. Once the pipeline completes, scroll to the bottom of the summary page to download the **Playwright HTML Report** artifact.

---

## 📁 Project Structure
```text
├── .github/workflows/
│   └── playwright.yml          # CI/CD pipeline definition (includes workflow_dispatch)
├── components/
│   └── navbar.py               # Shared UI components (Composition over Inheritance)
├── data/
│   ├── user_login.json         # Negative login scenarios (DDT)
│   └── test_users.json         # Negative sign-up scenarios (DDT)
├── pages/
│   ├── base_page.py            # Core UI interactions and Playwright wrappers
│   ├── home_page.py            # Home / feed page object
│   ├── sign_in_page.py         # Login page object
│   ├── sign_up_page.py         # Registration page object
│   ├── article_page.py         # Article detail page object
│   ├── editor_page.py          # Article editor page object
│   ├── profile_page.py         # User profile page object
│   └── settings_page.py        # User settings page object
├── tests/
│   ├── test_home.py            # Home page smoke tests
│   ├── test_feed.py            # Global feed, personal feed, tag filtering
│   ├── test_auth.py            # Sign-in & sign-up (happy path + negative DDT)
│   ├── test_articles.py        # Article CRUD, comments, favourites
│   ├── test_settings.py        # Settings update & logout
│   └── test_profile.py         # Profile page & tab navigation
├── utils/
│   ├── api_client.py           # APIClient helper for test setup/teardown
│   └── file_load.py            # JSON data loader utility
├── conftest.py                 # Global Pytest fixtures (Auth setup, State Injection, API fixtures)
├── .gitignore                  # Ignores local auth state (playwright/.auth/)
├── pytest.ini                  # Pytest config (base_url, default CLI flags)
├── requirements.txt            # Python dependencies
└── README.md                   # Framework documentation
```