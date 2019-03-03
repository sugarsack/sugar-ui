# coding: utf-8
"""
Floating forms
"""
import textwrap
import npyscreen
from sugarui.widgets.utils import make_button_label


class HelpForm(npyscreen.fmActionFormV2.ActionFormV2):
    """
    Floating help form.
    """
    DEFAULT_LINES = 25
    DEFAULT_COLUMNS = 60
    SHOW_ATX = 0
    SHOW_ATY = 0
    COLOR = "CURSOR_INVERSE"

    def __init__(self, text, width, height, *args, autowrap=False, **kwargs):
        self.__class__.SHOW_ATX = (width // 2) - (self.DEFAULT_COLUMNS // 2)
        self.__class__.SHOW_ATY = (height // 2) - (self.DEFAULT_LINES // 2)

        self.value = False

        kwargs["color"] = self.COLOR
        npyscreen.fmActionFormV2.ActionFormV2.__init__(self, *args, **kwargs)
        self.create_control_buttons()

        self.preserve_selected_widget = True
        self._pager = self.add(npyscreen.wgmultiline.Pager, autowrap=autowrap,
                       editable=True, color=self.COLOR, widgets_inherit_color=True)
        self._pager.values = self._set_text(text, autowrap)

    def _set_text(self, text, autowrap):
        """
        Set text.

        :param text:
        :param autowrap:
        :return:
        """
        width = self.__class__.DEFAULT_COLUMNS - 6
        if autowrap:
            text = [text]
        else:
            out = []
            for line in text.split("\n"):
                if len(line) > width:
                    out.extend(textwrap.wrap(line, width) + [""])
                else:
                    out.append(line)
            text = out

        return text

    def create_control_buttons(self):
        """
        Add control button.

        :return:
        """
        label = make_button_label("Close")
        self._add_button('ok_button', self.__class__.OKBUTTON_TYPE, label,
                         0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
                         0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(label), None)

    def on_ok(self):
        """
        Action on OK.

        :return:
        """
        self.value = True
