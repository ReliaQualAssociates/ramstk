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
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Stress data model contains the attributes and methods of a Physics of
    Failure operating stress.  A PoF will consist of one or more Stress per
    operating load.  The attributes of a Stress are:

    :ivar dict dicMethods: Dictionary of the test methods associated with the
                           operating stress.  Key is the Method ID; value is a
                           pointer to the instance of the test method data
                           model.
    :ivar int load_id: the PoF Load ID the Stress is associated with.
    :ivar int stress_id: the ID of the PoF Stress.
    :ivar str description: the description of the PoF Stress.
    :ivar int measurable_parameter: the index of the parameter that can be
                                    measured and correlated with the PoF
                                    Stress.
    :ivar int load_history: the index of the load history method for the
                            PoF Stress.
    :ivar str remarks: any remarks associated with the PoF Stress.
    """

    def __init__(self, load_id=None):
        """
        Method to initialize a Stress data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicMethods = {}

        # Define public list attributes.

        # Define public scalar attributes.
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
    The Stress data controller provides an interface between the Stress data
    model and an RTK view model.  A single Stress data controller can control
    one or more Stress data models.  Currently the Stress data controller is
    unused.
    """

    def __init__(self):
        """
        Method to initialize a Stress data controller instance.
        """

        pass
