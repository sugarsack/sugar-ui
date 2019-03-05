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
            callback(*(args or []), **(kwargs or {}))

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

    def tab_width(self):
        """
        Get tab width.

        :return:
        """
        return len(self._title) + 2

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
    def __init__(self, screen, tab_group, *args, color="GOOD", **kwargs):
        kwargs["max_height"] = 1
        kwargs["editable"] = False
        npyscreen.widget.Widget.__init__(self, screen, *args, **kwargs)
        self.color = color
        self._label = None
        self._tab_group = tab_group

    def set_label(self, label):
        """
        Set label of the base.

        :return:
        """
        if label is not None:
            self._label = "{} {} ".format(label, "\u25C2\u25C2\u25C2")
        else:
            self._label = None

    def _get_tabs_width(self):
        """
        Summarise tabs widths and spaces between.

        :return:
        """
        width = 0
        for tab in self._tab_group.get_tabs():
            width += tab.tab_width()
        return width + self._tab_group.space

    def update(self, clear=True):
        line = "\u2588" * self.width
        self.add_line(self.rely, self.relx, line,
                      self.make_attributes_list(line, self.parent.theme_manager.findPair(self, self.color)), self.width)

        line = "\u2582" * self.width
        self.add_line(self.rely - 1, self.relx, line,
                      self.make_attributes_list(line, self.parent.theme_manager.findPair(self, self.color)), 2)
        offset = self._get_tabs_width()
        self.add_line(self.rely - 1, self.relx + offset, line,
                      self.make_attributes_list(line, self.parent.theme_manager.findPair(self, self.color)),
                      self.width - offset)

        if self._label is not None:
            self.add_line(self.rely, self.relx + self.width - len(self._label), self._label, self.make_attributes_list(
                self._label, self.parent.theme_manager.findPair(self, self.color) | curses.A_STANDOUT), self.width)


class TabController:
    """
    Tabs widget controller. Used to switch between tabs.
    """
    class TabContainer:
        """
        Tab container.
        """
        def __init__(self, screen):
            self.__screen = screen
            self.__widgets = []

        def add_widget(self, *args, **kwargs):
            """
            Add a widget to the tab container:

            Typical npyscreen's way:

                F = npyscreen.Form(....)
                F.add(npyscreen.Text .....)

            So is translated:

                F = npyscreen.Form(....)
                group = TabGroup(F)
                group.get_tab_container(some_id).add_widget(npyscreen.Text ....)

            :param widget:
            :return:
            """
            widget = self.__screen.add(*args, **kwargs)
            if widget not in self.__widgets:
                self.__widgets.append(widget)
            return widget

        def get_widgets(self):
            """
            Get widgets in the container.

            :return:
            """
            for widget in self.__widgets:
                yield widget

    def __init__(self, screen):
        self.__screen = screen
        self.__tab_widgets_map = {}

    def create_controller(self, tab_id):
        """
        Create tab controller for widgets.

        :param tab_id:
        :return:
        """
        self.__tab_widgets_map.setdefault(tab_id, TabController.TabContainer(self.__screen))

    def add(self, tab_id, *args, **kwargs):
        """
        Add a widget to a tab.

        :param tab_id:
        :param args:
        :param kwargs:
        :return:
        """
        if tab_id not in self.__tab_widgets_map:
            raise KeyError("Please first create a tab controller for the ID '{}'.".format(tab_id))

        self.__tab_widgets_map[tab_id].add_widget(self.__screen.add(*args, **kwargs))

    def get_tab(self, tab_id):
        """
        Get a tab controller.

        :param tab_id:
        :return:
        """
        return self.__tab_widgets_map[tab_id]

    def show_tab(self, tab_id, *args, **kwargs):
        """
        Show widgets on the tab.

        :param tab_id:
        :return:
        """
        # npyscreen always only paints on top. So there is no really "memory" thing.
        # Thus "clear(True)" means "paint everything over". Thus we need first
        # paint background everything, then paint what needs to be shown.

        # Hide all first
        for tid in self.__tab_widgets_map:
            for widget in self.__tab_widgets_map[tid].get_widgets():
                widget.hidden = True
                widget.update(clear=widget.hidden)

        # Now show what needs to be shown
        for widget in self.__tab_widgets_map[tab_id].get_widgets():
            widget.hidden = False
            widget.update()


class TabGroup:
    """
    Tab group.
    """
    def __init__(self, screen, relx, rely, space=3):
        self.tabs = []
        self.space = space
        self.relx = relx
        self.rely = rely
        self.screen = screen
        self.base = self.screen.add(TabGroupBase, tab_group=self, relx=self.relx, rely=self.rely + 1)
        self.__first_init = True
        self.__tab_controller = TabController(self.screen)

    def get_tabs(self):
        """
        Return tab objects.

        :return:
        """
        for tab, label in self.tabs:
            yield tab

    def add_tab(self, tid, tab: TabButton, label: str = None, callbacks: list = None):
        """
        Add a tab object to the group.

        :param tab:
        :param callbacks: list of callbacks. Each callback is a tuple of (func, args, kwargs).
        :return:
        """
        if not callbacks:
            callbacks = []
        callbacks.append((self.__tab_controller.show_tab, tid, None))
        self.tabs.append((tab, label))
        self.__tab_controller.create_controller(tab_id=tid)
        tab._tab_group = self
        for callback in callbacks or []:
            callback, args, kwargs = callback
            tab.add_callback(callback, args, kwargs)

    def get_tab_container(self, tid):
        """
        Get tab by id.

        :param tid:
        :return:
        """
        return self.__tab_controller.get_tab(tab_id=tid)

    def align(self):
        """
        Align group on the canvas.

        :return:
        """
        offset = 0
        for tab, label in self.tabs:
            tab.rely = self.rely
            tab.relx = self.relx + offset + 1
            offset += tab.width + self.space

        # Pre-select first tab on first init
        if self.__first_init and self.tabs:
            tab, label = next(iter(self.tabs))
            tab._on_tab_select(10)
            self.__first_init = False

    def on_tab_select(self, tab_id):
        """
        Select current tab.

        :param tab_id:
        :return:
        """
        for tab, label in self.tabs:
            if tab.id == tab_id:
                self.base.set_label(label)
                tab.set_active(True)
            else:
                tab.set_active(False)

        self.base.update()

        for tab, label in self.tabs:
            tab.update()
