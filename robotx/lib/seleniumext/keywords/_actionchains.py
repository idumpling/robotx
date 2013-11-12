from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains


class _ActionChainsKeywords:

    def __init__(self):
        self.action_chains = None

    @property
    def s2l(self):
        return BuiltIn().get_library_instance('Selenium2Library')

    def __lazy_init_action_chains(self):
        if self.action_chains is None:
            self.action_chains = ActionChains(self.s2l._current_browser())
        return self.action_chains

    def chain_click(self, on_element=None):
        """ Click on the element identified by the on_element locator.
        When no such thing, click where the mouse currently is.
        """
        if on_element is not None:
            element = self.s2l._element_find(on_element, True, True)
        else:
            element = None
        self.__lazy_init_action_chains().click(element)

    def chain_double_click(self, on_element=None):
        """ Click on the element identified by the on_element locator.
        When no such thing, click where the mouse currently is.
        """
        if on_element is not None:
            element = self.s2l._element_find(on_element, True, True)
        else:
            element = None
        self.__lazy_init_action_chains().double_click(element)

    def chain_context_click(self, on_element=None):
        """ Click on the element identified by the on_element locator.
        When no such thing, click where the mouse currently is.
        """
        if on_element is not None:
            element = self.s2l._element_find(on_element, True, True)
        else:
            element = None
        self.__lazy_init_action_chains().context_click(element)

    def chain_drag_and_drop(self, source, target):
        """Drags element identified with locator by movement

        `movement is a string in format "+70 -300" interpreted as pixels in
        relation to elements current position.
        """
        element = self.s2l._element_find(source, True, True)
        target = self.s2l._element_find(target, True, True)
        self.__lazy_init_action_chains().drag_and_drop(element, target)

    def chain_drag_and_drop_with_offset(self, source, target, xset, yset):
        """Drags element identified with locator by movement

        `movement is a string in format "+70 -300" interpreted as pixels in
        relation to elements current position.
        """
        element = self.s2l._element_find(source, True, True)
        target = self.s2l._element_find(target, True, True)
        self.__lazy_init_action_chains().click_and_hold(element).\
            move_to_element_with_offset(target, xset, yset).release()

    def chain_click_and_hold(self, source):
        """ Click and hold the element identified by the 'source' locator
        """
        element = self.s2l._element_find(source, True, True)
        self.__lazy_init_action_chains().click_and_hold(element)

    def chain_release(self, target):
        """ Move the mouse to the element identified by the 'target' locator
        Release the mouse.
        """
        element = self.s2l._element_find(target, True, True)
        self.__lazy_init_action_chains().release(element)

    def move_by_offset(self, xoffset, yoffset):
        """Moving the mouse to an offset from current mouse position.
        Args:
            xoffset: X offset to move to.
            yoffset: Y offset to move to.
        """
        self.__lazy_init_action_chains().move_by_offset(xoffset, yoffset)

    def chain_move_to_element(self, target):
        element = self.s2l._element_find(target, True, True)
        self.__lazy_init_action_chains().move_to_element(element)

    def chain_move_to_element_with_offset(self, target, xoffset, yoffset):
        element = self.s2l._element_find(target, True, True)
        self.__lazy_init_action_chains().move_to_element_with_offset(
            element, xoffset, yoffset)

    def chain_send_keys(self, *keys_to_send):
        """Sends keys to current focused element.
        Args:
            keys_to_send: The keys to send.
        """
        self.__lazy_init_action_chains().send_keys(*keys_to_send)

    def chain_send_keys_to_element(self, element, *keys_to_send):
        """Sends keys to an element identifed by the 'eleemnt' locator.
        Args:
            element: The element to send keys.
            keys_to_send: The keys to send.
        """
        element_el = self.s2l._element_find(element, True, True)
        self.__lazy_init_action_chains().send_keys(element_el, *keys_to_send)

    def chain_sleep(self, time_, reason=None):
        """ Add a sleep to the action chains
        """
        self.__lazy_init_action_chains()._actions.append(
            lambda: BuiltIn().sleep(time_, reason))

    def chains_perform_now(self):
        if self.action_chains is not None:
            self.action_chains.perform()
            self.action_chains = None
