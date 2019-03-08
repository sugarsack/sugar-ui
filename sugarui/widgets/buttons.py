# coding: utf-8
"""
Enhanced npyscreen buttons.
"""
import curses
import curses.ascii
import npyscreen


class ClickButton(npyscreen.widget.Widget):
    """
    Button with callback
    """
    def __init__(self, *args, **kwargs):
        kwargs["color"] = "CAUTION"
        npyscreen.widget.Widget.__init__(self, *args, **kwargs)
        self.handlers.update({
                curses.ascii.NL: self.on_press,
                curses.ascii.CR: self.on_press,
            })
        self._callbacks = []
        self._width = kwargs.get("width")
        self._label = kwargs.get("label", "Button Label")
        if self._width is None:
            self._width = len(self._label) + 4

    def _render_label(self):
        if self.editing:
            tpl = "\u25B8 {} \u25C2"
        else:
            tpl = "[ {} ]"
        return tpl.format(self._label.center(self._width - 4, " "))

    def add_callback(self, callback):
        """
        Add button callback.
        :param callback:
        :return:
        """
        self._callbacks.append(callback)

    def on_press(self, ch):
        """
        Invoke callbacks on the button press.

        :return:
        """
        for callback in self._callbacks:
            callback(ch)

    def update(self, clear=False):
        super(ClickButton, self).update(clear=clear)

        state = curses.A_BOLD if self.editing else curses.A_NORMAL | curses.A_DIM
        state = state | curses.A_STANDOUT
        label = self._render_label()
        self.add_line(self.rely, self.relx, label,
                      self.make_attributes_list(label, self.parent.theme_manager.findPair(self, self.color) | state),
                      self.width)
