#!/usr/bin/env python
"""
#########################
PoF Operating Load Module
#########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Load.py is part of The RTK Project
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
    The Load data model contains the attributes and methods of a Physics of
    Failure operating load.  A PoF will consist of one or more Loads per
    failure mechanism.  The attributes of a Load are:

    :ivar dicStresses: Dictionary of the operating stresses associated with the
                       operating load.  Key is the Stress ID; value is a
                       pointer to the instance of the operating Stress data
                       model.

    :ivar mechanism_id: default value: None
    :ivar load_id: default value: 0
    :ivar description: default value: ''
    :ivar damage_model: default value: 0
    :ivar priority: default value: 0
    """

    def __init__(self, mechanism_id=None):
        """
        Method to initialize a Load data model instance.
        """

        # Set public dict attribute default values.
        self.dicStresses = {}

        # Set public scalar attribute default values.
        self.mechanism_id = mechanism_id
        self.load_id = None
        self.description = ''
        self.damage_model = 0
        self.priority = 0

    def set_attributes(self, values):
        """
        Method to set the Load data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.mechanism_id = int(values[0])
            self.load_id = int(values[1])
            self.description = str(values[2])
            self.damage_model = int(values[3])
            self.priority = int(values[4])
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

        :return: (mechanism_id, load_id, description, damage_model, priority)
        :rtype: tuple
        """

        return(self.mechanism_id, self.load_id, self.description,
               self.damage_model, self.priority)


class Load(object):
    """
    The Load data controller provides an interface between the Load data model
    and an RTK view model.  A single Load data controller can control one or
    more Load data models.  Currently the Load data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Load data controller instance.
        """

        pass
