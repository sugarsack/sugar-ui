# coding: utf-8
"""
Table display
"""
import curses
import npyscreen
import npyscreen.wgwidget
from sugarui.widgets.textfields import ColoredTextField

npyscreen.wgmultiline.MORE_LABEL = " \u25B8\u25B8\u25B8 More \u21B4"


class TableUtilMixin:
    """
    Mix-in for common utilities.
    """
    C_LHB_DOWN = "\u2501"       # "━"
    C_LVB_FULL = "\u2503"       # "┃"
    C_LHB_CELL = "\u252f"       # "┯"
    C_ELPS = "\u2026"           # "..."
    C_LVT_HALF_DOWN = "\u2577"  # "╷"
    C_BF_FULL = "\u2588"      # "█"
    C_BF_HALF_DOWN = "\u2584"   # "▄"
    C_LVT_FULL = "\u2502"       # "│"

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


class TableDivider(npyscreen.wgwidget.Widget, TableUtilMixin):
    """
    Vertical table divider.
    """
    def __init__(self, *args, header=True, **kwargs):
        self._header = int(bool(header))  # Usually tables has a header (TableHeader).
                                          # Header has some details on top. If no header specified,
                                          # divider will be painted as just plain vertical divider.
        kwargs["max_width"] = 1
        npyscreen.wgwidget.Widget.__init__(self, *args, **kwargs)

    def update(self, clear=True):
        """
        Widget redraw updates.

        :param clear:
        :return:
        """
        color = curses.color_pair(5)

        div = self.C_LVB_FULL
        if self._header:
            v_start_offset = 2
            self.add_line(self.rely, self.relx, self.C_BF_HALF_DOWN,
                          self.make_attributes_list(self.C_BF_HALF_DOWN, color), 1)
            self.add_line(self.rely + 1, self.relx, div,
                          self.make_attributes_list(div, color | curses.A_REVERSE), 1)
        else:
            v_start_offset = 0

        div = self.C_LVB_FULL
        for y_offset in range(self.height - v_start_offset - 1):
            self.add_line(self.rely + y_offset + v_start_offset,
                          self.relx, div, self.make_attributes_list(div, color), 1)


class TableHeader(npyscreen.wgwidget.Widget, TableUtilMixin):
    """
    Table header.
    """
    def __init__(self, *args, headers=None, color=5, title=None, **kwargs):
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
        self._color = color
        if title:
            self._title = " {} ".format(title)
        else:
            self._title = None

    def update(self, clear=True):
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False

        name = []
        for idx, header in enumerate(self._headers):
            name.append(self._fit_text_in_cell(header))
            if idx + 1 < self._columns:
                name.append(self.C_LVT_HALF_DOWN)
        name.append(" ")
        name = "".join(name).strip().ljust(self.width - 1).rjust(self.width)
        color = curses.color_pair(5)  # Already curses-initialised pair. 0-9 normal, 10-20 are bold
        self.add_line(self.rely + 1, self.relx, name,
                      self.make_attributes_list(name, curses.A_REVERSE | curses.A_NORMAL | color), self.width - 1)

        name = self.C_BF_HALF_DOWN * (self.width - 1)
        self.add_line(self.rely, self.relx, name, self.make_attributes_list(name, color), self.width)

        # Title
        if self._title:
            self.add_line(self.rely, self.relx + 1, self._title,
                          self.make_attributes_list(self._title, curses.color_pair(5)), 20)


class Table(npyscreen.MultiLineAction, TableUtilMixin):
    """
    Table view.
    """
    def __init__(self, *args, highlight_map=None, **keywords):
        self.cell_highlight_map = highlight_map or {}
        self._columns = 0
        super(Table, self).__init__(*args, **keywords)
        self.values = []
        self.add_handlers({
            "^V": self.on_add_record,
            curses.KEY_ENTER: self.on_view_record,
            10: self.on_view_record,
        })

    def handle_input(self, _input):
        super(Table, self).handle_input(_input)

    def on_add_record(self, *args, **kwargs):
        curses.beep()
        self.display()

    def h_select(self, ch):
        """
        Select current row.

        :return:
        """
        super(npyscreen.MultiLineAction, self).h_select(ch)
        for idx, widget in enumerate(self._my_widgets):
            widget.syntax_highlighting = idx != self.value

    def load_data(self, objects) -> None:
        """
        Load data if arbitrary objects.

        Each object will be either displayed by ".title" attribute
        or __str__ conversion.

        :param objects: Objects.
        :return: None
        """
        self.values = []
        for values in objects:
            if len(values) > self._columns:
                self._columns = len(values)
            self.values.append(values)

    def on_view_record(self, *args, **kwargs):
        """
        View record.

        :return:
        """
        self.h_select(None)

    def display_value(self, row_data):
        """
        Display value formatter.

        :param row_data: a list of objects in the cell.
        :return:
        """
        if self._columns:
            cell = []
            for obj in row_data:
                if hasattr(obj, "value"):
                    value = obj.value
                else:
                    value = str(obj)
                cell.append(self._fit_text_in_cell(value))
            cell = self.C_LVT_FULL.join(cell).ljust(self.max_width)
        else:
            cell = str(row_data)
        return cell.ljust(self.width)

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
