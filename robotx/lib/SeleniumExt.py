"""
This is for Selenium2Library extention,
and Selenium origin webdriver extention

example,

from SeleniumExt import SeleniumExt


class MyExt(SeleniumExt):

    def biggest_window1(self):
        # use Selenium2Library methods
        self.s2l.maximize_browser_window()

    def biggest_window2(self):
        # use Selenium origin webdriver methods
        webdriver = self._origin_webdriver
        webdriver.maximize_window()
"""


from robot.libraries.BuiltIn import BuiltIn
from Selenium2Library.keywords.keywordgroup import KeywordGroup


class SeleniumExt(KeywordGroup):

    def __init__(self):
        self.s2l = self._get_s2l()

    def _get_s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    def _run_on_failure(self):
        """required for on failure in this class to work
        call Selenium2Library's on failure.
        """
        self.s2l._run_on_failure()

    @property
    def _origin_webdriver(self):
        return self.s2l._current_browser()

