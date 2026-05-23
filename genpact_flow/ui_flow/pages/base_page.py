from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, url, page: Page):
        self.page = page
        self.url = url

    def goto(self):
        self.page.goto(self.url, wait_until="domcontentloaded")

    def click(self, selector: str):
        self.page.locator(selector).click()

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def expect_visible(self, selector: str):
        expect(self.page.locator(selector)).to_be_visible()