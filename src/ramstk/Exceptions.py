# -*- coding: utf-8 -*-
#
#       ramstk.Exceptions.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Exceptions Module."""


class DataAccessError(Exception):
    """Exception raised by methods in the data access package."""

    def __init__(self, message):
        """
        Initialize DataAccessError instance.

        :param str message: the message to display to the user when this
            exception is raised.
        """
        Exception.__init__(self)

        self.message = message


class OutOfRangeError(Exception):
    """Exception raised when an input value is outside legal limits."""

    def __init__(self, message):
        """
        Initialize OutOfRangeError instance.

        :param str message: the message to display to the user when this
            exception is raised.
        """
        Exception.__init__(self)

        self.message = message


class NoParentError(Exception):
    """Exception raised when a parent element does not exist."""

    def __init__(self, message):
        """
        Initialize NoParentError instance.

        :param str message: the message to display to the user when this
            exception is raised.
        """
        Exception.__init__(self)

        self.message = message


class NoMatrixError(Exception):
    """Exception raised when no Matrices are returned."""

    def __init__(self, message):
        """
        Initialize ONoMatrixError instance.

        :param str message: the message to display to the user when this
            exception is raised.
        """
        Exception.__init__(self)

        self.message = message
