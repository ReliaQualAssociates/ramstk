#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.fixed.Wirewound.py is part of the RTK
#       Project
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

"""
##########################################################
Hardware.Component.Resistor.Fixed Package Wirewound Module
##########################################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.resistor.Resistor import Model as Resistor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.resistor.Resistor import Model as Resistor

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


class Wirewound(Resistor):
    """
    The Wirewound resistor data model contains the attributes and methods of
    a Wirewound resistor.  The attributes of a Wirewound resistor are:

    :cvar list _lst_piR: list of MIL-HDBK-217FN2 resistance factor values.
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 29

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
        Method to initialize a Wirewound resistor data model instance.
        """

        super(Wirewound, self).__init__()

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Wirewound resistor data
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
                self.base_hr = 0.0031 * \
                    exp(((self.temperature_active + 273.0) / 398.0)**10.0) * \
                    exp((_stress * ((self.temperature_active + 273.0) /
                                    273.0))**1.5)
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

        return Resistor.calculate_part(self)


class WirewoundPower(Resistor):
    """
    The Wirewound Power resistor data model contains the attributes and
    methods of a Wirewound Power resistor.  The attributes of a Wirewound
    Power resistor are:

    :cvar list _lst_piR: list of MIL-HDBK-217FN2 resistance factor values.
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 30

    :ivar int specification: index of the specification applicable to the
                             resistor.
    :ivar int style: index of the resistor style.

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
        Method to initialize a Wirewound Power resistor data model instance.
        """

        super(WirewoundPower, self).__init__()

        self._lst_lambdab_count = []

        self.specification = 0
        self.style = 0

    def set_attributes(self, values):
        """
        Method to set the Wirewound Power resistor data model attributes.

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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Wirewound Power resistor
        data model attributes.

        :return: (specification, style)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.specification, self.style)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Wirewound Power resistor
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 19.
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
                    exp((_stress / 0.5) * ((self.temperature_active + 273.0) /
                                           273.0))
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
                elif self.resistance > 5000.0 and self.resistance <= 7500.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][3]
                elif self.resistance > 7500.0 and self.resistance <= 10000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][4]
                elif self.resistance > 10000.0 and self.resistance <= 15000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][5]
                elif self.resistance > 15000.0 and self.resistance <= 20000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][6]
                elif self.resistance > 20000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][7]
            elif self.specification == 2:   # MIL-R-26
                if self.resistance <= 100.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][0]
                elif self.resistance > 100.0 and self.resistance <= 1000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][1]
                elif self.resistance > 1000.0 and self.resistance <= 10000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][2]
                elif self.resistance > 10000.0 and self.resistance <= 100000.0:
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][3]
                elif(self.resistance > 100000.0 and
                     self.resistance <= 150000.0):
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][4]
                elif(self.resistance > 150000.0 and
                     self.resistance <= 200000.0):
                    self.piR = self._lst_piR[self.specification - 1][self.style - 1][5]

            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate_part(self)


class WirewoundChassisMount(Resistor):
    """
    The Wirewound Chassis Mount Power resistor data model contains the
    attributes and methods of a Wirewound Chassis Mount Power  resistor.  The
    attributes of a Wirewound Chassis Mount Power resistor are:

    :cvar list _lst_piR: list of MIL-HDBK-217FN2 resistance factor values.
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 31

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
        Method to initialize a Wirewound Chassis Mount Power resistor data
        model instance.
        """

        super(WirewoundChassisMount, self).__init__()

        self.characteristic = 0
        self.style = 0

    def set_attributes(self, values):
        """
        Method to set the Wirewound Chassis Mount Power resistor data model
        attributes.

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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Wirewound Chassis Mount
        Power resistor data model attributes.

        :return: (specification, style)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.characteristic, self.style)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Wirewound Chassis Mount
        Power resistor data model.

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
                           exp(2.64 * ((self.temperature_active + 273.0) /
                                       273.0)) * \
                           exp((_stress / -.466) * ((self.temperature_active +
                                                     273.0) / 273.0))
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Resistance factor.
            if self.resistance <= 500.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][0]
            elif self.resistance > 500.0 and self.resistance <= 1000.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][1]
            elif self.resistance > 1000.0 and self.resistance <= 5000.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][2]
            elif self.resistance > 5000.0 and self.resistance <= 10000.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][3]
            elif self.resistance > 10000.0 and self.resistance <= 20000.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][4]
            elif self.resistance > 20000.0:
                self.piR = self._lst_piR[self.characteristic - 1][self.style - 1][5]
            self.hazard_rate_model['piR'] = self.piR

        return Resistor.calculate_part(self)
