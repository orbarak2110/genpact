import pytest
import requests

from genpact_flow.genpact_flow import GenpactFlow


@pytest.fixture(scope="session")
def base_url():
    return "https://en.wikipedia.org/wiki/Playwright_(software)"

@pytest.fixture(scope="session")
def base_url_api():
    return "https://en.wikipedia.org/w/api.php"

@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()

    session.headers.update({
        "User-Agent": "GenpactAutomationAssignment/1.0",
        "Accept": "application/json"
    })

    yield session

    session.close()

@pytest.fixture
def genpact_flow(base_url, api_session, base_url_api, page):
    return GenpactFlow(base_url, api_session, base_url_api, page)