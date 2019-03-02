# coding: utf-8
"""
Table display
"""
import time
import curses
import npyscreen
import npyscreen.wgwidget
from sugarui.widgets.textfields import ColoredTextField


class TableUtilMixin:
    """
    Mix-in for common utilities.
    """
    C_HR_L = "\u2501"
    C_VR_L = "\u2503"
    C_VH_L = "\u252f"
    C_ELPS = "\u2026"
    C_V_HALF_DOWN = "\u2577"
    C_B_HALF_DOWN = "\u2584"

    def _get_cell_width(self):
        """
        Return max inner width of the cell.

        :return:
        """
        return (self.width - self._columns - 3) // self._columns

    def _fit_text_in_cell(self, text):
        """
        Fit text into a cell. It will truncate text with
        elipsis, if text is bigger.

        :param text:
        :return:
        """
        if not text:
            text = "N/A"
        text = " {} ".format(text.strip())

        cell_width = self._get_cell_width()
        text_width = len(text)
        if text_width > cell_width:
            text = " {} ".format(text[:cell_width - 2].strip() + self.C_ELPS)
        text = text.ljust(cell_width)

        return text


class TableHeader(npyscreen.wgwidget.Widget, TableUtilMixin):
    """
    Table header.
    """
    def __init__(self, *args, headers=None, **kwargs):
        """
        Table header.

        :param args: npyscreen-related
        :param headers: List of strings
        :param kwargs: npyscreen-related
        """
        npyscreen.wgwidget.Widget.__init__(self, *args, **kwargs)
        self.max_height = 1
        self._headers = headers
        self._columns = len(self._headers)
        self._min_width = (len(self._headers) * 6) + (len(self._headers) - 2)

    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False

        name = []
        for idx, header in enumerate(self._headers):
            name.append(self._fit_text_in_cell(header))
            if idx + 1 < self._columns:
                name.append(self.C_V_HALF_DOWN)
        name.append(" ")
        name = "".join(name).strip().ljust(self.width - 1).rjust(self.width)
        color = curses.color_pair(5)  # Already curses-initialised pair. 0-9 normal, 10-20 are bold
        self.add_line(self.rely + 1, self.relx, name,
                      self.make_attributes_list(name, curses.A_REVERSE | curses.A_BOLD | color), self.width - 1)

        name = self.C_B_HALF_DOWN * (self.width - 1)
        self.add_line(self.rely, self.relx, name, self.make_attributes_list(name, color), self.width)


class Table(npyscreen.MultiLineAction):
    """
    Table view.
    """
    def __init__(self, *args, columns=0, **keywords):
        self.cell_highlight_map = {
            "offline": "CRITICAL",
            "online": "IMPORTANT",
        }

        super(Table, self).__init__(*args, **keywords)
        self.add_handlers({
            "^V": self.on_add_record,
            curses.KEY_ENTER: self.on_view_record,
            10: self.on_view_record,
        })

    def handle_input(self, _input):
        super(Table, self).handle_input(_input)

    def on_add_record(self, *args, **kwargs):
        self.values.append(time.strftime("%T %D"))
        self.display()

    def h_select(self, ch):
        """
        Select current row.

        :return:
        """
        super(npyscreen.MultiLineAction, self).h_select(ch)
        for idx, widget in enumerate(self._my_widgets):
            widget.syntax_highlighting = idx != self.value

    def on_view_record(self, *args, **kwargs):
        """
        View record.

        :return:
        """
        self.h_select(None)

    def display_value(self, val):
        """
        Display value formatter.

        :param val:
        :return:
        """
        #w, h = self.width, self.height
        w = self.max_width
        status = val == "two" and "offline" or "online"
        return " {} {} {} ".format(val.rjust(10), "\u2502", status).ljust(w)

    def make_contained_widgets(self):
        """
        Create visible view of the widgets.
        :return:
        """
        self._my_widgets = []
        for height in range(self.height // self.__class__._contained_widget_height):
            row_widget = ColoredTextField(
                self.parent, rely=(height * self._contained_widget_height) + self.rely,
                relx=self.relx, max_width=self.width, max_height=self.__class__._contained_widget_height)
            row_widget.highlight_map = self.cell_highlight_map
            self._my_widgets.append(row_widget)


class TitledTable(npyscreen.BoxTitle):
    _contained_widget = Table
