#!/usr/bin/env python
"""
############################################
Transistor Package Bipolar Transistor Module
############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.transistor.Bipolar.py is part of
#       the RTK Project
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


class LFBipolar(Semiconductor):
    """
    The Low Frequency Bipolar Transistor data model contains the attributes and
    methods of a Low Frequency Bipolar Transistor component.  The attributes of
    a Low Frequency Bipolar Transistor are:

    :cvar int subcategory: default value: 14

    :ivar int application: the MIL-HDBK-217FN2 application index.
    :ivar float piA: the MIL-HDBK-217FN2 application factor.
    :ivar float piR: the MIL-HDBK-217FN2 power rating factor.
    :ivar float piS: the MIL-HDBK-217FN2 voltage stress factor.

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 6.3.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piA = [1.5, 0.7]
    _lst_piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                14.0, 32.0, 320.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lambdab_count = [[0.00015, 0.0011, 0.0017, 0.0017, 0.0037, 0.0030, 0.0067,
                       0.0060, 0.013, 0.0056, 0.000073, 0.0027, 0.0074, 0.056],
                      [0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26, 0.23,
                       0.50, 0.22, 0.0029, 0.11, 0.29, 1.1]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 14

    def __init__(self):
        """
        Method to initialize a Low Frequency Bipolar Transistor data model
        instance.
        """

        super(LFBipolar, self).__init__()

        # Initialize private list attributes.
        self._lst_lambdab_count = []

        # Initialize public scalar attributes.
        self.base_hr = 0.00074              # Base hazard rate.
        self.application = 0                # Application index.
        self.piA = 0.0                      # Application pi factor
        self.piR = 0.0                      # Power rating pi factor.
        self.piS = 0.0                      # Voltage stress pi factor.

    def set_attributes(self, values):
        """
        Method to set the Low Frequency Bipolar Transistor data model
        attributes.

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
            self.piA = float(values[101])
            self.piR = float(values[102])
            self.piS = float(values[103])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieves the current values of the Low Frequency Bipolar
        Transistor data model attributes.

        :return: (application, piA, piR, piS)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.application, self.piA, self.piR, self.piS)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Low Frequency Bipolar
        Transistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            if self.rated_power <= 0.1:
                self._lst_lambdab_count = self._lambdab_count[0]
            else:
                self._lst_lambdab_count = self._lambdab_count[1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piA * piR * piS * piQ * piE'

            # Set the base hazard rate for the model.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-2114.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the application factor for the model.
            self.piA = self._lst_piA[self.application - 1]
            self.hazard_rate_model['piA'] = self.piA

            # Set the power rating factor for the model.
            if self.rated_power <= 0.1:
                self.piR = 0.43
            else:
                self.piR = self.rated_power**0.37
            self.hazard_rate_model['piR'] = self.piR

            # Set the voltage stress factor for the model.
            _stress = self.operating_voltage / self.rated_voltage
            self.piS = 0.045 * exp(3.1 * _stress)
            self.hazard_rate_model['piS'] = self.piS

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the Low Frequency Bipolar Transistor is
        overstressed based on it's rated values and operating environment.

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
            if self.operating_power > 0.70 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 70% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.75 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 70% rated voltage.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
                _reason_num += 1
        else:
            if self.operating_power > 0.90 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 90% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 90% rated voltage.\n"
                _reason_num += 1

        self.reason = _reason

        return False


class HFLNBipolar(Semiconductor):
    """
    The High Frequency Low Noise Bipolar Transistor data model contains the
    attributes and methods of a High Frequency Low Noise Bipolar Transistor
    component.  The attributes of a High Frequency Low Noise Bipolar Transistor
    are:

    :cvar subcategory: default value: 17

    :ivar float piR: the MIL-HDBK-217FN2
    :ivar float piS: the MIL-HDBK-217FN2

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 6.6.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
                24.0, 250.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.5, 1.0, 2.0, 5.0]
    _lst_lambdab_count = [0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3, 2.3,
                          2.4, 0.047, 1.1, 3.6, 28.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 17

    def __init__(self):
        """
        Method to initialize a High Frequency Low Noise Bipolar Transistor data
        model instance.
        """

        super(HFLNBipolar, self).__init__()

        # Initialize public scalar attributes.
        self.base_hr = 0.18                 # Base hazard rate.
        self.piR = 0.0                      # Power rating pi factor.
        self.piS = 0.0                      # Voltage stress pi factor.

    def set_attributes(self, values):
        """
        Method to set the High Frequency Low Noise Bipolar Transistor data
        model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.piR = float(values[101])
            self.piS = float(values[102])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the High Frequency Low Noise
        Bipolar Transistor data model attributes.

        :return: (piR, piS)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.piR, self.piS)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the High Frequency Low Noise
        Bipolar Transistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piR * piS * piQ * piE'

            # Set the base hazard rate for the model.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-2114.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the power rating factor for the model.
            if self.rated_power <= 0.1:
                self.piR = 0.43
            else:
                self.piR = self.rated_power**0.37
            self.hazard_rate_model['piR'] = self.piR

            # Set the voltage stress factor for the model.
            _stress = self.operating_voltage / self.rated_voltage
            self.piS = 0.045 * exp(3.1 * _stress)
            self.hazard_rate_model['piS'] = self.piS

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the High Frequency Low Noise Bipolar
        Transistor is overstressed based on it's rated values and operating
        environment.

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
            if self.operating_power > 0.70 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 70% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.75 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 70% rated voltage.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
                _reason_num += 1
        else:
            if self.operating_power > 0.90 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 90% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 90% rated voltage.\n"
                _reason_num += 1

        self.reason = _reason

        return False


class HFHPBipolar(Semiconductor):
    """
    The High Frequency High Power Bipolar Transistor data model contains the
    attributes and methods of a High Frequency High Power Bipolar Transistor
    component.  The attributes of a High Frequency High Power Bipolar
    Transistor are:

    :cvar subcategory: default value: 18

    :ivar construction: default value: 0
    :ivar application: default value: 0
    :ivar matching: default value: 0
    :ivar frequency: default value: 0.0
    :ivar piA: default value: 0.0
    :ivar piM: default value: 0.0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.7.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piM = [1.0, 2.0, 4.0]
    _lst_piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
                24.0, 250.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.5, 1.0, 2.0, 5.0]
    _lst_lambdab_count = [0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37, 0.52,
                          0.88, 0.037, 0.33, 0.66, 1.8, 18.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 18

    def __init__(self):
        """
        Method to initialize a High Frequency High Power Bipolar Transistor
        data model instance.
        """

        super(HFHPBipolar, self).__init__()

        # Initialize public scalar attributes.
        self.construction = 0               # Construction index.
        self.application = 0                # Application index.
        self.matching = 0                   # Matching index.
        self.frequency = 0.0                # Operating frequency.
        self.piA = 0.0                      # Application pi factor.
        self.piM = 0.0                      # Matching network pi factor.

    def set_attributes(self, values):
        """
        Method to set the High Frequency High Power Bipolar Transistor data
        model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.construction = int(values[117])
            self.application = int(values[118])
            self.matching = int(values[119])
            self.frequency = float(values[101])
            self.piA = float(values[102])
            self.piM = float(values[103])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the High Frequency High Power
        Bipolar Transistor data model attributes.

        :return: (construction, application, matching, frequency, piA, piM)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.construction, self.application,
                             self.matching, self.frequency, self.piA, self.piM)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the High Frequency High Power
        Bipolar Transistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piA * piM * piQ * piE'

            # Set the base hazard rate for the model.
            self.base_hr = 0.032 * exp(0.354 * self.frequency +
                                       0.00558 * self.operating_power)
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
# TODO: Adjust equation to account for CR voltages as in MIL-HDBK-217F.
            if self.construction == 1:
                self.piT = 0.1 * exp(-2903.0 * ((1.0 /
                                                 (self.junction_temperature +
                                                  273.0)) - (1.0 / 373.0)))
            else:
                self.piT = 0.38 * exp(-5794.0 * ((1.0 /
                                                  (self.junction_temperature +
                                                   273.0)) - (1.0 / 373.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the power rating factor for the model.
            if self.application == 1:
                self.piA = 7.6
            else:
                self.piA = 0.06 * self.duty_cycle + 0.4
            self.hazard_rate_model['piA'] = self.piA

            # Set the voltage stress factor for the model.
            self.piM = self._lst_piM[self.matching - 1]
            self.hazard_rate_model['piM'] = self.piM

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the High Frequency High Power Bipolar
        Transistor is overstressed based on it's rated values and operating
        environment.

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
            if self.operating_power > 0.70 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 70% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.75 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 70% rated voltage.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
                _reason_num += 1
        else:
            if self.operating_power > 0.90 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 90% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 90% rated voltage.\n"
                _reason_num += 1

        self.reason = _reason

        return False
