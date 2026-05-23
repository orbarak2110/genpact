


def test_section_1(genpact_flow):
    """
        Validate that the 'Debugging features' section contains the same unique word count
        when extracted from both the Wikipedia UI and the MediaWiki API.

        Test flow:
        1. Open the Playwright Wikipedia page using the UI flow.
        2. Extract the 'Debugging features' section text from the API.
        3. Extract the same section text from the UI by headline.
        4. Normalize both texts using the shared Utils class.
        5. Count the unique words in both texts.
        6. Assert that the unique word counts are equal.
    """
    genpact_flow.ui_flow.wiki_page.open()
    api_txt = genpact_flow.api_flow.get_section_text()
    ui_txt_page = genpact_flow.ui_flow.wiki_page.get_text_by_headline()
    assert genpact_flow.utils.count_unique_words(api_txt) == genpact_flow.utils.count_unique_words(ui_txt_page)

def test_section_2(genpact_flow):
    """
        Validate that all technology names under the 'Testing and debugging' row
        in the 'Microsoft development tools' section are real text links.

        Test flow:
        1. Open the Playwright Wikipedia page using the UI flow.
        2. Locate the 'Microsoft development tools' navbox.
        3. Locate the 'Testing and debugging' row inside that navbox.
        4. Extract all technology items from the row.
        5. Validate that at least one technology item was found.
        6. For each technology item, verify that it contains an anchor tag with an href.
        7. Fail the test if any technology name is not a real text link.
    """
    genpact_flow.ui_flow.wiki_page.open()

    tools = genpact_flow.ui_flow.wiki_page.get_testing_and_debugging_tool_names_and_links()

    assert len(tools) > 0, "No technology items found under Testing and debugging"

    for tool in tools:
        assert tool["is_real_link"], (
            f"Technology '{tool['name']}' is not a real text link. "
            f"Expected an <a> tag with href."
        )


def test_section_3(genpact_flow):
    """
        Validate that the Wikipedia color mode can be changed to Dark.

        Test flow:
        1. Open the Playwright Wikipedia page using the UI flow.
        2. Select the 'Dark' option from the Color section.
        3. Read the class attribute from the HTML element.
        4. Validate that the HTML class contains 'skin-theme-clientpref-night',
           which indicates that the dark color mode was applied.
    """
    genpact_flow.ui_flow.wiki_page.open()
    genpact_flow.ui_flow.wiki_page.select_color_mode("Dark")
    assert "skin-theme-clientpref-night" in genpact_flow.ui_flow.wiki_page.get_html_class()
