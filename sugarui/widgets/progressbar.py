# coding: utf-8
"""
Progress bar widget
"""
import curses
import npyscreen


class ProgressBar(npyscreen.wgwidget.Widget):
    """
    Progress bar
    """
    def __init__(self, *args, **kwargs):
        npyscreen.wgwidget.Widget.__init__(self, *args, **kwargs)
        self.max_height = 1
        self.value = 43

    def update(self, clear=True):
        """
        On widget redraw.

        :param clear:
        :return:
        """
        if clear: self.clear()
        if self.hidden:
            self.clear()
            return False

        background = "\u2591" * self.width
        self.add_line(self.rely, self.relx, background,
                      self.make_attributes_list(background, curses.A_NORMAL), self.width)

        filled = "\u2588" * int(self.width * float(self.value / 100))
        self.add_line(self.rely, self.relx, filled,
                      self.make_attributes_list(filled, curses.A_BOLD), self.width)

        label = "{}%".format(self.value).rjust(4)
        self.add_line(self.rely, self.relx + self.width - 4, label,
                      self.make_attributes_list(label, curses.A_NORMAL), self.width)

    def set_value(self, value):
        """
        Set percentage value.

        :param value:
        :return:
        """
        self.value = value
        self.display()
