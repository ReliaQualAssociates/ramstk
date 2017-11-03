#!/usr/bin/env python
"""
#################################################
Transistor Package Field Effect Transistor Module
#################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.transistor.FET.py is part of
#       the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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


class HFSiFET(Semiconductor):
    """
    The High Frequency Silicon Field Effect Transistor data model contains the
    attributes and methods of a High Frequency Field Effect Transistor
    component.  The attributes of a High Frequency Field Effect Transistor are:

    :cvar subcategory: default value: 20

    :ivar type: default value: 0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.9.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                14.0, 32.0, 320.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.5, 1.0, 2.0, 5.0]
    _lst_lambdab_count = [0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53,
                          1.1, 0.51, 0.0069, 0.25, 0.68, 5.3]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 20

    def __init__(self):
        """
        Method to initialize a High Frequency Field Effect Transistor data
        model instance.
        """

        super(HFSiFET, self).__init__()

        # Initialize public scalar attributes.
        self.type = 0                       # FET type index.

    def set_attributes(self, values):
        """
        Sets the High Frequency Field Effect Transistor data model attributes.

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
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the High Frequency Field Effect
        Transistor data model attributes.

        :return: (type)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.type, )

        return _values

    def calculate_part(self):
        """
        Calculates the hazard rate for the High Frequency Field Effect
        Transistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piQ * piE'

            # Set the base hazard rate for the model.
            if self.type == 1:              # MOSFET
                self.base_hr = 0.060
            else:                           # JFET
                self.base_hr = 0.023
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-1925.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Determines whether the High Frequency Field Effect Transistor is
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


class LFSiFET(Semiconductor):
    """
    The Low Frequency Silicon Field Effect Transistor data model contains the
    attributes and methods of a Low Frequency Silicon Field Effect Transistor
    component.  The attributes of a Low Frequency Silicon Field Effect
    Transistor are:

    :cvar subcategory: default value: 15

    :ivar application: default value: 0
    :ivar type: default value: 0
    :ivar piA: default value: 0.0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.4.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                14.0, 32.0, 320.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_lambdab_count = [0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53,
                          1.1, 0.51, 0.0069, 0.25, 0.68, 5.3]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 15

    def __init__(self):
        """
        Initialize a Low Frequency Silicon Field Effect Transistor data model
        instance.
        """

        super(LFSiFET, self).__init__()

        # Initialize public scalar attributes.
        self.application = 0                # Application index.
        self.type = 0                       # Type index.
        self.piA = 0.0                      # Application pi factor.

    def set_attributes(self, values):
        """
        Sets the Low Frequency Silicon FET data model attributes.

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
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Low Frequency Silicon FET data
        model attributes.

        :return: (application, type, piA)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.application, self.type, self.piA)

        return _values

    def calculate_part(self):
        """
        Calculates the hazard rate for the Low Frequency Silicon FET
        Transistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 11.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piA * piQ * piE'

            # Set the base hazard rate for the model.
            if self.type == 1:              # MOSFET
                self.base_hr = 0.012
            else:                           # JFET
                self.base_hr = 0.0045
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-1925.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))

            self.hazard_rate_model['piT'] = self.piT

            # Set the application factor for the model.
            if self.rated_power < 2.0:
                if self.application == 1:   # Linear amplification
                    self.piA = 1.5
                else:                       # Small signal switching
                    self.piA = 0.7
            elif self.rated_power >= 2.0 and self.rated_power < 5.0:
                self.piA = 2.0
            elif self.rated_power >= 5.0 and self.rated_power < 50.0:
                self.piA = 4.0
            elif self.rated_power >= 50.0 and self.rated_power < 250.0:
                self.piA = 8.0
            elif self.rated_power >= 250.0:
                self.piA = 10.0
            self.hazard_rate_model['piA'] = self.piA

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Determines whether the Low Frequency Silicon Field Effect Transistor is
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


class HFGaAsFET(Semiconductor):
    """
    The High Frequency GaAs Field Effect Transistor data model contains the
    attributes and methods of a High Frequency GaAs Field Effect Transistor
    component.  The attributes of a High Frequency GaAs FET
    Transistor are:

    :cvar subcategory: default value: 19

    :ivar application: default value: 0
    :ivar matching: default value: 0
    :ivar frequency: default value: 0.0
    :ivar piA: default value: 0.0
    :ivar piM: default value: 0.0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.8.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piM = [1.0, 2.0, 4.0]
    _lst_piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5, 7.5,
                24.0, 250.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.5, 1.0, 2.0, 5.0]
    _lambdab_count = [[0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2, 7.2,
                       0.083, 2.8, 11.0, 63.0],
                      [0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0, 18.0,
                       0.21, 6.9, 27.0, 160.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 19

    def __init__(self):
        """
        Method to initialize a High Frequency GaAs Field Effect Transistor data
        model instance.
        """

        super(HFGaAsFET, self).__init__()

        # Initialize private list attributes.
        self._lst_lambdab_count = []

        # Initialize public scalar attributes.
        self.application = 0                # Application index.
        self.matching = 0                   # Matching index.
        self.frequency = 0.0                # Operating frequency.
        self.piA = 0.0                      # Application pi factor.
        self.piM = 0.0                      # Matching network pi factor.

    def set_attributes(self, values):
        """
        Method to set the High Frequency GaAs Field Effect Transistor data
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
            self.application = int(values[117])
            self.matching = int(values[118])
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
        Method to retrieve the current values of the High Frequency GaAs FET
        data model attributes.

        :return: (application, matching, frequency, piA, piM)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.application, self.matching, self.frequency,
                             self.piA, self.piM)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the High Frequency GaAs FET
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            if self.operating_power < 0.1:
                self._lst_lambdab_count = self._lambdab_count[0]
            else:
                self._lst_lambdab_count = self._lambdab_count[1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piA * piM * piQ * piE'

            # Set the base hazard rate for the model.
            if self.operating_power < 0.1:
                self.base_hr = 0.052
            elif self.frequency >= 4.0 and self.operating_power >= 0.1:
                self.base_hr = 0.0093 * exp(0.429 * self.frequency +
                                            0.486 * self.operating_power)
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
# TODO: Adjust equation to account for CR voltages as in MIL-HDBK-217F.
            self.piT = 0.1 * exp(-4485.0 * ((1.0 / (self.junction_temperature +
                                                    273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the power rating factor for the model.
            if self.application == 1:       # Low power or pulsed.
                self.piA = 1.0
            else:
                self.piA = 4.0
            self.hazard_rate_model['piA'] = self.piA

            # Set the matching network factor for the model.
            self.piM = self._lst_piM[self.matching - 1]
            self.hazard_rate_model['piM'] = self.piM

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the High Frequency GaAs Field Effect
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
            if self.operating_voltage > 0.70 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 70% rated voltage.\n"
                _reason_num += 1
            if self.junction_temperature > 135.0:
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
