# -*- coding: utf-8 -*-
#
#       ramstk.utilities.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Utility functions for interacting with the RAMSTK application."""

# Standard Library Imports
import functools
import gettext
import os
import os.path
import site
import warnings
from datetime import datetime
from typing import Callable, List, Union

# Third Party Imports
# noinspection PyPackageRequirements
from dateutil.parser import parse
from pubsub import pub

_ = gettext.gettext


def date_to_ordinal(date: str) -> int:
    """Convert date strings to ordinal dates for use in the database.

    :param date: the date string to convert.
    :return: ordinal representation of the passed date.
    :rtype: int
    """
    try:
        return parse(date).toordinal()
    except (ValueError, TypeError):
        return parse("01/01/1970").toordinal()


def deprecated(func: Callable) -> Callable:
    """Decorate other functions as deprecated."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            f"Call to deprecated function {func.__name__}.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def dir_exists(directory: str) -> bool:
    """Check if a directory exists.

    :param directory: a string representing the directory path to check
                          for.
    :return: False if the directory does not exist, True otherwise.
    :rtype: bool
    """
    return os.path.isdir(directory)


def do_subscribe_to_messages(messages) -> None:
    """Subscribe to PyPubSub messages."""
    for _message, _handler in messages.items():
        pub.subscribe(_handler, _message)


def file_exists(_file: str) -> bool:
    """Check if a file exists.

    :param _file: a string representing the filepath to check for.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(_file)


def none_to_default(
    field: None, default: Union[bool, float, int, str]
) -> Union[bool, float, int, str]:
    """Convert None values into default values.

    :param field: the original value that may be None.
    :param default: the new, default, value.
    :return: field; the new value if field is None, the old value
        otherwise.
    :rtype: any
    """
    return default if field is None else field


def none_to_string(string: Union[None, str]) -> str:
    """Convert None types to an empty string.

    :param string: the string to convert.
    :return: string; the converted string.
    :rtype: str
    """
    _return = string
    if _return is None or _return == "None":
        _return = ""

    return _return


def ordinal_to_date(ordinal: int) -> str:
    """Convert ordinal dates to date strings in ISO-8601 format.

    Defaults to the current date if a bad value is passed as the argument.

    :param ordinal: the ordinal date to convert.
    :return: the ISO-8601 date representation of the passed ordinal.
    :rtype: str
    """
    try:
        return str(datetime.fromordinal(ordinal).strftime("%Y-%m-%d"))
    except TypeError:
        ordinal = datetime.now().toordinal()
        return str(datetime.fromordinal(int(ordinal)).strftime("%Y-%m-%d"))


def split_string(string: str) -> List[str]:
    """Split a colon-delimited string into its constituent parts.

    :param string: the colon delimited string that needs to be split into
        a list.
    :return: _strlist
    :rtype: list of strings
    """
    return string.rsplit(":")


def boolean_to_integer(boolean: bool) -> int:
    """Convert boolean representations of TRUE/FALSE to an integer value.

    :param bool boolean: the boolean to convert.
    :return: _result
    :rtype: int
    """
    return 1 if boolean else 0


def integer_to_boolean(integer: int) -> bool:
    """Convert an integer to boolean value.

    Any value greater than zero is returned as True, all others are returned as
    False.

    :param integer: the integer to convert.
    :return: _result
    :rtype: bool
    :raise: TypeError if passed a string.
    """
    return integer > 0


def string_to_boolean(string: Union[bool, str]) -> bool:
    """Convert string representations of TRUE/FALSE to a boolean value.

    :param string: the string to convert.
    :return: _result
    :rtype: bool
    """
    try:
        return string.lower() in {"true", "yes", "t", "y"}  # type: ignore
    except AttributeError:
        return string  # type: ignore


def get_install_prefix() -> str:
    """Return the prefix that this code was installed into."""
    return site.getsitepackages()[0].split("/lib")[0]
