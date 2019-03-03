# coding: utf-8
"""
System overview form.
"""
import npyscreen
from sugarui.windows.forms import SugarForm


class SystemOverviewForm(SugarForm):
    """
    System overview form.
    """
    id = __name__

    def init(self):
        pager = self.add(npyscreen.Pager)
        pager.values = ["Here will be implementation of '{}' class.".format(self.__class__.__name__)]
