# coding: utf-8
"""
Compound controllers.
"""
import npyscreen
from sugarui.widgets.buttons import ClickButton
from sugarui.windows.floating import HelpForm


class WidgetHelp(npyscreen.widget.Widget):
    """
    Controller that also adds help button and displays floating help form
    for the particular widget. Example:

        Something: [.......] [?]

    The "[?]" button will invoke a floating form for the widget,
    explaining what it is for.
    """

    def __init__(self, screen, widget, help, *args, label_max_width=None, **kwargs):
        self.screen = screen
        kwargs["screen"] = screen
        npyscreen.widget.Widget.__init__(self, editable=False, *args, **kwargs)

        self.label = kwargs.get("label")
        if self.label:
            if label_max_width is not None:
                self.label = self.label.ljust(label_max_width)[:label_max_width]
                self.label_max_width = label_max_width
            else:
                self.label_max_width = len(self.label)
            screen.add(npyscreen.Textfield, value=self.label, relx=kwargs["relx"], rely=kwargs["rely"],
                       max_width=self.label_max_width + 1, color="CAUTION", editable=False)
            kwargs["relx"] = kwargs["relx"] + len(self.label) + 1
        del kwargs["screen"]

        height, width = self.screen.useable_space()
        self.help_button_width = 8
        self.help_text = help
        kwargs["max_width"] = width - self.help_button_width - 2 - self.relx - self.label_max_width

        if "label" in kwargs:
            del kwargs["label"]
        self.control_widget = screen.add(widget, *args, **kwargs)

        x_offset = width - self.help_button_width
        self.help_button = screen.add(ClickButton, label="Info", relx=x_offset, rely=self.rely,
                                      width=self.help_button_width, max_width=self.help_button_width)
        self.help_button.add_callback(self.on_help_button)

    def set_value(self, value):
        """
        This is a helper function that determines how to get to the inner object.

        :param value:
        :return:
        """
        classname = self.control_widget.__class__.__name__
        if classname in ["VisualTextField", "Textfield", "TitleTextfield"]:
            self.control_widget.value = str(value)
        elif classname in ["DropDown", "RadioChoice"]:
            self.control_widget.load_values(*[str(item) for item in value])
        else:
            raise Exception("Currently '{}' is not supported. "
                            "Add value directly to the 'control_widget' instance.".format(classname))

    def on_help_button(self, keycode):
        """
        On help.

        :param keycode:
        :return:
        """
        height, width = self.screen.useable_space()
        help = HelpForm(self.help_text, width // 2, 7, passive_text=True, name="Help")
        help.center_on_display()
        help.edit()
