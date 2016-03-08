#!/usr/bin/env python
"""
##################################
Semiconductor Package Diode Module
##################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.Diode.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class LowFrequency(Semiconductor):
    """
    The Low Frequency Diode data model contains the attributes and methods of a
    Low Frequency Diode component.  The attributes of a Low Frequency Diode
    are:

    :cvar int subcategory: default value: 12

    :ivar int application: default value: 0
    :ivar int construction: default value: 0
    :ivar float piS: default value: 0.0
    :ivar float piC: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_lambdab = [0.0038, 0.0010, 0.069, 0.003, 0.005, 0.0013, 0.0034, 0.002]
    _lst_piC = [1.0, 2.0]
    _lst_piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                14.0, 32.0, 320.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lambda_count = [[0.00360, 0.0280, 0.049, 0.043, 0.100, 0.092, 0.210,
                      0.200, 0.44, 0.170, 0.00180, 0.076, 0.23, 1.50],
                     [0.00094, 0.0075, 0.013, 0.011, 0.027, 0.024, 0.054,
                      0.054, 0.12, 0.045, 0.00047, 0.020, 0.06, 0.40],
                     [0.06500, 0.5200, 0.890, 0.780, 1.900, 1.700, 3.700,
                      3.700, 8.00, 3.100, 0.03200, 1.400, 4.10, 28.0],
                     [0.00280, 0.0220, 0.039, 0.034, 0.062, 0.073, 0.160,
                      0.160, 0.35, 0.130, 0.00140, 0.060, 0.18, 1.20],
                     [0.00290, 0.0230, 0.040, 0.035, 0.084, 0.075, 0.170,
                      0.170, 0.36, 0.140, 0.00150, 0.062, 0.18, 1.20],
                     [0.00330, 0.0240, 0.039, 0.035, 0.082, 0.066, 0.150,
                      0.130, 0.27, 0.120, 0.00160, 0.060, 0.16, 1.30],
                     [0.00560, 0.0400, 0.066, 0.060, 0.140, 0.110, 0.250,
                      0.220, 0.460, 0.21, 0.00280, 0.100, 0.28, 2.10]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 12

    def __init__(self):
        """
        Method to initialize a Low Frequency Diode data model instance.
        """

        super(LowFrequency, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_lambdab_count = []

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.application = 0                # Application index.
        self.construction = 0               # Construction index.
        self.piS = 0.0                      # Electrical stress pi factor.
        self.piC = 0.0                      # Contact construction pi factor.

    def set_attributes(self, values):
        """
        Method to set the Low Frequency Diode data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.application = int(values[117])
            self.construction = int(values[118])
            self.piS = float(values[101])
            self.piC = float(values[102])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Low Frequency Diode data
        model attributes.

        :return: (application, construction, piS, piC)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.application, self.construction, self.piS,
                             self.piC)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Low Frequency Diode data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            # Set the base hazard rate for the model.
            self._lst_lambdab_count = self._lambda_count[self.application - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piS * piC * piQ * piE'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab[self.application - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            if self.application < 7:
                self.piT = exp(-3091.0 * ((1.0 / (self.junction_temperature +
                                                  273.0)) - (1.0 / 298.0)))
            else:
                self.piT = exp(-1925.0 * ((1.0 / (self.junction_temperature +
                                                  273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the voltage stress factor for the model.
            if self.application > 6:
                self.piS = 1.0
            else:
                _stress = self.operating_voltage / self.rated_voltage
                if _stress <= 0.3:
                    self.piS = 0.054
                else:
                    self.piS = _stress**2.43
            self.hazard_rate_model['piS'] = self.piS

            # Set the contact construction factor for the model.
            self.piC = self._lst_piC[self.construction - 1]
            self.hazard_rate_model['piC'] = self.piC

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the Low Frequency Diode is overstressed
        based on it's rated values and operating environment.

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

        if _harsh:
            if self.operating_power > 0.7 * self.rated_power:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                              ". Operating power > 70% rated power.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                              ". Junction temperature > 125.0C.\n"
        else:
            if self.operating_power > 0.9 * self.rated_power:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                              ". Operating power > 90% rated power.\n"

        return False


class HighFrequency(Semiconductor):
    """
    The High Frequency Diode data model contains the attributes and methods of
    a High Frequency Diode component.  The attributes of a High Frequency Diode
    are:

    :cvar int subcategory: default value: 13

    :ivar int application: default value: 0
    :ivar int type: default value: 0
    :ivar float piA: default value: 0.0
    :ivar float piR: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_lambdab = [0.22, 0.18, 0.0023, 0.0081, 0.027, 0.0025, 0.0025]
    _lst_piA = [0.5, 2.5, 1.0]
    _lst_piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
                24.0, 250.0]
    _piQ_count = [[0.5, 1.0, 5.0, 25, 50], [0.5, 1.0, 1.8, 2.5]]
    _lst_piQ_stress = [0.5, 1.0, 1.8, 2.5, 1.0]
    _lambda_count = [[0.86, 2.80, 8.9, 5.6, 20.0, 11.0, 14.0, 36.0, 62.0, 44.0,
                      0.43, 16.0, 67.0, 350.0],
                     [0.31, 0.76, 2.1, 1.5, 4.60, 2.00, 2.50, 4.50, 7.60, 7.90,
                      0.16, 3.70, 12.0, 94.00],
                     [0.004, 0.0096, 0.0026, 0.0019, 0.058, 0.025, 0.032,
                      0.057, 0.097, 0.10, 0.002, 0.048, 0.15, 1.2],
                     [0.028, 0.068, 0.19, 0.14, 0.41, 0.18, 0.22, 0.40, 0.69,
                      0.71, 0.014, 0.34, 1.1, 8.5],
                     [0.047, 0.11, 0.31, 0.23, 0.68, 0.3, 0.37, 0.67, 1.1, 1.2,
                      0.023, 0.56, 1.8, 14.0],
                     [0.0043, 0.010, 0.029, 0.021, 0.063, 0.028, 0.034, 0.062,
                      0.11, 0.11, 0.0022, 0.052, 0.17, 1.3]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 13

    def __init__(self):
        """
        Method to initialize a High Frequency Diode data model instance.
        """

        super(HighFrequency, self).__init__()

        # Initialize private list attributes.
        self._lst_lambdab_count = []
        self._lst_piQ_count = []

        # Initialize public scalar attributes.
        self.application = 0                # Application index.
        self.type = 0                       # Type index.
        self.piA = 0.0                      # Electrical stress pi factor.
        self.piR = 0.0                      # Contact construction pi factor.

    def set_attributes(self, values):
        """
        Method to set the High Frequency Diode data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.application = int(values[117])
            self.type = int(values[118])
            self.piA = float(values[101])
            self.piR = float(values[102])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the High Frequency Diode data
        model attributes.

        :return: (application, type, piA, piR)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.application, self.type, self.piA, self.piR)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the High Frequency Diode data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write calculate_part; current McCabe Complexity metric = 12.
        from math import exp, log

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            # Set the base hazard rate for the model.
            self._lst_lambdab_count = self._lambda_count[self.application - 1]

            if self.type == 5:
                self._lst_piQ_count = self._piQ_count[1]
            else:
                self._lst_piQ_count = self._piQ_count[0]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piA * piR * piQ * piE'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab[self.application - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            if self.type == 1:
                self.piT = exp(-2100.0 * ((1.0 / (self.junction_temperature +
                                                  273.0)) - (1.0 / 298.0)))
            else:
                self.piT = exp(-5260.0 * ((1.0 / (self.junction_temperature +
                                                  273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the application factor for the model.
            if self.application == 6:       # pragma: no cover
                self.piA = 0.5
            elif self.application == 7:
                self.piA = 2.5
            else:                           # pragma: no cover
                self.piA = 1.0
            self.hazard_rate_model['piA'] = self.piA

            # Set the power rating factor for the model.
            if self.application == 4:
                self.piR = 0.326 * log(self.rated_power) - 0.25
            else:
                self.piR = 1.0
            self.hazard_rate_model['piR'] = self.piR

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the High Frequency Diode is overstressed
        based on it's rated values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
        _reason = ''
        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if _harsh:
            if self.operating_power > 0.7 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              ". Operating power > 70% rated power.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              ". Junction temperature > 125.0C.\n"
        else:
            if self.operating_power > 0.9 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              ". Operating power > 90% rated power.\n"

        self.reason = _reason

        return False
