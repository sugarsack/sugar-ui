# coding: utf-8
"""
Checkbox widget.
"""
import curses
import curses.ascii
import npyscreen


class CheckBox(npyscreen.widget.Widget):
    """
    Checkbox implementation.
    """
    LABEL_SELECTED = "\u25FC"
    LABEL_NOT_SELECTED = "\u25FB"

    def __init__(self, screen, *args, label=None, label_margin=23, **kwargs):
        kwargs["max_height"] = kwargs.get("max_height") or 1
        if kwargs["max_height"] > 2:
            kwargs["max_height"] = 2

        kwargs["screen"] = screen
        npyscreen.widget.Widget.__init__(self, *args, **kwargs)

        self.label = label
        self.label_margin = label_margin
        self.value = False

        self.handlers.update({
            curses.ascii.SP: self.h_select,
            curses.ascii.CR: self.h_select,
            10: self.h_select,
        })

    def h_select(self, ch):
        """
        Event on widget select.

        :param ch:
        :return:
        """
        self.value = not self.value

    def update(self, clear=True):
        """
        Widget update.

        :param clear:
        :return:
        """
        if self.hidden and clear:
            self.clear()
            return

        super(CheckBox, self).update(clear=clear)

        state = curses.A_BOLD if self.editing else curses.A_NORMAL
        label = self.label.ljust(self.label_margin) if self.label else ""
        render = "{lbl}{val}".format(lbl=len(label) * " ",
                                     val=self.value and self.LABEL_SELECTED or self.LABEL_NOT_SELECTED)

        self.add_line(self.rely, self.relx, render,
                      self.make_attributes_list(
                          render, self.parent.theme_manager.findPair(
                              self, self.value and "CAUTION" or "NORMAL") | state),
                      self.width)
        if self.label:
            self.add_line(self.rely, self.relx, label,
                          self.make_attributes_list(
                              label, self.parent.theme_manager.findPair(self, "IMPORTANT") | state),
                          self.width)
