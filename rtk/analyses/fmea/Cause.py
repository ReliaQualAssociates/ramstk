#!/usr/bin/env python
"""
#################
FMEA Cause Module
#################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Cause.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities as _util
except ImportError:
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Cause data model contains the attributes and methods of a FMEA cause.
    A Mechanism will consist of one or more Causes.  The attributes of a Cause
    are:

    :ivar dicControls: Dictionary of the Controls associated with the Cause.
                       Key is the Control ID, value is a pointer to the
                       instance of the Controldata model.
    :ivar dicActions: Dictionary of the Actions associated with the Cause.
                      Key is the Action ID, value is a pointer to the instance
                      of the Action data model.

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
        self.rpn_occurrence = 9
        self.rpn_detection = 9
        self.rpn = 1000
        self.rpn_occurrence_new = 9
        self.rpn_detection_new = 9
        self.rpn_new = 1000

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
            self.rpn_occurrence = int(values[4])
            self.rpn_detection = int(values[5])
            self.rpn = int(values[6])
            self.rpn_occurrence_new = int(values[7])
            self.rpn_detection_new = int(values[8])
            self.rpn_new = int(values[9])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Cause data model
        attributes.

        :return: (mode_id, mechanism_id, cause_id, description, rpn_occurrence,
                  rpn_detection, rpn, rpn_occurrence_new, rpn_detection_new,
                  rpn_new)
        :rtype: tuple
        """

        return(self.mode_id, self.mechanism_id, self.cause_id,
               self.description, self.rpn_occurrence, self.rpn_detection,
               self.rpn, self.rpn_occurrence_new, self.rpn_detection_new,
               self.rpn_new)


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
