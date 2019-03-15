# coding: utf-8
"""
Text fields class.
These are used to display some data in the tables.
"""
import curses
import npyscreen
from sugarui.windows.floating import ErrorMessageForm


class ColoredTextField(npyscreen.Textfield):
    """
    Colorised text field (highlighted data)
    """
    syntax_highlighting = True

    def __init__(self, *args, **kwargs):
        npyscreen.Textfield.__init__(self, *args, **kwargs)
        self.syntax_highlighting = True
        self.highlight_map = {}

    def colorise(self):
        """
        On the current value highlight string that has value.

        :param value: Value to highlight.
        :return:
        """
        if self.value:
            hldata = [curses.A_NORMAL for _ in range(len(self.value))]
            for value in self.highlight_map:
                offset = self.value.find(value)
                if offset > -1:
                    hl_colorc = self.parent.theme_manager.findPair(self, self.highlight_map[value])
                    hldata = hldata[:offset] + [hl_colorc for _ in range(len(value))] + hldata[offset + len(value):]
            self._highlightingdata = hldata
            del hldata

    def update(self, clear=True, cursor=True):
        """
        On update.
        :param clear:
        :param cursor:
        :return:
        """
        self.colorise()
        super(npyscreen.Textfield, self).update(clear, cursor)


class VisualTextField(npyscreen.Textfield):
    """
    Text field with colored background.
    """
    def __init__(self, *args, **kwargs):
        kwargs["color"] = "CAUTIONHL"
        kwargs["max_height"] = 1
        npyscreen.Textfield.__init__(self, *args, **kwargs)

    def _print(self):
        """
        Create text content within the field.

        :return:
        """
        self._field_space()
        width_of_char_to_print = 0

        string_to_print = self._get_string_to_print()
        if not string_to_print:
            return None

        string_to_print = self.display_value(self.value)[
                          self.begin_at:self.maximum_string_length + self.begin_at - self.left_margin]

        column = 0
        place_in_string = 0
        if self.syntax_highlighting:
            self.update_highlighting(start=self.begin_at,
                                     end=self.maximum_string_length + self.begin_at - self.left_margin)
            while column <= (self.maximum_string_length - self.left_margin):
                if not string_to_print or place_in_string > len(string_to_print) - 1:
                    break
                width_of_char_to_print = self.find_width_of_char(string_to_print[place_in_string])
                if column - 1 + width_of_char_to_print > self.maximum_string_length:
                    break
                try:
                    highlight = self._highlightingdata[self.begin_at + place_in_string]
                except IndexError:
                    highlight = curses.A_NORMAL
                self.parent.curses_pad.addstr(self.rely, self.relx + column + self.left_margin,
                                              self._print_unicode_char(string_to_print[place_in_string]),
                                              highlight)
                column += self.find_width_of_char(string_to_print[place_in_string])
                place_in_string += 1
        else:
            color = self._get_color()
            while column <= (self.maximum_string_length - self.left_margin):
                if not string_to_print or place_in_string > len(string_to_print) - 1:
                    if self.highlight_whole_widget:
                        self.parent.curses_pad.addstr(self.rely, self.relx + column + self.left_margin, ' ', color)
                        column += width_of_char_to_print
                        place_in_string += 1
                        continue
                    else:
                        break

                width_of_char_to_print = self.find_width_of_char(string_to_print[place_in_string])
                if column - 1 + width_of_char_to_print > self.maximum_string_length:
                    break
                self.parent.curses_pad.addstr(self.rely, self.relx + column + self.left_margin,
                                              self._print_unicode_char(string_to_print[place_in_string]), color)
                column += width_of_char_to_print
                place_in_string += 1

    def _field_space(self):
        """
        Create a field space.

        :return:
        """
        line = " " * self.width
        self.add_line(self.rely, self.relx, line, self.make_attributes_list(
            line, self.parent.theme_manager.findPair(
                self, self.color) | curses.A_STANDOUT | curses.A_BOLD | curses.A_DIM), self.width)

    def _get_color(self):
        """
        Get color.

        :return:
        """
        if self.do_colors():
            if self.show_bold and self.color == 'DEFAULT':
                color = self.parent.theme_manager.findPair(self, 'BOLD') | curses.A_BOLD
            elif self.show_bold:
                color = self.parent.theme_manager.findPair(self, self.color) | curses.A_BOLD
            elif self.important:
                color = self.parent.theme_manager.findPair(self, 'IMPORTANT') | curses.A_BOLD
            else:
                color = self.parent.theme_manager.findPair(self)
        else:
            if self.important or self.show_bold:
                color = curses.A_BOLD
            else:
                color = curses.A_NORMAL
        return color | curses.A_STANDOUT | curses.A_BOLD | curses.A_DIM


