# -*- coding: utf-8 -*-
#
#       ramstk.exceptions.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Exceptions Module."""


class RAMSTKError(Exception):
    """Basic exception for errors raised by RAMSTK."""

    def __init__(self, msg=None):
        """
        Initialize the basic RAMSTK exception.

        :keyword str msg: the message to display to the user when this
            exception is raised.
        """
        if msg is None:
            # Set some default useful error message
            msg = "An error occured with RAMSTK."

        super(RAMSTKError, self).__init__(msg)


class DataAccessError(RAMSTKError):
    """Exception raised by methods in the data access package."""

    def __init__(self, msg):
        """
        Initialize DataAccessError instance.

        :param str msg: the message to display to the user when this
            exception is raised.
        """
        super(DataAccessError, self).__init__(msg=msg)

        self.msg = msg


class OutOfRangeError(RAMSTKError):
    """Exception raised when an input value is outside legal limits."""

    def __init__(self, msg):
        """
        Initialize OutOfRangeError instance.

        :param str msg: the message to display to the user when this
            exception is raised.
        """
        super(OutOfRangeError, self).__init__(msg=msg)

        self.msg = msg


class NoParentError(RAMSTKError):
    """Exception raised when a parent element does not exist."""

    def __init__(self, msg):
        """
        Initialize NoParentError instance.

        :param str msg: the message to display to the user when this
            exception is raised.
        """
        super(NoParentError, self).__init__(msg=msg)

        self.msg = msg


class NoMatrixError(RAMSTKError):
    """Exception raised when no Matrices are returned."""

    def __init__(self, msg):
        """
        Initialize a NoMatrixError instance.

        :param str msg: the message to display to the user when this
            exception is raised.
        """
        super(NoMatrixError, self).__init__(msg=msg)

        self.msg = msg
