from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library.keywords.keywordgroup import KeywordGroup


def _get_s2l():
    return BuiltIn().get_library_instance('Selenium2Library')


class Selenium2LibraryExt(KeywordGroup):

    def _run_on_failure(self):
        """required for on failure in this class to work
        call Selenium2Library's on failure.
        """
        _get_s2l()._run_on_failure()

    def do_something(self):
        """An example"""
        s2l = _get_s2l()
        webdriver = s2l._current_browser()
        # from now on, you can write your own code for the Keyword.
        # such as:
        webdriver.maximize_window()
        webdriver.close()
        # ...
