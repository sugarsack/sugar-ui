# coding: utf-8
"""
Module runner
"""
import npyscreen
from sugarui.windows.forms import SugarForm
from sugarui.widgets.table import TableHeader, Table, TableDivider
from sugarui.widgets.tabs import TabButton, TabGroup
from sugarui.widgets.textfields import VisualTextField


class ModuleRunnerForm(SugarForm):
    """
    Module runner form.
    """
    id = __name__

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
