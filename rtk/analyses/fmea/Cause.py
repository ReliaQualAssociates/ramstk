#!/usr/bin/env python
"""
#################
FMEA Cause Module
#################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Cause.py is part of The RTK Project
#
# All rights reserved.


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    elif 'invalid literal' in message[0]:   # Value error
        _error_code = 50
    else:                                   # Unhandled error
        _error_code = 1000

    return _error_code


class Model(object):
    """
    The Cause data model contains the attributes and methods of a FMEA cause.
    A Mechanism will consist of one or more Causes.  The attributes of a Cause
    are:

    :ivar dicControls: Dictionary of the Controls associated with the Cause.
    Key is the Control ID, value is a pointer to the instance of the Control
    data model.
    :ivar dicActions: Dictionary of the Actions associated with the Cause.
    Key is the Action ID, value is a pointer to the instance of the Action
    data model.

    :ivar mode_id: default value: 0
    :ivar mechanism_id: default value: 0
    :ivar cause_id: default value: 0
    :ivar description: default value: ''
    """

    def __init__(self):
        """
        Method to initialize a Cause data model instance.
        """

        # Set public dict attribute default values.
        self.dicControls = {}
        self.dicActions = {}

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.description = ''

    def set_attributes(self, values):
        """
        Method to set the Cause data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.mode_id = int(values[0])
            self.mechanism_id = int(values[1])
            self.cause_id = int(values[2])
            self.description = str(values[3])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Cause data model
        attributes.

        :return: (self.mode_id, self.mechanism_id, self.cause_id,
                  self.description)
        :rtype: tuple
        """

        return(self.mode_id, self.mechanism_id, self.cause_id,
               self.description)


class Cause(object):
    """
    The Cause data controller provides an interface between the Cause data
    model and an RTK view model.  A single Cause controller can control one or
    more Cause data models.  Currently the Cause controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Cause controller instance.
        """

        pass
