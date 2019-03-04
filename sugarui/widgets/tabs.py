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

    def __init__(self, screen, *args, color="CONTROL", title="Button", **kwargs):
        self._title = " {} ".format(title)
        self.color = color
        self.id = hash(self._title)
        self._tab_group = None
        self._callbacks = []
        self._is_active = False
        self._is_control_tab = False

        kwargs["max_height"] = 1
        npyscreen.widget.Widget.__init__(self, screen, *args, **kwargs)
        self.width = len(self._title)

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
            lc, rc = "[", "]"
        else:
            lc, rc = " ", " "

        self.add_line(self.rely, self.relx + len(lc), self._title,
                      self.make_attributes_list(self._title, self.parent.theme_manager.findPair(self, self.color) | state),
                      self.width)
        # corners
        self.add_line(self.rely, self.relx, lc,
                      self.make_attributes_list(lc, self.parent.theme_manager.findPair(self, self.color)),
                      self.width)
        self.add_line(self.rely, self.relx + len(self._title) + 1, rc,
                      self.make_attributes_list(rc, self.parent.theme_manager.findPair(self, self.color)),
                      self.width)


class TabGroupBase(npyscreen.widget.Widget):
    """
    Tab group base.
    """
    def __init__(self, screen, *args, color="GOOD", **kwargs):
        kwargs["max_height"] = 1
        kwargs["editable"] = False
        npyscreen.widget.Widget.__init__(self, screen, *args, **kwargs)
        self.color = color
        self._label = None

    def set_label(self, label):
        """
        Set label of the base.

        :return:
        """
        if label is not None:
            self._label = "{} {} ".format(label, "\u25C2\u25C2\u25C2")
        else:
            self._label = None

    def update(self, clear=True):
        line = "\u2588" * self.width
        self.add_line(self.rely, self.relx, line,
                      self.make_attributes_list(line, self.parent.theme_manager.findPair(self, self.color)), self.width)

        line = "\u2582" * self.width
        self.add_line(self.rely - 1, self.relx, line,
                      self.make_attributes_list(line, self.parent.theme_manager.findPair(self, self.color)), self.width)

        if self._label is not None:
            self.add_line(self.rely, self.relx + self.width - len(self._label), self._label, self.make_attributes_list(
                self._label, self.parent.theme_manager.findPair(self, self.color) | curses.A_STANDOUT), self.width)


class TabGroup:
    """
    Tab group.
    """
    def __init__(self, screen, relx, rely, space=3):
        self._group = []
        self.space = space
        self.relx = relx
        self.rely = rely
        self.screen = screen
        self.base = self.screen.add(TabGroupBase, relx=self.relx, rely=self.rely + 1)

    def add_tab(self, tab: TabButton, label: str = None, callbacks: list = None):
        """
        Add a tab object to the group.

        :param tab:
        :param callbacks: list of callbacks. Each callback is a tuple of (func, args, kwargs).
        :return:
        """
        self._group.append((tab, label))
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
        for tab, label in self._group:
            tab.rely = self.rely
            tab.relx = self.relx + offset + 1
            offset += tab.width + self.space

    def on_tab_select(self, tab_id):
        """
        Select current tab.

        :param tab_id:
        :return:
        """
        for tab, label in self._group:
            if tab.id == tab_id:
                self.base.set_label(label)
                tab.set_active(True)
            else:
                tab.set_active(False)

        self.base.update()

        for tab, label in self._group:
            tab.update()
