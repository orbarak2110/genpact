# Genpact Automation Infrastructure Assignment

## Overview

This project is a lightweight automation framework built with **Python**, **Playwright**, **Pytest**, and **Requests**.

The assignment goal is to test the Wikipedia page:

```text
https://en.wikipedia.org/wiki/Playwright_(software)
```

The project contains both **UI automation** and **API automation**, with a clean separation between the UI flow, API flow, utilities, fixtures, and tests.

---

## Tech Stack

- Python
- Playwright
- Pytest
- Pytest Playwright
- Requests
- BeautifulSoup

---

## Project Structure

```text
genpact/
│
├── genpact_flow/
│   ├── api_flow/
│   │   ├── base_api_client.py
│   │   └── page_wiki_api.py
│   │
│   ├── ui_flow/
│   │   └── pages/
│   │       ├── base_page.py
│   │       ├── pages.py
│   │       └── wikipedia_page.py
│   │
│   └── genpact_flow.py
│
├── tests/
│   └── test_assignment.py
│
├── utils/
│   └── text_utils.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Framework Design

The framework is divided into several layers:

### API Flow

The API flow contains the API client logic for working with the MediaWiki API.

Main files:

```text
genpact_flow/api_flow/base_api_client.py
genpact_flow/api_flow/page_wiki_api.py
```

Responsibilities:

- Send API requests using `requests`
- Handle API response errors
- Get Wikipedia page sections
- Find a section index by section title
- Extract section HTML
- Convert Wikipedia HTML into clean text using BeautifulSoup

---

### UI Flow

The UI flow contains the Page Object Model classes for working with the Wikipedia page through Playwright.

Main files:

```text
genpact_flow/ui_flow/pages/base_page.py
genpact_flow/ui_flow/pages/pages.py
genpact_flow/ui_flow/pages/wikipedia_page.py
```

Responsibilities:

- Open the Wikipedia page
- Extract section text from the UI by headline
- Locate the Microsoft development tools navbox
- Validate technology names under the Testing and debugging row
- Select Wikipedia color mode
- Validate the HTML class after changing the color mode

---

### Utils

The utils layer contains reusable helper methods.

Main file:

```text
utils/text_utils.py
```

Responsibilities:

- Normalize text
- Remove references and special characters
- Split text into words
- Count unique words

---

## GenpactFlow Object

The `GenpactFlow` object is the main high-level object used by the tests.

It is very useful when a test needs to work with both **UI** and **API** in the same scenario.

Instead of creating the UI page object and the API client separately in every test, the test receives one object from the fixture:

```python
def test_section_1(genpact_flow):
    genpact_flow.ui_flow.wiki_page.open()
    api_txt = genpact_flow.api_flow.get_section_text()
    ui_txt_page = genpact_flow.ui_flow.wiki_page.get_text_by_headline()

    assert genpact_flow.utils.count_unique_words(api_txt) == genpact_flow.utils.count_unique_words(ui_txt_page)
```

The `genpact_flow` object gives access to:

```python
genpact_flow.ui_flow
genpact_flow.api_flow
genpact_flow.utils
```

This makes the tests cleaner, more readable, and easier to maintain, especially when combining UI validations with API validations.

---

## Fixtures

The project uses fixtures from `conftest.py`.

### base_url

Returns the Wikipedia page URL:

```python
https://en.wikipedia.org/wiki/Playwright_(software)
```

### base_url_api

Returns the MediaWiki API URL:

```python
https://en.wikipedia.org/w/api.php
```

### api_session

Creates a reusable `requests.Session()` with default headers.

### genpact_flow

Creates and returns the main `GenpactFlow` object used by the tests.

---

## Test Cases

All tests are located in:

```text
tests/test_assignment.py
```

---

### test_section_1

This test validates the **Debugging features** section.

Flow:

1. Open the Wikipedia page through the UI.
2. Extract the `Debugging features` section using the UI.
3. Extract the same section using the MediaWiki API.
4. Normalize both texts.
5. Count unique words.
6. Assert that both unique word counts are equal.

---

### test_section_2

This test validates the **Microsoft development tools** section.

Flow:

1. Open the Wikipedia page.
2. Find the `Microsoft development tools` navbox.
3. Find the `Testing and debugging` row.
4. Extract the technology names.
5. Validate that every technology item is a real text link.
6. Fail the test if one of the technology names does not contain an `<a>` tag with an `href`.

---

### test_section_3

This test validates changing Wikipedia color mode to **Dark**.

Flow:

1. Open the Wikipedia page.
2. Select the `Dark` color mode.
3. Get the HTML class attribute.
4. Validate that the class contains:

```text
skin-theme-clientpref-night
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd genpact
```

Replace `<repository-url>` with the GitHub repository URL.

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

---

### 3. Activate the virtual environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

---

### 4. Install requirements

```bash
pip install -r requirements.txt
```

---

### 5. Install Playwright browsers

```bash
playwright install
```

---

## Requirements

The current `requirements.txt` contains:

```text
playwright==1.60.0
pytest==9.0.3
pytest-playwright==0.8.0
requests==2.34.2
beautifulsoup4==4.14.3
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Because `pytest.ini` already includes:

```ini
[pytest]
testpaths = tests
addopts = -v --browser chromium --headed
```

The tests will run with:

- verbose mode
- Chromium browser
- headed browser mode

---

## Run a Specific Test File

```bash
pytest tests/test_assignment.py
```

---

## Run a Specific Test

Run Task 1:

```bash
pytest tests/test_assignment.py::test_section_1
```

Run Task 2:

```bash
pytest tests/test_assignment.py::test_section_2
```

Run Task 3:

```bash
pytest tests/test_assignment.py::test_section_3
```

---

## Assignment Coverage

### Task 1

Extract the `Debugging features` section:

- Via UI using Playwright and Page Object Model
- Via API using MediaWiki Parse API

Then normalize both texts, count unique words, and validate that the counts are equal.

Covered by:

```text
test_section_1
```

---

### Task 2

Go to the Microsoft development tools section and validate that all technology names under `Testing and debugging` are text links.

Covered by:

```text
test_section_2
```

---

### Task 3

Go to the `Color (beta)` section and change the color to `Dark`.

Then validate that the color actually changed.

Covered by:

```text
test_section_3
```

---

## Notes

- The framework uses the Page Object Model pattern for UI automation.
- API logic is separated from UI logic.
- Shared utilities are located under the `utils` folder.
- `GenpactFlow` is used as a single entry point for the tests.
- The same test can easily combine UI actions and API validations.
- The project is designed to be simple, readable, and easy to extend.

---

## Author

Or Barak