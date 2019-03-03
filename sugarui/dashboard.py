# coding: utf-8
"""
Main dashboard
"""
import sys
import curses

from sugarui.widgets.progressbar import ProgressBar
from sugarui.widgets.table import Table, TableHeader, TableDivider
from sugarui.windows.forms import MainForm
from sugarui.windows.floating import HelpForm


class FormData:
    """
    Form data
    """


class Dashboard(MainForm):
    """
    Dashboard form.
    """

    f_state_process = None
    f_systems_overview = None
    f_modules_run = None
    f_state_run = None

    def init(self):
        """
        Create form layout, place widgets.

        :return:
        """
        # Shortcuts
        self.handlers.update({
            "^Q": self.on_exit,
            "h": self.on_help,
            "?": self.on_help,
        })

        self.f_state_process = FormData()
        self.f_systems_overview = FormData()
        self.f_modules_run = FormData()
        self.f_state_run = FormData()

        # Menu
        self.create_menu()

        # Widgets
        cell_highlight_map = {
            "failed": "DANGER",
            "success": "GOOD",
            "warnings": "WARNING",
        }

        self.add(TableHeader, title="Job History", headers=["Date"], max_height=2, max_width=40, rely=1)
        self.f_state_process.w_jobs_pane = self.add(Table, relx=2, rely=3, max_width=39)

        self.add(TableDivider, relx=41, rely=1)
        self.add(TableHeader, title="Result Details", headers=["Hostname", "Status", "Finished"],
                 color=3, relx=42, max_height=2, rely=1)
        self.f_state_process.w_clients_pane = self.add(Table, relx=42, rely=3, highlight_map=cell_highlight_map)
        self.f_state_process.w_progressbar = self.add(ProgressBar, name="Progress", relx=43,
                                                      editable=False, max_height=3)
        self.load_sample_data()

    def load_sample_data(self):
        import time
        import random
        data = []
        for hostname in ["zoo", "web1", "web2", "web3", "db1", "db2", "middleware", "auth", "kerb", "kerb1",
                         "ldap", "ldap1", "backup", "backup1"]:
            status = random.choice(["success", "failed", "warnings"])
            data.append(("{}.some.lan".format(hostname), status, time.strftime("%T, %D")))
        self.f_state_process.w_clients_pane.load_data(data)

        data = []
        for x in range(10):
            data.append((time.strftime("%T, %D"),))
        self.f_state_process.w_jobs_pane.load_data(data)

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

    def on_beep(self):
        curses.beep()
        import time
        for x in range(100):
            self.f_state_process.w_progressbar.set_value(x + 1)
            time.sleep(0.01)

    def on_help(self, *arga, **kwargs):
        height, width = self.useable_space()
        text = """Sugar Dashboard, v0.0.0

Dashboard UI allows you to see the status of the jobs, their history, navigate between configured states, call modules on the machines and more.

To navigate current space, use TAB key. To switch between the screens, use ^X to invoke menu.

On each table:

  l       - To filter items (pop-up).
            On the pop-up you can press "n" for
            next item, "p" for the previous item.

  Up/Down - To go up/down on the items.
        """.format(b=curses.A_BOLD, r=curses.A_NORMAL)
        HelpForm(text, width, height, name="Help").edit()

    def on_exit(self, *args, **kwargs):
        self.editing = False
        self.parentApp.switchFormNow()
        sys.exit(1)
