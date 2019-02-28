# coding: utf-8
"""
Progress bar widget
"""
import npyscreen


class ProgressBar(npyscreen.BoxTitle):
    """
    Progress bar.
    """
    _contained_widget = npyscreen.SliderPercent
