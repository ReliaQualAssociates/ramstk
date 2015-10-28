#!/usr/bin/env python
"""
###################
FMEA Control Module
###################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Control.py is part of The RTK Project
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
    The Control data model contains the attributes and methods of a FMEA
    control.  A Mechanism or a Cause will consist of one or more Controls.
    The attributes of a Control are:


    :ivar mode_id: default value: 0
    :ivar mechanism_id: default value: 0
    :ivar cause_id: default value: 0
    :ivar control_id: default value: 0
    :ivar description: default value: ''
    :ivar control_type: default value: 0
    """

    def __init__(self):
        """
        Method to initialize a Control data model instance.
        """

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.control_id = 0
        self.description = ''
        self.control_type = 0

    def set_attributes(self, values):
        """
        Method to set the Control data model attributes.

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
            self.control_id = int(values[3])
            self.description = str(values[4])
            self.control_type = int(values[5])
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
        Method to retrieve the current values of the Control data model
        attributes.

        :return: (self.mode_id, self.mechanism_id, self.cause_id,
                  self.control_id, self.description, self.control_type)
        :rtype: tuple
        """

        return(self.mode_id, self.mechanism_id, self.cause_id, self.control_id,
               self.description, self.control_type)


class Control(object):
    """
    The Control data controller provides an interface between the Control data
    model and an RTK view model.  A single Control controller can control one
    or more Control data models.  Currently the Control controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Control data controller instance.
        """

        pass
