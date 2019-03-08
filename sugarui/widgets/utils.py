# coding: utf-8
"""
Common utilities for the Widgets.
"""

TYPE_BTN_CONFIRM = "\u25a3"
TYPE_BTN_REJECT = "\u25c9"
TYPE_BTN_SELECT = "\u25c8"


def make_button_label(label: str, type=TYPE_BTN_CONFIRM, selected: bool = True) -> str:
    """
    Turns any label into a button label standard.

    :param label: Text
    :return: button label string
    """
    if selected:
        ls = "\u25B8"
        rs = "\u25C2"
    else:
        ls = "\u25B9"
        rs = "\u25C3"

    return "{ls} {label} {f}  {rs}".format(f=type, label=(label or "* ERROR *").strip(), ls=ls, rs=rs)
