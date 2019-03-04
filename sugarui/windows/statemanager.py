# coding: utf-8
"""
State manager interface.
"""
import npyscreen
from sugarui.windows.forms import SugarForm


class StateManagerForm(SugarForm):
    """
    State manager form.
    """
    id = __name__

    def init(self):
        pager = self.add(npyscreen.Pager)
        pager.values = ["Here will be implementation of '{}' class.".format(self.__class__.__name__)]
