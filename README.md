# Playwright + Pytest Framework

This repository provides a production-ready Python test automation framework built with Pytest and Playwright. It includes:

- reusable browser fixtures
- a page object model structure
- logging and screenshot capture on failures
- HTML test reporting
- sample UI and API tests
- test organization by suite type

## Project Structure

- config/: framework configuration and environment settings
- core/: shared base classes for page objects
- fixtures/: reusable fixtures and test hooks
- locators/: CSS selectors grouped by page
- pages/: page object classes
- tests/: test suites organized by purpose
  - tests/ui/
  - tests/smoke/
  - tests/regression/
  - tests/api/
- utils/: helpers and logging utilities
- reports/: generated pytest HTML reports
- screenshots/: generated screenshots on failures
- logs/: framework log output
- testdata/: static input files

## Prerequisites

- Python 3.10+
- pip

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Run Tests

Run all tests:

```bash
pytest
```

Run a specific suite:

```bash
pytest tests/ui
pytest tests/api
pytest tests/smoke
pytest tests/regression
```

Run a specific test file:

```bash
pytest tests/ui/test_sample_app.py
```

## Reporting and Artifacts

- HTML report: reports/pytest_report.html
- Failure screenshots: screenshots/
- Logs: logs/framework.log

## Example Features

- Playwright browser fixtures
- Base page class with common actions
- Page objects for reusable UI flows
- Automatic failure screenshots
- Pytest markers for smoke, UI, regression, and API tests

## Notes

The framework is designed to be extended as your suite grows. You can add new page objects, locators, and test files under the existing structure.
