#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.PALPLA.py is part of
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

"""
###########################################################
Hardware.Component.IntegratedCircuit Package PAL/PLA Module
###########################################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.integrated_circuit.IntegratedCircuit import \
         Model as IntegratedCircuit
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.integrated_circuit.IntegratedCircuit import \
         Model as IntegratedCircuit

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


class PALPLA(IntegratedCircuit):
    """
    The PAL/PLA IC data model contains the attributes and methods of a
    PAL/PLA IC component.  The attributes of a PAL/PLA IC are:

    :cvar subcategory: default value: 3

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _C1 = [[0.01, 0.021, 0.042], [0.00085, 0.0017, 0.0034, 0.0068]]
    _piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.25, 1.0, 2.0]
    _lst_lambdab_count = [[[0.0061, 0.016, 0.029, 0.027, 0.040, 0.032, 0.037,
                            0.044, 0.061, 0.054, 0.0061, 0.034, 0.076, 1.2],
                           [0.0110, 0.028, 0.048, 0.046, 0.065, 0.054, 0.063,
                            0.077, 0.100, 0.089, 0.0110, 0.057, 0.120, 1.9],
                           [0.0220, 0.052, 0.087, 0.082, 0.120, 0.099, 0.110,
                            0.140, 0.190, 0.160, 0.0220, 0.100, 0.220, 3.3]],
                          [[0.0046, 0.018, 0.035, 0.035, 0.052, 0.035, 0.044,
                            0.044, 0.070, 0.070, 0.0046, 0.044, 0.100, 1.9],
                           [0.0056, 0.021, 0.042, 0.042, 0.062, 0.042, 0.052,
                            0.053, 0.084, 0.083, 0.0056, 0.052, 0.120, 2.3],
                           [0.0061, 0.022, 0.043, 0.042, 0.063, 0.043, 0.054,
                            0.055, 0.086, 0.084, 0.0081, 0.053, 0.130, 2.3],
                           [0.0095, 0.033, 0.064, 0.063, 0.094, 0.065, 0.080,
                            0.083, 0.130, 0.130, 0.0095, 0.079, 0.190, 3.3]]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 3                         # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a PAL/PLA IC data model instance.
        """

        super(PALPLA, self).__init__()

        # Initialize private list attributes.
        self._lambdab_count = []

        # Initialize public scalar attributes.
        self.technology = 0
        self.package = 0
        self.n_gates = 0
        self.n_pins = 0
        self.years_production = 0.0
        self.case_temperature = 0.0
        self.C1 = 0.0
        self.C2 = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
        Sets the PAL/PLA IC data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = IntegratedCircuit.set_attributes(self, values[:134])

        try:
            self.technology = int(values[134])
            self.package = int(values[135])
            self.n_gates = int(values[136])
            self.n_pins = int(values[137])
            self.years_production = float(values[138])
            self.case_temperature = float(values[139])
            self.C1 = float(values[140])
            self.C2 = float(values[141])
            self.piL = float(values[142])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the PAL/PLA IC data model
        attributes.

        :return: (technology, package, n_gates, n_pins, years_production,
                  case_temperature, C1, C2, piL)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (self.technology, self.package, self.n_gates,
                             self.n_pins, self.years_production,
                             self.case_temperature, self.C1, self.C2, self.piL)

        return _values

    def calculate_part(self):
        """
        Calculates the hazard rate for the PAL/PLA IC data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor calculate_part; current McCabe Complexity metric = 14.
        from math import exp

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            if self.n_gates < 201:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][0]
            elif self.n_gates > 200 and self.n_gates < 1001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][1]
            elif self.n_gates > 1000 and self.n_gates < 5001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][2]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = '(C1 * piT + C2 * piE) * piQ * piL'

            # Die complexity failure rate.
            if self.n_gates < 201:
                self.C1 = self._C1[self.technology - 1][0]
            elif self.n_gates > 200 and self.n_gates < 1001:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.n_gates > 1000 and self.n_gates < 5001:
                self.C1 = self._C1[self.technology - 1][2]
            self.hazard_rate_model['C1'] = self.C1

            # Temperature factor.
            self.junction_temperature = self.case_temperature + \
                                        self.operating_power * \
                                        self.thermal_resistance

            self.piT = 0.1 * exp((-0.65 / 8.617E-5) *
                                 ((1.0 / (self.junction_temperature + 273.0)) -
                                  (1.0 / 296.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Package failure rate.
            if self.package in [1, 2, 3]:
                _constant = [2.8E-4, 1.08]
            elif self.package == 4:         # pragma: nocover
                _constant = [9.0E-5, 1.51]
            elif self.package == 5:         # pragma: nocover
                _constant = [3.0E-5, 1.82]
            elif self.package == 6:         # pragma: nocover
                _constant = [3.0E-5, 2.01]
            else:                           # pragma: nocover
                _constant = [3.6E-4, 1.08]
            self.C2 = _constant[0] * self.n_pins**_constant[1]
            self.hazard_rate_model['C2'] = self.C2

            # Learning factor.
            self.piL = 0.01 * exp(5.35 - 0.35 * self.years_production)
            self.hazard_rate_model['piL'] = self.piL

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return IntegratedCircuit.calculate_part(self)
