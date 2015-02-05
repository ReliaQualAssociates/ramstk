#!/usr/bin/env python
"""
##################
FMEA Action Module
##################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Action.py is part of The RTK Project
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
    The Action data model contains the attributes and methods of a FMEA
    action.  A Mechanism or a Cause will contain of one or more Actions.
    The attributes of an Action are:


    :ivar mode_id: default value: 0
    :ivar mechanism_id: default value: 0
    :ivar cause_id: default value: 0
    :ivar action_id: default value: 0
    :ivar action_recommended: default value: ''
    :ivar action_category: default value: 0
    :ivar action_owner: default value: 0
    :ivar action_due_date: default value: 0
    :ivar action_status: default value: 0
    :ivar action_taken: default value: ''
    :ivar action_approved: default value: 0
    :ivar action_approved_date: default value: 0
    :ivar action_closed: default value: 0
    :ivar action_closed_date: default value: 0
    """

    def __init__(self):
        """
        Method to initialize an Action data model instance.
        """

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.action_id = 0
        self.action_recommended = ''
        self.action_category = 0
        self.action_owner = 0
        self.action_due_date = 0
        self.action_status = 0
        self.action_taken = ''
        self.action_approved = 0
        self.action_approved_date = 0
        self.action_closed = 0
        self.action_closed_date = 0

    def set_attributes(self, values):
        """
        Method to set the Actopm data model attributes.

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
            self.action_id = int(values[3])
            self.action_recommended = str(values[4])
            self.action_category = int(values[5])
            self.action_owner = int(values[6])
            self.action_due_date = int(values[7])
            self.action_status = int(values[8])
            self.action_taken = str(values[9])
            self.action_approved = int(values[10])
            self.action_approved_date = int(values[11])
            self.action_closed = int(values[12])
            self.action_closed_date = int(values[13])
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
        Method to retrieve the current values of the Action data model
        attributes.

        :return: (mode_id, mechanism_id, cause_id, action_id,
                  action_recommended, action_category, action_owner,
                  action_due_date, action_status, action_taken,
                  action_approved, action_approved_date, action_closed,
                  action_closed_date)
        :rtype: tuple
        """

        return(self.mode_id, self.mechanism_id, self.cause_id, self.action_id,
               self.action_recommended, self.action_category,
               self.action_owner, self.action_due_date, self.action_status,
               self.action_taken, self.action_approved,
               self.action_approved_date, self.action_closed,
               self.action_closed_date)


class Action(object):
    """
    The Action data controller provides an interface between the Action data
    model and an RTK view model.  A single Action controller can control one
    or more Action data models.  Currently the Action controller is unused.
    """

    def __init__(self):
        """
        Method to initialize an Action data controller instance.
        """

        pass
