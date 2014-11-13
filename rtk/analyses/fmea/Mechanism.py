#!/usr/bin/env python
"""
#####################
FMEA Mechanism Module
#####################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Mechanism.py is part of The RTK Project
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


class OutOfRangeError(Exception): pass


class Model(object):
    """
    The Mechanism data model contains the attributes and methods of a FMEA
    failure mechanism.  A Mode will consist of one or more Mechanisms.
    The attributes of a Mechanism are:

    :ivar mode_id: default value: 0
    :ivar mechanism_id: default value: 0
    :ivar description: default value: ''
    :ivar rpn_occurrence: default value: 0
    :ivar rpn_detection: default value: 0
    :ivar rpn: default value: 0
    :ivar rpn_occurrence_new: default value: 0
    :ivar rpn_detection_new: default value: ''
    :ivar rpn_new: default value: 0
    :ivar include_pof: default value: 0
    """

    def __init__(self):
        """
        Method to initialize an Mechanism data model instance.
        """

        # Set public dict attribute default values.
        self.dicCauses = {}
        self.dicControls = {}
        self.dicActions = {}

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.description = ''
        self.rpn_occurrence = 10
        self.rpn_detection = 10
        self.rpn = 1000
        self.rpn_occurrence_new = 10
        self.rpn_detection_new = 10
        self.rpn_new = 1000
        self.include_pof = 0

    def set_attributes(self, values):
        """
        Method to set the Mechanism data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.mode_id = int(values[0])
            self.mechanism_id = int(values[1])
            self.description = str(values[2])
            self.rpn_occurrence = int(values[3])
            self.rpn_detection = int(values[4])
            self.rpn = int(values[5])
            self.rpn_occurrence_new = int(values[6])
            self.rpn_detection_new = int(values[7])
            self.rpn_new = int(values[8])
            self.include_pof = int(values[9])
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
        Method to retrieve the current values of the Mechanism data model
        attributes.

        :return: (self.mode_id, self.mechanism_id, self.description,
                  self.rpn_occurrence, self.rpn_detection, self.rpn,
                  self.rpn_occurrence_new, self.rpn_detection_new,
                  self.rpn_new, self.include_pof)
        :rtype: tuple
        """

        return(self.mode_id, self.mechanism_id, self.description,
               self.rpn_occurrence, self.rpn_detection, self.rpn,
               self.rpn_occurrence_new, self.rpn_detection_new, self.rpn_new,
               self.include_pof)

    def calculate(self, severity, occurrence, detection):
        """
        Calculate the Risk Priority Number (RPN) for the Mechanism.

            RPN = S * O * D

        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Mechanism is associated
                             with.
        :param int occurrence: the Occurrence (O) value of the Mechanism.
        :param int detection: the Detection (D) value of the Mechanism.
        :return: _rpn
        :rtype: int
        """

        if not 0 < severity < 11:
            raise OutOfRangeError
        if not 0 < occurrence < 11:
            raise OutOfRangeError
        if not 0 < detection < 11:
            raise OutOfRangeError

        _rpn = int(severity) * int(occurrence) * int(detection)

        if not 0 < _rpn < 1001:
            raise OutOfRangeError

        return _rpn


class Mechanism(object):
    """
    The Mechanism data controller provides an interface between the Mechanism
    data model and an RTK view model.  A single Mechanism data controller can
    control one or more Mechanism data models.  Currently the Mechanism
    data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mechanism data controller instance.
        """

        pass
