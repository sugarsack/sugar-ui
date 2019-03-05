# coding: utf-8
"""
Text fields class.
These are used to display some data in the tables.
"""
import curses
import npyscreen


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
            color = color | curses.A_STANDOUT | curses.A_BOLD | curses.A_DIM
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
