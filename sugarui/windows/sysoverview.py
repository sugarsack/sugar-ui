# coding: utf-8
"""
System Overview
"""
import time
import npyscreen
from sugarui.windows.forms import SugarForm
from sugarui.widgets.table import TableHeader, Table, TableDivider
from sugarui.widgets.tabs import TabButton, TabGroup, TabController


class SystemOverviewForm(SugarForm):
    """
    Module runner form.
    """
    id = __name__

    TAB_SUMMARY = 1
    TAB_ADVANCED = 2
    TAB_PDATA = 3
    TAB_PACKAGES = 4

    def init(self):
        h, w = self.useable_space()
        self.w_clients_list_header = self.add(TableHeader, title="Selected Clients",
                                              headers=["Hostname"], max_height=2, max_width=40, rely=1)
        self.w_clients_list = self.add(Table, relx=2, rely=3, max_width=39, max_height=h - 5)
        self.w_clients_list.add_on_select_callback(self.set_hostname)

        self.w_clients_div = self.add(TableDivider, relx=41, rely=1, max_width=1)

        self.tabs = TabGroup(self, relx=42, rely=1)
        self.tabs.add_tab(self.TAB_SUMMARY, self.add(TabButton, title="Summary"))
        self.tabs.add_tab(self.TAB_ADVANCED, self.add(TabButton, title="Advanced"))
        self.tabs.add_tab(self.TAB_PDATA, self.add(TabButton, title="P-Data"))
        self.tabs.add_tab(self.TAB_PACKAGES, self.add(TabButton, title="Packages"),
                          label=time.strftime("Last updated: %D %T"))
        # Setup layouts
        self.summary_tab = self.tabs.get_tab_container(self.TAB_SUMMARY)
        self.summary_tab.w_hostname = self.summary_tab.add_widget(npyscreen.TitleText, relx=43, rely=5,
                                                                  name="Hostname:", editable=False)
        self.summary_tab.w_machine_id = self.summary_tab.add_widget(npyscreen.TitleText, relx=43,
                                                                    name="Machine ID:", editable=False)
        self.summary_tab.w_os = self.summary_tab.add_widget(npyscreen.TitleText, relx=43,
                                                            name="OS:", editable=False)
        self.summary_tab.w_uptodate = self.summary_tab.add_widget(npyscreen.TitleText, relx=43,
                                                                  name="Up to date:", editable=False)

        tab = self.tabs.get_tab_container(self.TAB_ADVANCED)
        tab.add_widget(npyscreen.BoxBasic, name="shit", relx=44, rely=5, max_height=5)

        self.tabs.align()

        self.load_sample_data()

    def set_hostname(self, value):
        self.summary_tab.w_hostname.set_value(value[0])
        self.summary_tab.w_hostname.update()
        self.refresh()

    def load_sample_data(self):
        """
        Load sample data.

        :return:
        """
        self.summary_tab.w_hostname.set_value("web1.some.lan")
        self.summary_tab.w_machine_id.set_value("234dfgdfgw3243242")
        self.summary_tab.w_os.set_value("Linux")

        self.summary_tab.w_uptodate.entry_widget.color = "CAUTIONHL"
        self.summary_tab.w_uptodate.set_value(" UPDATES ")

        data = []
        for hostname in ["zoo", "web1", "web2", "web3", "db1", "db2", "middleware", "auth", "kerb", "kerb1",
                         "ldap", "ldap1", "backup", "backup1"]:
            data.append(("{}.some.lan".format(hostname),))
        self.w_clients_list.load_data(data)
        self.w_clients_list.update()

    def refresh(self):
        """
        Recalculate widget sizes and reposition on each refresh.

        :return:
        """
        curr_height, curr_width = self.useable_space()
        super(SystemOverviewForm, self).refresh()
