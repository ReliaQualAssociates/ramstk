#!/usr/bin/env python
"""
################################################
Hardware.Component.Switch Package Breaker Module
################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Breaker.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    from hardware.component.switch.Switch import Model as \
        Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.hardware.component.switch.Switch import Model as \
        Switch

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'invalid literal for int() with base 10' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        print message
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Breaker(Switch):
    """
    The Breaker Switch data model contains the attributes and methods of a
    Breaker Switch component.  The attributes of a Breaker Switch are:

    :cvar subcategory: default value: 71

    :ivar construction: default value: 0
    :ivar contact_form: default value: 0
    :ivar use: default value: 0
    :ivar piC: default value: 0.0
    :ivar piU: default value: 0.0
    :ivar piQ: default value: 0.0

    Covers specifications MIL-C-39019, MIL-C-55629, MIL-C-83383, and W-C-375.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 14.5.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piC = [1.0, 2.0, 3.0, 4.0]
    _lst_piE = [1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0, 0.5,
                25.0, 67.0, 0.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66, 0.72,
                          2.8, 0.030, 1.5, 4.0, 0.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 71

    def __init__(self):
        """
        Initialize a Breaker Switch data model instance.
        """

        super(Breaker, self).__init__()

        # Initialize public scalar attributes.
        self.construction = 0
        self.contact_form = 0
        self.use = 0
        self.piC = 0.0
        self.piU = 0.0
        self.piQ = 0.0

    def set_attributes(self, values):
        """
        Sets the Breaker Switch data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Switch.set_attributes(self, values)

        try:
            self.construction = int(values[117])
            self.contact_form = int(values[118])
            self.use = int(values[119])
            self.piC = float(values[99])
            self.piU = float(values[100])
            self.piQ = float(values[101])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Breaker Switch data model
        attributes.

        :return: (construction, contact_form, use, piC, piU, piQ)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.construction, self.contact_form, self.use,
                             self.piC, self.piU, self.piQ)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Breaker Switch data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piC * piU * piQ * piE'

            # Set the base hazard rate for the model.
            if self.construction == 1:      # Magnetic
                self.base_hr = 0.020
            elif self.construction == 2:    # Thermal
                self.base_hr = 0.038
            else:                           # Thermal-magnetic
                self.base_hr = 0.038
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the configuration factor for the model.
            self.piC = self._lst_piC[self.contact_form - 1]
            self.hazard_rate_model['piC'] = self.piC

            # Set the use factor for the model.
            if self.use == 1:
                self.piU = 1.0
            else:
                self.piU = 10.0
            self.hazard_rate_model['piU'] = self.piU

            # Set the quality factor for the model.
            if self.quality == 1:           # MIL-SPEC
                self.piQ = 1.0
            else:
                self.piQ = 8.4
            self.hazard_rate_model['piQ'] = self.piQ

        return Switch.calculate(self)
