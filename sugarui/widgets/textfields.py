# coding: utf-8
"""
Text fields class.
These are used to display some data in the tables.
"""
import curses
import npyscreen


class ColoredTextField(npyscreen.Textfield):
    """
    Colorised text field.
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
