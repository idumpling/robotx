from keywords._pagetests import _PageTestsKeywords
from keywords._draganddrop import _DragAndDropKeywords
from keywords._actionchains import _ActionChainsKeywords


class Selenium2LibraryExtensions(_PageTestsKeywords, _DragAndDropKeywords,
                                 _ActionChainsKeywords):
    """Selenium2LibraryExtensions adds a number of keywords to the
    Selenium2Library.

    Note that in fact it does not extend the Selenium2Library.
    Internally it accesses the Selenium2Library instance and uses the
    underlying selenium browser.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.0.1'

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot'):
        for base in Selenium2LibraryExtensions.__bases__:
            if hasattr(base, '__init__'):
                base.__init__(self)
