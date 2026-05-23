import requests


class BaseApiClient:
    def __init__(self, base_url: str, session: requests.Session, timeout: int = 15):
        self.base_url = base_url
        self.timeout = timeout
        self.session = session

    def get(self, endpoint: str = "", params: dict | None = None, headers: dict | None = None):
        url = f"{self.base_url}{endpoint}"

        response = self.session.get(
            url=url,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        return self._handle_response(response)

    def post(
        self,
        endpoint: str = "",
        json: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ):
        url = f"{self.base_url}{endpoint}"

        response = self.session.post(
            url=url,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout
        )

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise AssertionError(
                f"API request failed.\n"
                f"Status code: {response.status_code}\n"
                f"URL: {response.url}\n"
                f"Response body: {response.text}"
            ) from error

        try:
            return response.json()
        except ValueError:
            return response.text

