# coding: utf-8
"""
Radio choice for either or any choice.
This is drawing something like:

My Choices:  ( ) One
             (*) Of there
             ( ) Three

2b or !2b:   [x] Boolean
"""
import curses
import npyscreen


class _ConstrainedOption(npyscreen.widget.Widget):
    """
    Radio choice widget, where only one can be selected
    """
    LABEL_RADIO_SELECTED = "\u26AB"
    LABEL_RADIO_NOT_SELECTED = "\u26AA"

    LABEL_OPT_SELECTED = "\u25FC"
    LABEL_OPT_NOT_SELECTED = "\u25FB"

    def __init__(self, screen, *args, **kwargs):
        self._screen = screen
        self.selected = False
        self.highlighted = False
        self.value = None
        self._type = RadioChoice.TYPE_RADIO
        kwargs["max_height"] = 1
        kwargs["screen"] = screen
        npyscreen.widget.Widget.__init__(self, *args, **kwargs)

    def update(self, clear=True):
        """
        Update the widget.

        :param clear:
        :return:
        """
        super(_ConstrainedOption, self).update(clear=clear)
        state = curses.A_BOLD if self.highlighted else curses.A_NORMAL
        if self.value:
            if self._type == RadioChoice.TYPE_RADIO:
                pre_label = (self.LABEL_RADIO_SELECTED if self.selected else self.LABEL_RADIO_NOT_SELECTED)
            else:
                pre_label = (self.LABEL_OPT_SELECTED if self.selected else self.LABEL_OPT_NOT_SELECTED)
            render = "{pl}   {lb}".format(pl=pre_label, lb=self.value)
            self.color = "CAUTION" if self.selected else "NORMAL"
            self.add_line(self.rely, self.relx, render,
                          self.make_attributes_list(
                              render, self.parent.theme_manager.findPair(self, self.color) | state),
                          self.width)


class RadioChoice(npyscreen.MultiLine):
    """
    Radio choice container widget.
    """
    _contained_widgets = None

    TYPE_RADIO = 1
    TYPE_OPTION = 2

    def __init__(self, screen, type=TYPE_RADIO, *args, **kwargs):
        self._type = type
        self._contained_widgets = _ConstrainedOption
        kwargs["screen"] = screen
        self._my_widgets = []
        npyscreen.MultiLine.__init__(self, *args, **kwargs)

    def get_height(self):
        """
        Return actual painted hight.

        :return:
        """
        return len(self.values)

    def make_contained_widgets(self):
        """
        Fill-in multi-line container.

        :return:
        """
        self._my_widgets = []
        for h in range(self.height // self.__class__._contained_widget_height):
            widget = self._contained_widgets(self.parent, rely=(h*self._contained_widget_height)+self.rely,
                                             relx = self.relx, max_width=self.width,
                                             max_height=self.__class__._contained_widget_height)
            widget._type = self._type
            self._my_widgets.append(widget)

    def load_values(self, *values):
        """
        Add values, resize the whole thing.
        :param values:
        :return:
        """
        self.values = values
        self.max_height = len(self.values) + 1

    def h_exit(self, ch):
        """
        On losing focus.

        :param ch:
        :return:
        """
        super(RadioChoice, self).h_exit(ch)
        for idx, widget in enumerate(self._my_widgets):
            widget.highlighted = False
            widget.update()

    def h_select(self, ch):
        """
        On select.

        :param ch:
        :return:
        """
        super(RadioChoice, self).h_select(ch)
        for idx, widget in enumerate(self._my_widgets):
            if self._type == self.TYPE_RADIO:
                widget.selected = self.cursor_line == idx
            else:
                if self.cursor_line == idx:
                    widget.selected = not widget.selected
            widget.update()
            self.value = self.values[self.cursor_line]

    def update(self, clear=True):
        """
        Event on widget update (repaint).

        :param clear:
        :return:
        """
        super(RadioChoice, self).update(clear=clear)

        if not clear:
            for idx, widget in enumerate(self._my_widgets):
                widget.highlighted = self.cursor_line == idx and self.editing
                widget.update()
