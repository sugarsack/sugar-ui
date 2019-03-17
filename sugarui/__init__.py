# coding: utf-8
"""
Main UI app runner.
This meant to be imported by the main Sugar app
and run as a sub-app from the nested command-line.
"""

import npyscreen
from sugarui.windows.jobmanager import JobManager
from sugarui.windows.sysoverview import SystemOverviewForm
from sugarui.windows.statemanager import StateManagerForm
from sugarui.windows.modrunner import ModuleRunnerForm
from sugarui.apiconnector import SugarAPIClient
from sugar.config import get_config


class SugarUI(npyscreen.StandardApp):
    """
    Sugar UI class.
    """
    def __init__(self):
        npyscreen.StandardApp.__init__(self)
        self._app_name = "Sugar"
        self._forms = [
            # (id, class, args, keywords, title, shortcut, classname)
        ]
        self.api = SugarAPIClient(get_config())

    def register_form(self, fid, cls, *args, **keywords):
        """
        Register form class to the menu data.

        :param fid:
        :param cls:
        :param args:
        :param keywords:
        :return:
        """
        keywords["name"] = self.ftitle(keywords["name"])
        self._forms.append((fid, cls, args, keywords, keywords.pop("title"), keywords.pop("shortcut"),
                            "on_load_{}".format(cls.__name__.lower())))

    def ftitle(self, text):
        """
        Format screen form title.

        :param text:
        :return:
        """
        return "{} - {}".format(self._app_name, text)

    def init_forms(self):
        """
        Init forms.

        :return:
        """
        for form_data in self._forms:
            fid, cls, args, kwargs = form_data[:4]
            self.addForm(fid, cls, self.api, *args, **kwargs)

    def onStart(self):
        """
        On start of the application.

        :return:
        """
        self.register_form(JobManager.id, JobManager,
                           title="JobManager", shortcut="^D", name="JobManager")
        self.register_form(SystemOverviewForm.id, SystemOverviewForm,
                           title="System Overview", shortcut="^O", name="System Overview")
        self.register_form(StateManagerForm.id, StateManagerForm,
                           title="State Manager", shortcut="^T", name="State Manager")
        self.register_form(ModuleRunnerForm.id, ModuleRunnerForm,
                           title="Module Runner", shortcut="^T", name="Module Runner")
        self.init_forms()
