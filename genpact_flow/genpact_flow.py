from genpact_flow.api_flow.page_wiki_api import WikiPageAPI
from genpact_flow.ui_flow.pages.pages import Pages
from utils.text_utils import Utils


class GenpactFlow:
    def __init__(self, base_url, session, base_url_api, page):
        self.ui_flow = Pages(base_url, page)
        self.api_flow = WikiPageAPI(base_url_api, session)
        self.utils = Utils()