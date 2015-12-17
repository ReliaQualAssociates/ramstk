#!/usr/bin/env python
"""
#######################################################################
Hardware.Component.Semiconductor.Optoelectronics Package Display Module
#######################################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.optoelectronics.Display.py is
#       part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor

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


class Display(Semiconductor):
    """
    The Optoelectronic Display data model contains the attributes and methods
    of an Optoelectronic Display component.  The attributes of an
    Optoelectronic Display are:

    :cvar subcategory: default value: 23

    :ivar type: default value: 0
    :ivar construction: default value: 0
    :ivar n_characters: default value: 0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.12.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_lambdab = [0.0055, 0.0040, 0.0025, 0.013, 0.013, 0.0064, 0.0033,
                    0.017, 0.017, 0.0086, 0.0013, 0.00023]
    _lst_piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5, 9.0,
                24.0, 450.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_lambdab_count = [0.0062, 0.016, 0.045, 0.032, 0.10, 0.046, 0.058, 0.11,
                          0.19, 0.18, 0.0031, 0.082, 0.28, 2.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 23

    def __init__(self):
        """
        Initialize a Optoelectronic Display data model instance.
        """

        super(Display, self).__init__()

        # Initialize public scalar attributes.
        self.type = 0                       # Type index.
        self.construction = 0               # Construction index.
        self.n_characters = 0               # Number of display characters.

    def set_attributes(self, values):
        """
        Sets the Optoelectronic Display data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.type = int(values[117])
            self.construction = int(values[118])
            self.n_characters = int(values[119])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Optoelectronic Display data model
        attributes.

        :return: (type, n_characters)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.type, self.construction, self.n_characters)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Optoelectronic Display data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piQ * piE'

            # Set the base hazard rate for the model.
            if self.type == 1:              # Segment display
                if self.construction == 1:  # With logic chip
                    self.base_hr = 0.00043 * self.n_characters + 0.000043
                else:
                    self.base_hr = 0.00043 * self.n_characters
            else:                           # Diode array display
                if self.construction == 1:  # With logic chip
                    self.base_hr = 0.00009 + 0.00017 * self.n_characters + 0.000043
                else:
                    self.base_hr = 0.00009 + 0.00017 * self.n_characters

            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-2790.0 * ((1.0 / (self.junction_temperature + 273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

        return Semiconductor.calculate(self)

    def _overstressed(self):
        """
        Determines whether the Optoelectronic Display is overstressed based on
        it's rated values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if self.operating_voltage > 0.70 * self.rated_voltage:
            self.overstress = True
            self.reason = self.reason + str(_reason_num) + \
                           ". Operating voltage > 70% rated voltage.\n"
            _reason_num += 1
        if self.junction_temperature > 125.0:
            self.overstress = True
            self.reason = self.reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
            _reason_num += 1

        return False
