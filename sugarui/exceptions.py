# coding: utf-8
"""
API network exceptions.
"""
from sugar.lib.exceptions import SugarException


class UnauthorisedError(SugarException):
    """
    User is unauthorised
    """


class UnknownResourceError(SugarException):
    """
    Resource not found.
    """


class RequestError(SugarException):
    """
    Trello request error
    """


class CLIError(SugarException):
    """
    CLI error
    """


class DataMapperError(SugarException):
    """
    Error of the data mapper
    """
