# coding: utf-8
"""
Main UI app runner.
This meant to be imported by the main Sugar app
and run as a sub-app from the nested command-line.
"""

import npyscreen
from sugarui.dashboard import Dashboard


class SugarUI(npyscreen.StandardApp):
    """
    Sugar UI class.
    """
    def onStart(self):
        self.addForm(Dashboard.id, Dashboard, name="Sugar Dashboard, v0.0.0")
