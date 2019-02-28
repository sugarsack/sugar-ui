# coding: utf-8
"""
Main dashboard
"""
import sys
import curses
import npyscreen
from sugarui.widgets.progressbar import ProgressBar


class Dashboard(npyscreen.FormBaseNewWithMenus):
    """
    Dashboard form.
    """
    id = "MAIN"

    def __init__(self, *args, **kwargs):
        npyscreen.FormBaseNewWithMenus.__init__(self, *args, **kwargs)
        self.w_root_menu = None
        self.w_progressbar = None

    def create_menu(self):
        """
        Create menus

        :return:
        """
        self.w_root_menu = self.add_menu(name="Main", shortcut="^M")
        self.w_root_menu.addItemsFromList([
            ("Display Text".ljust(30), None, "a"),
            ("Just beep".ljust(30), self.on_beep, "^E"),
            ("Exit".ljust(30), self.on_exit, "^Q"),
        ])

        self.m2 = self.add_menu(name="Another Menu", shortcut="b", )
        self.m2.addItemsFromList([
            ("Just Beep", self.on_beep),
        ])

        self.m3 = self.m2.addNewSubmenu("A sub menu", "^F")
        self.m3.addItemsFromList([
            ("Just Beep", self.on_beep),
        ])

    def create(self):
        """
        Create form

        :return:
        """
        self.w_progressbar = self.add(ProgressBar, name="Progress", editable=True, max_height=3)
        self.create_menu()

    def on_beep(self):
        curses.beep()

    def on_exit(self):
        self.editing = False
        self.parentApp.switchFormNow()
        sys.exit(1)
