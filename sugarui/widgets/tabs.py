# coding: utf-8
"""
Various buttons.
"""
import curses
import curses.ascii
import npyscreen


class TabButton(npyscreen.widget.Widget):
    """
    Tab button.
    """

    def __init__(self, screen, *args, color="CONTROL", label="Button", **kwargs):
        self._label = " {} ".format(label)
        self.color = color
        self.id = hash(self._label)
        self._tab_group = None
        self._callbacks = []
        self._is_active = False
        self._is_control_tab = False

        kwargs["max_height"] = 1
        npyscreen.widget.Widget.__init__(self, screen, *args, **kwargs)
        self.width = len(self._label)

        self.handlers.update({
            curses.ascii.SP: self._on_tab_select,
            ord('x'): self._on_tab_select,
            curses.ascii.NL: self._on_tab_select,
            curses.ascii.CR: self._on_tab_select,
            ord('j'): self.h_exit_down,
            ord('k'): self.h_exit_up,
            ord('h'): self.h_exit_left,
            ord('l'): self.h_exit_right,
        })

    def handle_mouse_event(self, mouse_event):
        """
        Handle mouse click.

        :param mouse_event:
        :return:
        """
        self._on_tab_select(None)

    def _on_tab_select(self, ch):
        """
        Handle keyboard click.

        :param ch: None is mouse event
        :return:
        """
        if self._tab_group is None:
            raise Exception("Tab is not in the group. Please add it to one.")

        self._tab_group.on_tab_select(self.id)
        for callback, args, kwargs in self._callbacks:
            callback(*args, **kwargs)

    def add_callback(self, callback, *args, **kwargs):
        """
        Add callback when tab is selected.

        :param callback:
        :param args:
        :param kwargs:
        :return:
        """
        self._callbacks.append((callback, args, kwargs))

    def set_active(self, state):
        """
        Set tab active or inactive.

        :param state:
        :return:
        """
        self._is_active = state

    def update(self, clear=True):
        """
        Update button on the screen.

        :param clear:
        :return:
        """
        self.color = "GOOD"
        state = curses.A_BOLD if self.editing else curses.A_NORMAL

        if self._is_active:
            state = state | curses.A_STANDOUT
            lc, rc = "\u2597", "\u2596"
        else:
            lc, rc = " ", " "

        self.add_line(self.rely, self.relx + len(lc), self._label,
                      self.make_attributes_list(self._label, self.parent.theme_manager.findPair(self, self.color) | state),
                      self.width)
        # corners
        self.add_line(self.rely, self.relx, lc,
                      self.make_attributes_list(lc, self.parent.theme_manager.findPair(self, self.color)),
                      self.width)
        self.add_line(self.rely, self.relx + len(self._label) + 1, rc,
                      self.make_attributes_list(rc, self.parent.theme_manager.findPair(self, self.color)),
                      self.width)


class TabGroup:
    """
    Tab group.
    """
    def __init__(self, relx, rely, space=2, autoalign=True):
        self._group = []
        self.space = space
        self.relx = relx
        self.rely = rely

    def add_tab(self, tab: TabButton, callbacks: list = None):
        """
        Add a tab object to the group.

        :param tab:
        :param callbacks: list of callbacks. Each callback is a tuple of (func, args, kwargs).
        :return:
        """
        self._group.append(tab)
        tab._tab_group = self
        for callback in callbacks or []:
            callback, args, kwargs = callback
            tab.add_callback(callback, args, kwargs)

    def align(self):
        """
        Align group on the canvas.

        :return:
        """
        offset = 0
        for tab in self._group:
            tab.rely = self.rely
            tab.relx = self.relx + offset
            offset += tab.width + self.space

    def on_tab_select(self, tab_id):
        """
        Select current tab.

        :param tab_id:
        :return:
        """
        for tab in self._group:
            tab.set_active(tab.id == tab_id)
            tab.update()
