#!/usr/bin/env python
"""
#####################################################
Hardware.Component.Resistor.Fixed Package Film Module
#####################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.fixed.Film.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    from hardware.component.resistor.Resistor import Model as Resistor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
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


class Film(Resistor):
    """
    The Carbon Film resistor data model contains the attributes and methods of
    a Carbon Film resistor.  The attributes of a carbon film resistor are:

    :cvar _lst_piR: list of resistance factor values.
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 26

    :ivar specification: default value: 0

    Covers specifications MIL-R-10509, MIL-R-22684, MIL-R-39017, and
    MIL-R-55182.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.2
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piR = [1.0, 1.1, 1.6, 2.5]
    _lst_piE = [1.0, 2.0, 8.0, 4.0, 14.0, 4.0, 8.0, 10.0, 18.0, 19.0, 0.2,
                10.0, 28.0, 510.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [0.03, 0.1, 0.3, 1.0, 5.0, 5.0, 15.0]
    _lambdab_count = [[0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013,
                       0.018, 0.033, 0.030, 0.00025, 0.014, 0.044, 0.69],
                      [0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013,
                       0.018, 0.033, 0.030, 0.00025, 0.014, 0.044, 0.69],
                      [0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014,
                       0.021, 0.038, 0.034, 0.00028, 0.016, 0.050, 0.78],
                      [0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014,
                       0.021, 0.038, 0.034, 0.00028, 0.016, 0.050, 0.78]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 26                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Carbon Film resistor data model instance.
        """

        super(Film, self).__init__()

        self._lst_lambdab_count = []

        self.specification = 0

    def set_attributes(self, values):
        """
        Sets the carbon Film network resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        Resistor.set_attributes(self, values)

        try:
            self.specification = int(values[117])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Resistor data model attributes.

        :return: (specification)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.specification,)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Carbon Film resistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self._lst_lambdab_count = self._lambdab_count[self.specification - 1]
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piR * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                if self.specification < 3:
                    self.base_hr = \
                        3.25E-4 * \
                        exp(((self.temperature_active + 273.0) / 343.0)**3.0) * \
                        exp(_stress * ((self.temperature_active + 273.0) / 273.0))
                elif self.specification > 2:
                    self.base_hr = \
                        5.0E-5 * \
                        exp(3.5 * ((self.temperature_active + 273.0) / 343.0)) * \
                        exp(_stress * ((self.temperature_active + 273.0) / 273.0))
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Resistance factor.
            if self.resistance < 100000.0:
                self.piR = 1.0
            elif self.resistance >= 100000.0 and self.resistance < 1.0E6:
                self.piR = 1.1
            elif self.resistance >= 1.0E6 and self.resistance < 1.0E7:
                self.piR = 1.6
            elif self.resistance >= 1.0E7:
                self.piR = 2.5
            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate(self)


class FilmPower(Resistor):
    """
    The Carbon Film power resistor data model contains the attributes and
    methods of a Carbon Film power resistor.  The attributes of a carbon film
    power resistor are:

    :cvar _lst_piR: list of resistance factor values.
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 27

    Covers specifications MIL-R-11804.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.3
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piR = [1.0, 1.2, 1.3, 3.5]
    _lst_piE = [1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0, 0.5,
                14.0, 36.0, 660.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [1.0, 3.0]
    _lst_lambdab_count = [0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10, 0.19,
                          0.24, 0.32, 0.0060, 0.18, 0.47, 8.2]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 27                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Carbon Film power resistor data model instance.
        """

        super(FilmPower, self).__init__()

    def calculate(self):
        """
        Calculates the hazard rate for the Carbon Film power resistor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piR * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                self.base_hr = \
                    7.33E-3 * \
                    exp(0.202 * ((self.temperature_active + 273.0) / 298.0)**2.6) * \
                    exp((_stress / 1.45) * ((self.temperature_active + 273.0) / 273.0)**0.89)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Resistance factor.
            if self.resistance >= 10.0 and self.resistance <= 100.0:
                self.piR = 1.0
            elif self.resistance > 100.0 and self.resistance <= 1.0E4:
                self.piR = 1.2
            elif self.resistance > 1.0E4 and self.resistance <= 1.0E6:
                self.piR = 1.3
            elif self.resistance > 1.0E6:
                self.piR = 3.5
            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate(self)


class FilmNetwork(Resistor):
    """
    The Carbon Film network resistor data model contains the attributes and
    methods of a Carbon Film network resistor.  The attributes of a carbon film
    network resistor are:

    :cvar _lst_piR: list of resistance factor values.
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 28

    Covers specifications MIL-R-83401.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.4
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0, 0.5,
                14.0, 36.0, 660.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [1.0, 3.0]
    _lst_lambdab_count = [0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022, 0.043,
                          0.077, 0.15, 0.10, 0.0011, 0.055, 0.15, 1.7]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 28                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Carbon Film network resistor data model instance.
        """

        super(FilmNetwork, self).__init__()

        self.n_resistors = 1
        self.piT = 0.0
        self.piNR = 0.0

    def set_attributes(self, values):
        """
        Sets the Carbon Film network resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        Resistor.set_attributes(self, values)

        try:
            self.n_resistors = int(values[117])
            self.piT = float(values[102])
            self.piNR = int(values[103])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Carbon Film network resistor data
        model attributes.

        :return: (n_resistors, piT, piNR)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_resistors, self.piT, self.piNR)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Carbon Film network resistor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piNR * piQ * piE'

            # Base hazard rate.
            self.base_hr = 0.00006
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Temperature factor.
            if self.junction_temperature <= 0.0:
                _stress = self.operating_power / self.rated_power
                self.junction_temperature = self.temperature_active + \
                                            55.0 * _stress
            self.piT = exp(-4056.0 * ((1.0 / (self.junction_temperature + 273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Number of resistors factor.
            self.piNR = float(self.n_resistors)
            self.hazard_rate_model['piNR'] = self.piNR

        return Resistor.calculate(self)
