#!/usr/bin/env python
"""
##########################################################
Hardware.Component.Resistor.Fixed Package Wirewound Module
##########################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.fixed.Wirewound.py is part of the RTK
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


class Wirewound(Resistor):
    """
    The Wirewound resistor data model contains the attributes and methods of
    a Wirewound resistor.  The attributes of a Wirewound resistor are:

    :cvar _lst_piR: list of resistance factor values.
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 29

    Covers specifications MIL-R-93, MIL-R-39005.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.5
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 11.0, 5.0, 18.0, 15.0, 18.0, 28.0, 35.0, 27.0, 0.8,
                14.0, 38.0, 610.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
    _lst_lambdab_count = [0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17, 0.30,
                          0.38, 0.26, 0.0068, 0.13, 0.37, 5.4]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 29                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Wirewound resistor data model instance.
        """

        super(Wirewound, self).__init__()

    def calculate(self):
        """
        Calculates the hazard rate for the Wirewound resistor data model.

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
                self.base_hr = 0.0031 * \
                    exp(((self.temperature_active + 273.0) / 398.0)**10.0) * \
                    exp((_stress * ((self.temperature_active + 273.0) / 273.0))**1.5)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Resistance factor.
            if self.resistance <= 10000.0:
                self.piR = 1.0
            elif self.resistance > 10000.0 and self.resistance <= 1.0E5:
                self.piR = 1.7
            elif self.resistance > 1.0E5 and self.resistance <= 1.0E6:
                self.piR = 3.0
            elif self.resistance > 1.0E6:
                self.piR = 5.0
            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate(self)


class WirewoundPower(Resistor):
    """
    The Wirewound Power resistor data model contains the attributes and
    methods of a Wirewound Power resistor.  The attributes of a Wirewound
    Power resistor are:

    :cvar _lst_piR: list of resistance factor values.
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 30

    :ivar specification: default value: 0
    :ivar style: default value: 0

    Covers specifications MIL-R-26 and MIL-R-39007.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.6
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piR = [[[1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0],
                 [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6],
                 [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0],
                 [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0]],
                [[1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
                 [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
                 [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
                 [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.6, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.2, 0.0, 0.0],
                 [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                 [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.5, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.4, 1.6, 0.0],
                 [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
                 [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
                 [1.0, 1.0, 1.4, 2.4, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 2.6, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                 [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.0, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                 [1.0, 1.2, 1.5, 0.0, 0.0, 0.0],
                 [1.0, 1.2, 0.0, 0.0, 0.0, 0.0]]]
    _lst_piE = [1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0, 0.3,
                13.0, 34.0, 610.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
    _lambdab_count = [[0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15, 0.19,
                       0.39, 0.42, 0.0042, 0.21, 0.62, 9.4],
                      [0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13, 0.18,
                       0.35, 0.38, 0.0038, 0.19, 0.56, 8.6]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 30                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Wirewound Power resistor data model instance.
        """

        super(WirewoundPower, self).__init__()

        self._lst_lambdab_count = []

        self.specification = 0
        self.style = 0

    def set_attributes(self, values):
        """
        Sets the Wirewound Power resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.specification = int(values[117])
            self.style = int(values[118])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Wirewound Power resistor data model
        attributes.

        :return: (specification, style)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.specification, self.style)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Wirewound Power resistor data model.

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
                self.base_hr = \
                    0.00148 * \
                    exp(((self.temperature_active + 273.0) / 298.0)**2.0) * \
                    exp((_stress / 0.5) * ((self.temperature_active + 273.0) / 273.0))
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Resistance factor.
            if self.specification == 1:     # MIL-R-39007
                if self.resistance <= 500.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][0]
                elif self.resistance > 500.0 and self.resistance <= 1000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][1]
                elif self.resistance > 1000.0 and self.resistance <= 5000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][2]
                elif self.resistance > 5000.0 and self.resistance <= 7500.0:    # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][3]
                elif self.resistance > 7500.0 and self.resistance <= 10000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][4]
                elif self.resistance > 10000.0 and self.resistance <= 15000.0:  # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][5]
                elif self.resistance > 15000.0 and self.resistance <= 20000.0:  # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][6]
                elif self.resistance > 20000.0:                                 # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][7]
            elif self.specification == 2:   # MIL-R-26
                if self.resistance <= 100.0:                                    # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][0]
                elif self.resistance > 100.0 and self.resistance <= 1000.0:     # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][1]
                elif self.resistance > 1000.0 and self.resistance <= 10000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][2]
                elif self.resistance > 10000.0 and self.resistance <= 100000.0: # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][3]
                elif(self.resistance > 100000.0 and
                     self.resistance <= 150000.0):                              # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][4]
                elif(self.resistance > 150000.0 and
                     self.resistance <= 200000.0):                              # pragma: no cover
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][5]

            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate(self)


class WirewoundChassisMount(Resistor):
    """
    The Wirewound Chassis Mount Power resistor data model contains the
    attributes and methods of a Wirewound Chassis Mount Power  resistor.  The
    attributes of a Wirewound Chassis Mount Power resistor are:

    :cvar _lst_piR: list of resistance factor values.
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ_count: list of quality factor values for the parts count
                          method.
    :cvar _lst_piQ_stress: list of quality factor values for the parts stress
                           method.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: default value: 31

    Covers specifications MIL-R-18546 and MIL-R-39009.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.7
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piR = [[[1.0, 1.2, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.2, 1.6, 0.0],
                 [1.0, 1.0, 1.0, 1.1, 1.2, 1.6],
                 [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
                 [1.0, 1.0, 1.0, 1.0, 1.2, 1.6]],
                [[1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                 [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                 [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                 [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
                 [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
                 [1.0, 1.0, 1.0, 1.1, 1.4, 0.0]]]
    _lst_piE = [1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0, 0.5,
                13.0, 34.0, 610.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
    _lst_lambdab_count = [0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088, 0.12,
                          0.24, 0.25, 0.004, 0.13, 0.37, 5.5]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 31                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Initialize a Wirewound Chassis Mount Power resistor data model
        instance.
        """

        super(WirewoundChassisMount, self).__init__()

        self.characteristic = 0
        self.style = 0

    def set_attributes(self, values):
        """
        Sets the Wirewound Chassis Mount Power resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        Resistor.set_attributes(self, values)

        try:
            self.characteristic = int(values[117])
            self.style = int(values[118])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Wirewound Chassis Mount Power
        resistor data model attributes.

        :return: (specification, style)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.characteristic, self.style)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Wirewound Chassis Mount Power
        resistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piR * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            self.base_hr = 0.00015 * \
                           exp(2.64 * ((self.temperature_active + 273.0) / 273.0)) * \
                           exp((_stress / -.466) * ((self.temperature_active + 273.0) / 273.0))
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Resistance factor.
            if self.resistance <= 500.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][0]
            elif self.resistance > 500.0 and self.resistance <= 1000.0:     # pragma: no cover
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][1]
            elif self.resistance > 1000.0 and self.resistance <= 5000.0:    # pragma: no cover
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][2]
            elif self.resistance > 5000.0 and self.resistance <= 10000.0:   # pragma: no cover
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][3]
            elif self.resistance > 10000.0 and self.resistance <= 20000.0:  # pragma: no cover
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][4]
            elif self.resistance > 20000.0:                                 # pragma: no cover
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][5]
            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate(self)
