# coding: utf-8
"""
Basic forms.
This overrides npyscreen's forms, allowing concurrent widget updates.
"""

import npyscreen


class MainForm(npyscreen.FormBaseNewWithMenus):
    """
    Main form with the menus.
    """
    id = "MAIN"

    def __init__(self, *args, **kwargs):
        npyscreen.FormBaseNewWithMenus.__init__(self, *args, **kwargs)

        # This must be called in the constructor,
        # otherwise events don't see the widgets.
        self.init()

    def init(self):
        """
        Create form.

        :return:
        """
        raise NotImplementedError("This method should be overridden")
