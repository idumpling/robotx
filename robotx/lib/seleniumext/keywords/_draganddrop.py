from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains


class _DragAndDropKeywords:
    @property
    def s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    def drag_and_drop(self, source, target):
        """Drags element identified with locator 'source' onto the element
        identified by the locator 'target'
        """
        element = self.s2l._element_find(source, True, True)
        target_elem = self.s2l._element_find(target, True, True)
        ActionChains(self.s2l._current_browser()).drag_and_drop(
            element, target_elem).perform()

    def drag_and_drop_with_offset(self, source, target, xoffset, yoffset):
        """Drags element identified with 'source' locator onto the
        target element identified by the target locator.
        Before dropping, move to the offset specified
        """
        element = self.s2l._element_find(source, True, True)
        target_elem = self.s2l._element_find(target, True, True)
        ActionChains(self.s2l._current_browser()).click_and_hold(
            element).move_to_element_with_offset(
            target_elem, xoffset, yoffset).perform()