class RangeVisualTextField(VisualTextField):
    """
    Visual text field that supports integer/float ranges.
    """
    def __init__(self, screen, value, *args, range=(0, 100), **kwargs):
        self.range = range
        self._value = value
        kwargs["screen"] = screen
        VisualTextField.__init__(self, *args, **kwargs)
        self.screen = screen

    def get_value(self):
        """
        Get numeric value.

        :return:
        """
        if self.value:
            try:
                value = (int if "." in self.value else float)(self.value)
            except ValueError:
                msg = "Value should be a number."
                alert = ErrorMessageForm(msg, len(msg) + 6, 6, passive_text=True, name="Error")
                alert.center_on_display()
                alert.edit()
                value = 0
        else:
            value = 0

        return value

    def check_value(self):
        """
        Check if value is within the range.

        :return:
        """
        value = self.get_value()
        if self.range:
            low, high = self.range
            if not low <= value <= high:
                if not self.editing:
                    msg = "Value should be within the range from {} to {}.".format(*self.range)
                    alert = ErrorMessageForm(msg, len(msg) + 6, 6, passive_text=True, name="Error")
                    alert.center_on_display()
                    alert.edit()

    def h_exit_down(self, _input):
        """
        Exit editing mode downwards.

        :param _input:
        :return:
        """
        super(RangeVisualTextField, self).h_exit_down(_input)
        self.check_value()

    def h_exit_up(self, _input):
        """
        Exit editing mode upwards.

        :param _input:
        :return:
        """
        super(RangeVisualTextField, self).h_exit_up(_input)
        self.check_value()

    def h_exit_left(self, _input):
        """
        Exit editing mode left.

        :param _input:
        :return:
        """
        super(RangeVisualTextField, self).h_exit_left(_input)
        self.check_value()

    def h_exit_right(self, _input):
        """
        Exit editing mode right.

        :param _input:
        :return:
        """
        super(RangeVisualTextField, self).h_exit_right(_input)
        self.check_value()

    def h_exit_escape(self, _input):
        """
        Exit editing mode at ESC key.

        :param _input:
        :return:
        """
        super(RangeVisualTextField, self).h_exit_escape(_input)
        self.check_value()

    def h_exit_mouse(self, _input):
        """
        Exit editing mode at mouse handler clicked elsewhere.

        :param _input:
        :return:
        """
        super(RangeVisualTextField, self).h_exit_mouse(_input)
        self.check_value()


class ConcealedVisualTextField(VisualTextField):
    """
    Concealed text field (for passwords and sensitive info)
    """
    MASK_CHAR = "\u25CF"

    def __init__(self, screen, *args, mask=MASK_CHAR, **kwargs):
        self.screen = screen
        kwargs["screen"] = screen
        VisualTextField.__init__(self, *args, **kwargs)
        self._mask = mask or self.MASK_CHAR
        assert len(self._mask) == 1, "Mask is should be one character."

    def _print(self):
        """
        Display value in the entry field.

        :return:
        """
        self._field_space()
        color = self._get_color()

        strlen = len(self.value)
        if self.maximum_string_length < strlen:
            tmp_x = self.relx
            for i in range(self.maximum_string_length):
                self.parent.curses_pad.addch(self.rely, tmp_x, self._mask, color)
                tmp_x += 1

        else:
            tmp_x = self.relx
            for i in range(strlen):
                self.parent.curses_pad.addstr(self.rely, tmp_x, self._mask, color)
                tmp_x += 1
