# coding: utf-8
"""
Vertical divider.
"""
import curses
import npyscreen


class Divider(npyscreen.widget.Widget):
    """
    Adds an empty space.
    Allows text and line(s)
    """
    BG_DIM_25 = 1
    BG_DIM_50 = 2
    BG_DIM_75 = 3
    BG_DOUBLE_LINE = 4
    BG_LINE = 5
    BG_THIN_LINE = 6
    BG_THICK_LINE = 7
    BG_THIN_DOTLINE = 8
    BG_THICK_DOTLINE = 9
    BG_THIN_DASHLINE = 10
    BG_THICK_DASHLINE = 11
    BG_THIN_LDASHLINE = 12
    BG_THICK_LDASHLINE = 13
    BG_BOTTOM_THIN_BLOCK = 14
    BG_TOP_THIN_BLOCK = 15

    __backgrounds = {
        None: " ",
        BG_DIM_25: "\u2591",
        BG_DIM_50: "\u2592",
        BG_DIM_75: "\u2593",
        BG_BOTTOM_THIN_BLOCK: "\u2581",
        BG_TOP_THIN_BLOCK: "\u2594",
        BG_DOUBLE_LINE: "\u2550",
        BG_THIN_LINE: "\u2500",
        BG_THICK_LINE: "\u2501",
        BG_THIN_DOTLINE: "\u2508",
        BG_THICK_DOTLINE: "\u2509",
        BG_THIN_DASHLINE: "\u2504",
        BG_THICK_DASHLINE: "\u2505",
        BG_THIN_LDASHLINE: "\u254C",
        BG_THICK_LDASHLINE: "\u254D",
    }

    def __init__(self, screen, *args, title=None, background=None, **kwargs):
        kwargs["screen"] = screen
        kwargs["max_height"] = 1
        kwargs["editable"] = False
        npyscreen.widget.Widget.__init__(self, *args, **kwargs)
        self._title = title
        self._background = background

    def update(self, clear=True):
        """
        Update widget.

        :param clear:
        :return:
        """
        background = self.__backgrounds[self._background] * self.width
        self.add_line(self.rely, self.relx, background,
                      self.make_attributes_list(background, self.parent.theme_manager.findPair(self, self.color)),
                      self.width)

        if self._title:
            label = " {} ".format(self._title)
            if not self._background:
                label = label.strip()
            self.add_line(self.rely, self.relx + 2, label,
                          self.make_attributes_list(label,
                                                    self.parent.theme_manager.findPair(
                                                        self, self.color) | curses.A_BOLD), len(label))
