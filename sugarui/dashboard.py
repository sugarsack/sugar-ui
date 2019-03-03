# coding: utf-8
"""
Main dashboard
"""
import sys
import curses

from sugarui.widgets.progressbar import ProgressBar
from sugarui.widgets.table import Table, TableHeader, TableDivider
from sugarui.windows.forms import SugarForm


class FormData:
    """
    Form data
    """


class Dashboard(SugarForm):
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
        self.f_state_process = FormData()
        self.f_systems_overview = FormData()
        self.f_modules_run = FormData()
        self.f_state_run = FormData()

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
        self.f_state_process.w_progressbar = self.add(ProgressBar, name="Progress", relx=42,
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

    def on_beep(self):
        curses.beep()
        import time
        for x in range(100):
            self.f_state_process.w_progressbar.set_value(x + 1)
            time.sleep(0.01)
