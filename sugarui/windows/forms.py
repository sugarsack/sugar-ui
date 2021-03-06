# coding: utf-8
"""
Basic forms.
This overrides npyscreen's forms, allowing concurrent widget updates.
"""
import sys
import curses
import npyscreen
from sugarui.windows.floating import HelpForm


class SugarForm(npyscreen.FormBaseNewWithMenus):
    """
    Main form with the menus.
    """
    id = "MAIN"

    # npyscreen is not introspecting instances, but classes.
    # So therefore it is not possible right now to add form switches "on_load_<something>"
    # completely dynamically in Pythonic way. Thus all switches has to be
    # defined manually here. :-( To make life easier, simply define
    # the name of the function "on_load_<lowercase-classname-of-the-form>" and
    # get its target form ID by referencing the function name in the "_form_id_map".

    def __init__(self, api, *args, **kwargs):
        npyscreen.FormBaseNewWithMenus.__init__(self, *args, **kwargs)
        self.api = api
        self.handlers.update({
            "^Q": self.on_exit,
            "h": self.on_help,
            "?": self.on_help,
        })

        self._form_id_map = {}

        # This must be called in the constructor,
        # otherwise events don't see the widgets.
        self.init()
        self.create_menu()
        self.refresh()  # npyscreen has no layout packer like e.g. urwid.Pile at all. So on resize shift happens...
                        # In this case all the auto-positioning and resizing happening manually at overridden refresh.

    def draw_form(self):
        """
        Draw form main canvas.

        :return:
        """
        super(npyscreen.FormBaseNewWithMenus, self).draw_form()
        menu_advert = " " + self.__class__.MENU_KEY + ": Menu, ^Q: Quit "
        y, x = self.display_menu_advert_at()
        self.add_line(y, x, menu_advert, self.make_attributes_list(menu_advert, curses.color_pair(5)),
                      self.columns - x - 1)

    def widget_useable_space(self, rely=0, relx=0):
        """
        Allow more width than usual.

        :param rely:
        :param relx:
        :return:
        """
        mxy, mxx = self.useable_space(rely=rely, relx=relx)
        return mxy - 1, mxx

    def init(self):
        """
        Create form.

        :return:
        """
        raise NotImplementedError("This method should be overridden")

    def create_menu(self):
        """
        Create menus

        :return:
        """
        self.w_root_menu = self.add_menu(name="Menu")  # width defaulted to 39
        menu = []
        for form_data in self.parentApp._forms:
            fid, title, shortcut, action = [form_data[0]] + list(form_data[4:])
            # TODO: Add submenus here
            if self.id != fid:
                self._form_id_map[action] = fid
                menu.append((title.ljust(30), getattr(self, action), shortcut))
        menu.append(("Help".ljust(30), self.on_help, "h"))
        menu.append(("Exit".ljust(30), self.on_exit, "^Q"))
        self.w_root_menu.addItemsFromList(menu)

    def create_submenu(self):
        """
        This includes a submenu for the current form.

        :return:
        """
        # Override me and return a submenu object

    def on_load_systemoverviewform(self, *args, **kwargs):
        """
        On load system overview.

        :return:
        """
        self.parentApp.switchForm(self._form_id_map["on_load_systemoverviewform"])

    def on_load_jobmanager(self, *args, **kwargs):
        """
        On load job manager.

        :return:
        """
        self.parentApp.switchForm(self._form_id_map["on_load_jobmanager"])

    def on_load_statemanagerform(self, *args, **kwargs):
        """
        On load state manager form.

        :return:
        """
        self.parentApp.switchForm(self._form_id_map["on_load_statemanagerform"])

    def on_load_modulerunnerform(self, *args, **kwargs):
        """
        On load module runner form.

        :return:
        """
        self.parentApp.switchForm(self._form_id_map["on_load_modulerunnerform"])

    def on_exit(self, *args, **kwargs):
        self.editing = False
        self.parentApp.switchFormNow()
        sys.exit(1)

    def on_help(self, *args, **kwargs):
        """
        Display generic help.

        :param args:
        :param kwargs:
        :return:
        """
        height, width = self.useable_space()
        text = """Sugar JobManager, v0.0.0

JobManager UI allows you to see the status of the jobs, their history, navigate between configured states, call modules on the machines and more.

To navigate current space, use:

  TAB, ^N - To select next control.
  ^P      - To select previous control.
  ^X      - For main menu invocation.

On each table:

  l       - To filter items (pop-up).
            On the pop-up you can press "n" for
            next item, "p" for the previous item.

  Up/Down - To go up/down on the items.
            """.format(b=curses.A_BOLD, r=curses.A_NORMAL)
        HelpForm(text, width, height, name="Help").edit()
