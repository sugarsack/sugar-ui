# coding: utf-8
"""
Module runner
"""
import yaml
import json
import textwrap
import npyscreen
from sugarui.windows.forms import SugarForm
from sugarui.widgets.table import TableHeader, Table, TableDivider
from sugarui.widgets.textfields import VisualTextField
from sugarui.widgets.dropdown import DropDown
from sugarui.widgets.compounds import WidgetHelp
from sugarui.widgets.divider import Divider


class ModuleStructure:
    """
    Object item that supports module structure elements.
    """
    def __init__(self):
        """
        :param json_data:
        """
        self._json = {}
        self._module_id = None

    @property
    def module_id(self):
        """
        Module ID.

        :return:
        """
        return self._module_id

    @module_id.setter
    def module_id(self, value):
        """
        Set module ID.

        :param value:
        :return:
        """
        self._module_id = value

    def load(self, json_data):
        """
        Load JSON data.

        :param json_data:
        :return:
        """
        if not self.module_id:
            raise Exception("Module ID was not set")

        self._json = json.loads(json_data)
        return self

    def get_functions(self):
        """
        Get list of all functions.

        :return:
        """
        return sorted(self._json.get("tasks", {}).keys())

    def get_function_signature(self, func) -> tuple:
        """
        Get signature of the function.

        :param func:
        :return: tuple of function URI and its layout
        """
        return "{}.{}".format(self._module_id, func), self._json.get("tasks", {}).get(func, {})


class ModulesLayouts:
    """
    Structure controller for keeping layouts and switching between them.
    """
    def __init__(self, y_offset=0):
        self.__layouts = {}
        self.__y_offset = y_offset

    def add_module(self, mod_uri):
        """
        Add slot for the module.

        :param mod_id:
        :return:
        """
        self.__layouts.setdefault(mod_uri, {})

    def __get_mf(self, uri):
        """
        Get module/function from the URI.

        :param uri:
        :return:
        """
        if "." not in uri:
            raise Exception("Not a function URI")

        mod, func = uri.rsplit(".", 1)
        return mod, func

    def add_function(self, uri) -> list:
        """
        Add function by URI.

        Example: [some.module].[function]

        :param uri:
        :return: List of widgets for this screen layout
        """
        mod, func = self.__get_mf(uri)
        self.add_module(mod_uri=mod)
        self.__layouts[mod].setdefault(func, [])

        return self.__layouts[mod][func]

    def add_widget(self, uri, widget):
        """
        Add widget to the function by URI.

        :param uri:
        :param widget:
        :return:
        """
        self.add_function(uri).append(widget)

    def get_next_rel_y(self, uri):
        """
        Get a "rely" for the next widget to be placed.

        :return:
        """
        rely = 0
        for widget in self.add_function(uri):
            if hasattr(widget, "control_widget"): # and widget.control_widget.__class__.__name__ == "RadioChoice":
                rely += widget.control_widget.height
            else:
                rely += 1
        return rely + self.__y_offset

    def get_widgets(self, uri):
        """
        Get widgets for the particular module/function by URI.

        :param uri:
        :return:
        """
        mod, func = self.__get_mf(uri)
        if mod not in self.__layouts:
            raise Exception("Module '{}' was not registered before".format(mod))
        elif func not in self.__layouts[mod]:
            raise Exception("Function '{}' was not registered before".format(func))

        return self.__layouts[mod][func]


class ModuleRunnerForm(SugarForm):
    """
    Module runner form.
    """
    id = __name__

    def __init__(self, *args, **kwargs):
        SugarForm.__init__(self, *args, **kwargs)

        self._module_form_params = {}
        self._current_module = ModuleStructure()
    def init(self):
        h, w = self.useable_space()
        self.w_clients_list_header = self.add(TableHeader, title="Selected Clients",
                                              headers=["Hostname"], max_height=2, max_width=40, rely=1)
        self.w_clients_list = self.add(Table, relx=2, rely=3, max_width=39, max_height=h - 5)
        self.w_clients_div = self.add(TableDivider, relx=41, rely=1, max_width=1)
        self.w_query_label = self.add(npyscreen.Textfield, value="Query:", relx=2, rely=3, max_width=8,
                                      max_height=2, color="CAUTION", editable=False)
        self.w_query = self.add(VisualTextField, value="*", relx=9, rely=3)

        self.load_sample_data()

    def load_sample_data(self):
        """
        Load sample data.

        :return:
        """
        data = []
        for hostname in ["zoo", "web1", "web2", "web3", "db1", "db2", "middleware", "auth", "kerb", "kerb1",
                         "ldap", "ldap1", "backup", "backup1"]:
            data.append(("{}.some.lan".format(hostname),))
            data.append(("{}.some.lan".format(hostname),))
            data.append(("{}.some.lan".format(hostname),))
        self.w_clients_list.load_data(data)
        self.w_clients_list.update()

    def on_load_modules(self, *args, **kwargs):
        """
        Event is happening on load modules. This is called either on query
        completion or a single host selection.

        :param args:
        :param kwargs:
        :return:
        """
        # TODO: call master API to get list of modules.

        # Sample modules
        values = [
            "system.test",
            "system.pkg",
            "network.utils",
            "network.routing",
        ]
        self.w_modules.add_values(*values)

    def refresh(self):
        """
        Recalculate widget sizes and reposition on each refresh.

        :return:
        """
        curr_height, curr_width = self.useable_space()
        self.w_query.rely = (curr_height - 2)
        self.w_query_label.rely = (curr_height - 2)
        self.w_clients_list.height = curr_height - 6
        self.w_clients_list.max_height = curr_height - 6

        super(ModuleRunnerForm, self).refresh()
