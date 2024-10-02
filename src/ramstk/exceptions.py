# -*- coding: utf-8 -*-
#
#       ramstk.exceptions.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Exceptions Module."""


class RAMSTKError(Exception):
    """Base exception class for RAMSTK errors.

    :param msg: Custom error message.
    :type msg: str
    """

    def __init__(self, msg: str = "An error occurred with RAMSTK.") -> None:
        """Initialize the basic RAMSTK exception."""
        super().__init__(msg)
        self.msg = msg

    def __str__(self) -> str:
        """Return the error message."""
        return self.msg


class DataAccessError(RAMSTKError):
    """Exception raised when attempting to access non-existent data.

    This exception is used when accessing data in the data access object (DAO) or the
    `treelib` Tree() where the data does not exist.

    :param msg: Custom error message (optional).
    :type msg: str
    """

    def __init__(self, msg: str = "Data access error.") -> None:
        """Initialize DataAccessError instance."""
        super().__init__(msg)


class OutOfRangeError(RAMSTKError):
    """Exception raised when an input value is outside legal limits.

    :param msg: Custom error message indicating the out-of-range value.
    :type msg: str
    """

    def __init__(self, msg: str = "Input value is out of the allowed range.") -> None:
        """Initialize the OutOfRangeError with an optional message."""
        super().__init__(msg)
