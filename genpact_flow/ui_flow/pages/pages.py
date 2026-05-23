from playwright.sync_api import Page

from genpact_flow.ui_flow.pages.wikipedia_page import WikipediaPage


class Pages:
    def __init__(self, url, page: Page):
        self.wiki_page = WikipediaPage(url, page)