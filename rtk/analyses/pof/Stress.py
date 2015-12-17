#!/usr/bin/env python
"""
###########################
PoF Operating Stress Module
###########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Stress.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Stress data model contains the attributes and methods of a Physics of
    Failure operating stress.  A PoF will consist of one or more Stress per
    operating load.  The attributes of a Stress are:

    :ivar dicMethods: Dictionary of the test methods associated with the
                      operating stress.  Key is the Method ID; value is a
                      pointer to the instance of the test method data model.

    :ivar load_id: default value: None
    :ivar stress_id: default value: None
    :ivar description: default value: ''
    :ivar measurable_parameter: default value: 0
    :ivar load_history: default value: 0
    :ivar remarks: default value: ''
    """

    def __init__(self, load_id=None):
        """
        Method to initialize a Stress data model instance.
        """

        # Set public dict attribute default values.
        self.dicMethods = {}

        # Set public scalar attribute default values.
        self.load_id = load_id
        self.stress_id = None
        self.description = ''
        self.measurable_parameter = 0
        self.load_history = 0
        self.remarks = ''

    def set_attributes(self, values):
        """
        Method to set the Stress data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.load_id = int(values[0])
            self.stress_id = int(values[1])
            self.description = str(values[2])
            self.measurable_parameter = int(values[3])
            self.load_history = int(values[4])
            self.remarks = str(values[5])
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
        Method to retrieve the current values of the Mode data model
        attributes.

        :return: (load_id, stress_id, description, measurable_parameter,
                  load_history, remarks)
        :rtype: tuple
        """

        return(self.load_id, self.stress_id, self.description,
               self.measurable_parameter, self.load_history, self.remarks)


class Stress(object):
    """
    The Stress data controller provides an interface between the Stress data model
    and an RTK view model.  A single Stress data controller can control one or
    more Stress data models.  Currently the Stress data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Stress data controller instance.
        """

        pass
