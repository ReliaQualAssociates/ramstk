#!/usr/bin/env python
"""
###################
FMEA Control Module
###################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Control.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Control data model contains the attributes and methods of a FMEA
    control.  A Mechanism or a Cause will consist of one or more Controls.
    The attributes of a Control are:


    :ivar int mode_id: the ID of the failure Mode this Control is associated
                       with.
    :ivar int mechanism_id: the ID of the failure Mechanism this Control is
                            associated with.
    :ivar int cause_id: the ID of the failure Cause this Control is associated
                        with.
    :ivar int control_id: the ID of this Control.
    :ivar str description: the description of this Control.
    :ivar int control_type: the type of Control
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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = Utilities.error_handler(_err.args)
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
