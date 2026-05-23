from genpact_flow.ui_flow.pages.base_page import BasePage
import re

class WikipediaPage(BasePage):
    def __init__(self, url, page):
        super().__init__(url, page)

    def open(self):
        self.goto()

    def get_text_by_headline(self, headline: str = "Debugging features") -> str:
        text = self.page.evaluate(
            """
            (headline) => {
                const cleanText = (text) =>
                    text.replace(/\\[edit\\]/gi, "")
                        .replace(/\\s+/g, " ")
                        .trim()
                        .toLowerCase();

                const getVisibleTextWithoutReferences = (element) => {
                    const clone = element.cloneNode(true);

                    clone.querySelectorAll(
                        "sup.reference, .mw-editsection"
                    ).forEach(ref => ref.remove());

                    return clone.innerText;
                };

                const removeEmptyLines = (text) => {
                    return text
                        .split("\\n")
                        .map(line => line.trim())
                        .filter(line => line.length > 0)
                        .join("\\n");
                };

                const headings = Array.from(
                    document.querySelectorAll("h1, h2, h3, h4, h5, h6")
                );

                const headingElement = headings.find(
                    h => cleanText(h.innerText) === cleanText(headline)
                );

                if (!headingElement) {
                    throw new Error(`Headline was not found: ${headline}`);
                }

                const headingLevel = Number(headingElement.tagName.substring(1));
                const texts = [];

                let element = headingElement.parentElement.nextElementSibling;

                while (element) {
                    const nextHeading = element.querySelector("h1, h2, h3, h4, h5, h6");

                    if (nextHeading) {
                        const nextHeadingLevel = Number(nextHeading.tagName.substring(1));

                        if (nextHeadingLevel <= headingLevel) {
                            break;
                        }
                    }

                    const elementText = getVisibleTextWithoutReferences(element);

                    if (elementText.trim()) {
                        texts.push(elementText);
                    }

                    element = element.nextElementSibling;
                }

                return removeEmptyLines(texts.join("\\n"));
            }
            """,
            headline
        )

        return text

    def get_testing_and_debugging_tool_names_and_links(self):
        return self.page.evaluate("""
            () => {
                const navbox = [...document.querySelectorAll("div.navbox")]
                    .find(box => box.innerText.includes("Microsoft development tools"));

                if (!navbox) {
                    throw new Error("Microsoft development tools navbox was not found");
                }

                const rows = [...navbox.querySelectorAll("tr")];

                const row = rows.find(row =>
                    row.innerText.replace(/\\s+/g, " ").includes("Testing and debugging")
                );

                if (!row) {
                    throw new Error("Testing and debugging row was not found");
                }

                return [...row.querySelectorAll("td li")].map(li => {
                    const link = li.querySelector("a");
                    const href = link ? link.getAttribute("href") : null;

                    return {
                        name: li.innerText.trim(),
                        has_a_tag: !!link,
                        href: href,
                        is_real_link: !!href
                    };
                });
            }
        """)

    def select_color_mode(self, mode: str):
        allowed_modes = {
            "Automatic": "os",
            "Light": "day",
            "Dark": "night"
        }

        if mode not in allowed_modes:
            raise ValueError(f"Invalid color mode: {mode}. Use one of: {list(allowed_modes.keys())}")

        value = allowed_modes[mode]

        color_section = self.page.locator("#skin-client-prefs-skin-theme")

        color_section.locator(
            f"input[name='skin-client-pref-skin-theme-group'][value='{value}']"
        ).check()

    def get_html_class(self) -> str:
        html_class = self.page.locator("html").get_attribute("class")

        if html_class is None:
            raise AssertionError("HTML class attribute was not found")

        return html_class
