# coding: utf-8
"""
Dropdown select list is to choose something
from a pop-up window below.
"""
import curses
import npyscreen
from sugarui.widgets.buttons import ClickButton



class _DropDownTextItem(npyscreen.Textfield):
    """
    Text item in the drop down list.
    """
    def update(self, clear=True, cursor=True):
        state = curses.A_STANDOUT | curses.A_BOLD | curses.A_DIM if self.editing or self.highlight else curses.A_NORMAL

        background = " " * self.width
        self.add_line(self.rely, self.relx, background,
                      self.make_attributes_list(background, self.parent.theme_manager.findPair(self, self.color) | state),
                      self.width)
        if self.value:
            self.add_line(self.rely, self.relx + 1, self.value, self.make_attributes_list(
                self.value, self.parent.theme_manager.findPair(self, self.color) | state), self.width)


class _DropDownItems(npyscreen.MultiLine):
    """
    Drop down items render.
    """
    _contained_widgets = _DropDownTextItem

    def __init__(self, *args, **kwargs):
        npyscreen.MultiLine.__init__(self, *args, **kwargs)
        self.__callbacks = []

    def add_callback(self, callback):
        """
        Add callback for "on_select".

        :param callback:
        :return:
        """
        self.__callbacks.append(callback)

    def h_select(self, ch):
        """
        Invoke callable.

        :param ch:
        :return:
        """
        for callback in self.__callbacks:
            callback(self.values[self.cursor_line])
        self.editing = False


class _DropDownPopup(npyscreen.fmForm.FormBaseNew):
    """
    Drop-down popup.
    """
    DEFAULT_LINES = 25
    DEFAULT_COLUMNS = 60
    SHOW_ATX = 0
    SHOW_ATY = 0
    COLOR = "CURSOR_INVERSE"

    def __init__(self, parent, *args, **kwargs):
        npyscreen.fmForm.FormBaseNew.__init__(self, *args, **kwargs)

        # TODO: override height, so we take more space
        self.callbacks = []
        self.value = False
        self.w_select_label = self.add(npyscreen.Textfield, value="Select:", relx=2, rely=1, editable=False)

        noitems_label = "No items to select."
        self.w_no_items_label = self.add(npyscreen.Textfield, value=noitems_label,
                                         relx=self.columns // 2 - (len(noitems_label) // 2),
                                         rely=self.lines // 2 - 1, editable=False)

        self.items = self.add(_DropDownItems, color=self.color, widgets_inherit_color=True, rely=2)
        self.items.add_callback(self.on_item_select)
        self.parent = parent

        self.close_button = self.add(ClickButton, label="Close", width=10,
                                     relx=self.columns // 2 - 5, rely=self.lines - 2)
        self.close_button.add_callback(self.on_item_select)

    def add_callback(self, callback):
        """
        Add value passing callback.

        :param callback:
        :return:
        """
        self.callbacks.append(callback)

    def on_item_select(self, value):
        """
        On item select.

        :param value:
        :return:
        """
        for callback in self.callbacks:
            callback(value)
        self.editing = False

    def show(self):
        """
        Show form.

        :return:
        """
        empty = not self.items.values

        self.items.hidden = empty
        self.items.update(clear=empty)
        self.w_select_label.hidden = empty
        self.w_select_label.update(clear=empty)

        for helper_widget in [self.close_button, self.w_no_items_label]:
            helper_widget.hidden = not empty
            helper_widget.update(clear=not empty)

        self.edit()


class DropDown(npyscreen.widget.Widget):
    """
    Drop-down.
    """
    def __init__(self, screen, *args, label_max_width=None, **kwargs):
        kwargs["screen"] = screen
        kwargs["color"] = "CAUTIONHL"
        self.label = kwargs.get("label")
        if self.label:
            if label_max_width is not None:
                self.label = self.label.ljust(label_max_width)[:label_max_width]
            screen.add(npyscreen.Textfield, value=self.label, relx=kwargs["relx"], rely=kwargs["rely"],
                       max_width=len(self.label) + 1, color="CAUTION", editable=False)
            kwargs["relx"] = kwargs["relx"] + len(self.label) + 1
        npyscreen.widget.Widget.__init__(self, *args, **kwargs)
        self.screen = screen
        self.handlers[10] = self.on_select
        self.value = None
        self._dropdown_values = []
        self._callbacks = []

    def add_callback(self, callback):
        """
        Add value select callback.

        :param callback:
        :return:
        """
        self._callbacks.append(callback)

    def add_values(self, *values):
        """
        Add values to the dropdown.

        :param values:
        :return:
        """
        self._dropdown_values += values

    def _field_space(self):
        """
        Create a field space.

        :return:
        """
        color = self.parent.theme_manager.findPair(self, self.color) | curses.A_STANDOUT | curses.A_BOLD
        if not self.editing:
            color = color | curses.A_DIM

        line = " " * self.width
        self.add_line(self.rely, self.relx, line, self.make_attributes_list(line, color), self.width)

        if self.editing:
            line = "[\u25BC]"
            self.add_line(self.rely, self.relx + self.width - 3, line, self.make_attributes_list(line, color), 3)

    def update(self, clear=True):
        """
        Update the screen.

        :param clear:
        :return:
        """
        # TODO: Add "V" and "^" chars at the end of the field (Unicode) to indicate it is a dropdown
        self._field_space()
        state = (curses.A_DIM if self.editing else curses.A_NORMAL) | curses.A_STANDOUT | curses.A_BOLD | curses.A_DIM
        if self.value:
            self.add_line(self.rely, self.relx, self.value, self.make_attributes_list(
                self.value, self.parent.theme_manager.findPair(self, self.color) | state), self.width)

    def on_return_value(self, value):
        """
        On return value.

        :param value:
        :return:
        """
        self.value = value
        for callback in self._callbacks:
            callback(self.value)

    def on_select(self, *args, **kwargs):
        """
        On select value.

        :param args:
        :param kwargs:
        :return:
        """
        popup = _DropDownPopup(self, show_atx=self.relx, show_aty=self.rely + 1,
                               lines=10, columns=self.width, color="VERYGOOD")
        if self._dropdown_values:
            popup.items.values = self._dropdown_values
            popup.add_callback(self.on_return_value)
        popup.show()

