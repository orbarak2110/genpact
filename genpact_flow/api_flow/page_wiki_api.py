import requests
from bs4 import BeautifulSoup

from genpact_flow.api_flow.base_api_client import BaseApiClient


class WikiPageAPI(BaseApiClient):
    def __init__(self, base_url, session: requests.Session):
        super().__init__(base_url, session)

    @staticmethod
    def clean_wikipedia_html_to_text(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.select(
                "sup.reference, "
                ".mw-editsection, "
                ".mw-references-wrap, "
                "ol.references, "
                ".references, "
                ".reference, "
                "h1, h2, h3, h4, h5, h6"
        ):
            tag.decompose()

        return soup.get_text("\n", strip=True)

    def get_sections(self, page_title: str):
        params = {
            "action": "parse",
            "page": page_title,
            "prop": "sections",
            "format": "json",
        }

        data = self.get(params=params)
        return data["parse"]["sections"]

    def get_section_index(self, page_title: str, section_title: str) -> str:
        sections = self.get_sections(page_title)

        for section in sections:
            if section["line"].strip().lower() == section_title.strip().lower():
                return section["index"]

        raise ValueError(f"Section not found: {section_title}")

    def get_section_html(self, page_title: str, section_title: str) -> str:
        section_index = self.get_section_index(
            page_title=page_title,
            section_title=section_title
        )

        params = {
            "action": "parse",
            "page": page_title,
            "section": section_index,
            "prop": "text",
            "format": "json",
        }

        data = self.get(params=params)
        return data["parse"]["text"]["*"]

    def get_section_text(self, page_title: str="Playwright_(software)", section_title: str="Debugging features") -> str:
        html = self.get_section_html(
            page_title=page_title,
            section_title=section_title
        )

        return self.clean_wikipedia_html_to_text(html)




