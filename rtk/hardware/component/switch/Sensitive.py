#!/usr/bin/env python
"""
###################################################################
Hardware.Component.Switch.Sensitive Switch Package Sensitive Module
###################################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Sensitive.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    from hardware.component.switch.Switch import Model as Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.hardware.component.switch.Switch import Model as Switch

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


class Sensitive(Switch):
    """
    The Sensitive Switch data model contains the attributes and methods of a
    Sensitive Switch component.  The attributes of a Sensitive Switch are:

    :cvar subcategory: default value: 68

    :ivar load_type: default value: 0
    :ivar n_contacts: default value: 0
    :ivar cycles_per_hour: default value: 0.0
    :ivar actuation_differential: default value: 0.0
    :ivar piCYC: default value: 0.0
    :ivar piL: default value: 0.0

    Covers specification MIL-S-8805.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 14.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5,
                25.0, 67.0, 1200.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.15, 0.44, 2.7, 1.2, 4.3, 1.5, 2.7, 1.9, 3.3, 6.8,
                          0.74, 3.7, 9.9, 180.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 68

    def __init__(self):
        """
        Initialize a Sensitive Switch data model instance.
        """

        super(Sensitive, self).__init__()

        # Initialize public scalar attributes.
        self.load_type = 0
        self.n_contacts = 0                 # Number of active contacts
        self.cycles_per_hour = 0.0
        self.actuation_differential = 0.0
        self.piCYC = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
        Sets the Sensitive Switch data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Switch.set_attributes(self, values)

        try:
            self.load_type = int(values[117])
            self.n_contacts = int(values[118])
            self.cycles_per_hour = float(values[99])
            self.actuation_differential = float(values[100])
            self.piCYC = float(values[101])
            self.piL = float(values[102])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Sensitive Switch data model
        attributes.

        :return: (load_type, cycles_per_hour, actuation_differential, piCYC,
                  piL)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.load_type, self.n_contacts,
                             self.cycles_per_hour, self.actuation_differential,
                             self.piCYC, self.piL)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Sensitive Switch data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piCYC * piL * piE'

            # Set the base hazard rate for the model.
            if self.quality == 1:       # MIL-SPEC
                if self.actuation_differential > 0.002:
                    self.base_hr = 0.1 + 0.00045 * self.n_contacts
                else:
                    self.base_hr = 0.1 + 0.0009 * self.n_contacts
            else:
                if self.actuation_differential > 0.002:
                    self.base_hr = 0.1 + 0.23 * self.n_contacts
                else:
                    self.base_hr = 0.1 + 0.63 * self.n_contacts
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the cycling factor for the model.
            if self.cycles_per_hour <= 1.0:
                self.piCYC = 1.0
            else:
                self.piCYC = float(self.cycles_per_hour)
            self.hazard_rate_model['piCYC'] = self.piCYC

            # Set the load stress factor for the model.
            _stress = self.operating_current / self.rated_current
            if self.load_type == 1:         # Resistive
                self.piL = exp((_stress / 0.8)**2.0)
            elif self.load_type == 2:       # Inductive
                self.piL = exp((_stress / 0.4)**2.0)
            elif self.load_type == 3:       # Lamp
                self.piL = exp((_stress / 0.2)**2.0)
            self.hazard_rate_model['piL'] = self.piL

        return Switch.calculate(self)
