# coding: utf-8
"""
Dynamic form for display options
"""
import yaml
import npyscreen


class DynamicOverlayForm(npyscreen.fmForm.FormBaseNew):
    """
    Dynamic overlay form.
    """
    DEFAULT_LINES = 25
    DEFAULT_COLUMNS = 60
    SHOW_ATX = 0
    SHOW_ATY = 0
    COLOR = "NORMAL"

    def __init__(self, parent, *args, scheme=None, **kwargs):
        npyscreen.fmForm.FormBaseNew.__init__(self, *args, **kwargs)
        self.callbacks = []
        self.value = False
        self.parent = parent

        text = self.add(npyscreen.Pager, relx=1, rely=1, max_height=5)
        text.values = scheme["description"]

    @staticmethod
    def generate(screen: npyscreen.Form, scheme: list,
                 relx: int, rely: int, padding: list = None) -> 'DynamicOverlayForm':
        """
        Create overlay.

        :param screen: Parent form
        :param scheme: plugin structure/documentation.
        :return: DynamicOverlayForm
        """
        if not padding:
            padding = [0, 0, 0, 0]
        pad_x_r, pad_y_b, pad_x_l, pad_y_t = padding

        height, width = screen.useable_space()
        return DynamicOverlayForm(screen, scheme=scheme, show_atx=relx + pad_x_l, show_aty=rely + pad_y_t,
                                  columns=width-relx - pad_x_r, lines=height - rely - pad_y_b)
