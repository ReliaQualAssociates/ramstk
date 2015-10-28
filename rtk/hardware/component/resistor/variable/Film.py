#!/usr/bin/env python
"""
########################################################
Hardware.Component.Resistor.Variable Package Film Module
########################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.variable.Film.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import configuration as _conf
    from hardware.component.resistor.Resistor import Model as Resistor
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    from rtk.hardware.component.resistor.Resistor import Model as Resistor

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


class VarFilm(Resistor):
    """
    The VarFilm Variable resistor data model contains the attributes and
    methods of a VarFilm Variable resistor.  The attributes of a
    VarFilm Variable resistor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 39

    :ivar n_taps: default value: 3
    :ivar style: default value: 0
    :ivar piTAPS: default value: 0.0
    :ivar piV: default value: 0.0

    Covers specifications MIL-R-23285 and MIL-R-39023.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.15
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 14.0, 7.0, 24.0, 6.0, 12.0, 20.0, 30.0, 39.0, 0.5,
                22.0, 57.0, 1000.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [2.0, 4.0]
    _lst_lambdab_count = [0.048, 0.16, 0.76, 0.36, 1.3, 0.36, 0.72, 1.4, 2.2,
                          2.3, 0.024, 1.2, 3.4, 52.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 39                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Variable Film resistor data model instance.
        """

        super(VarFilm, self).__init__()

        self.n_taps = 3
        self.style = 0
        self.piTAPS = 0.0
        self.piV = 0.0

    def set_attributes(self, values):
        """
        Sets the Variable Film resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.n_taps = int(values[117])
            self.style = int(values[118])
            self.piTAPS = float(values[104])
            self.piV = float(values[105])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Variable Film resistor data model
        attributes.

        :return: (n_taps, style, piTAPS, piV)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_taps, self.style, self.piTAPS, self.piV)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Variable Film resistor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp, sqrt

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piTAPS * piR * piV * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                if self.style == 1:
                    self.base_hr = 0.018 * \
                                   exp(((self.temperature_active + 273.0) / 343.0)**7.4) * \
                                   exp((_stress / 2.55) * ((self.temperature_active + 273.0) / 273.0)**3.6)
                elif self.style == 2:
                    self.base_hr = 0.0257 * \
                                   exp(((self.temperature_active + 273.0) / 398.0)**7.9) * \
                                   exp((_stress / 2.45) * ((self.temperature_active + 273.0) / 273.0)**4.3)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Potentiometer taps factor.
            self.piTAPS = (self.n_taps**1.5 / 25.0) + 0.792
            self.hazard_rate_model['piTAPS'] = self.piTAPS

            # Resistance factor.
            if self.resistance <= 10000.0:
                self.piR = 1.0
            elif self.resistance > 100000.0 and self.resistance <= 50000.0:     # pragma: no cover
                self.piR = 1.1
            elif self.resistance > 50000.0 and self.resistance <= 200000.0:
                self.piR = 1.2
            elif self.resistance > 200000.0 and self.resistance <= 1000000.0:
                self.piR = 1.4
            elif self.resistance > 1000000.0:
                self.piR = 1.8
            self.hazard_rate_model['piR'] = self.piR

            # Voltage factor.
            _v_applied = sqrt(self.resistance * self.operating_power)
            if _v_applied / self.rated_voltage <= 0.8:      # pragma: no cover
                self.piV = 1.00
            elif(_v_applied / self.rated_voltage > 0.8 and
                 _v_applied / self.rated_voltage <= 0.9):
                self.piV = 1.05
            elif(_v_applied / self.rated_voltage > 0.9 and
                 _v_applied / self.rated_voltage <= 1.0):   # pragma: no cover
                self.piV = 1.20
            self.hazard_rate_model['piV'] = self.piV

        return Resistor.calculate(self)
