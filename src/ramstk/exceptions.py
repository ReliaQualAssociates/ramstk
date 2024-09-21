# -*- coding: utf-8 -*-
#
#       ramstk.exceptions.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Exceptions Module."""


class RAMSTKError(Exception):
    """Basic exception for errors raised by RAMSTK."""

    def __init__(self, msg: str = "") -> None:
        """Initialize the basic RAMSTK exception.

        :param str msg: the message to display to the user when this
            exception is raised.
        """
        self.msg = msg or "An error occurred with RAMSTK."
        super().__init__(msg)


class DataAccessError(RAMSTKError):
    """Exception raised when attempting to access non-existent data."""

    def __init__(self, msg: str = "") -> None:
        """Initialize DataAccessError instance.

        This exception is intended for use for non-existent data in the data
        access object and the treelib Tree()'s.  Use it to override the
        native exceptions.

        :param msg: the message to display to the user when this
            exception is raised.
        """
        super().__init__(msg)


class OutOfRangeError(RAMSTKError):
    """Exception raised when an input value is outside legal limits."""

    def __init__(self, msg: str) -> None:
        """Initialize OutOfRangeError instance.

        :param msg: the message to display to the user when this
            exception is raised.
        """
        super().__init__(msg=msg)
