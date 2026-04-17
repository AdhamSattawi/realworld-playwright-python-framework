# RealWorld Conduit E2E Automation Framework

[![Playwright Tests](https://github.com/AdhamSattawi/realworld-playwright-python-framework/actions/workflows/playwright.yml/badge.svg)](https://github.com/AdhamSattawi/realworld-playwright-python-framework/actions)

## 📌 Overview
An enterprise-grade End-to-End (E2E) testing framework built to validate the [RealWorld (Conduit) Next.js application](https://github.com/AdhamSattawi/next-fullstack-realworld-app). 

This framework demonstrates scalable test architecture, utilizing the **Page Object Model (POM)** design pattern, **Data-Driven Testing (DDT)**, and seamless **API state injection** to optimize test execution speed and reliability.

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.x
* **Framework:** Playwright & Pytest
* **Design Pattern:** Page Object Model (POM)
* **CI/CD:** GitHub Actions (with Docker Compose integration)
* **Reporting:** Playwright HTML Reporter

## 🚀 Key Features
* **Strict Separation of Concerns:** Complete decoupling of UI locators, test data, and business assertions.
* **API Interception (Fast Login):** Utilizes Playwright's `APIRequestContext` to bypass UI login sequences, injecting session state directly into the browser context to reduce execution time.
* **Fully Containerized CI/CD:** The GitHub Actions pipeline automatically spins up the target Next.js + Postgres application via Docker Compose before executing the test suite against the ephemeral environment.
* **Automated HTML Reporting:** Detailed HTML reports with trace viewers and failure screenshots are automatically uploaded as artifacts to every CI/CD run.

## 📁 Project Structure
```text
├── .github/workflows/
│   └── playwright.yml      # CI/CD pipeline definition
├── data/
│   └── test_users.json     # Data-Driven Testing (DDT) payloads
├── pages/
│   ├── base_page.py        # Core UI interactions and explicit waits
│   
├── tests/
│   ├── conftest.py         # Global Pytest fixtures and API state setups
│   
├── utils/
│   └── api_client.py       # API setup for state injection
├── requirements.txt        # Python dependencies
└── README.md               # Framework documentation