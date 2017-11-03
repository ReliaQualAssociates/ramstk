#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.Linear.py is part of the RTK
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
Hardware.Component.IntegratedCircuit Package Linear Module
##########################################################
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


class Linear(IntegratedCircuit):
    """
    The Linear IC data model contains the attributes and methods of a Linear IC
    component.  The attributes of a Linear IC are:

    :cvar subcategory: default value: 1

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _C1 = [[0.01, 0.02, 0.04, 0.06], [0.01, 0.02, 0.04, 0.06]]
    _piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.25, 1.0, 2.0]
    _lst_lambdab_count = [[0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062,
                           0.12, 0.13, 0.076, 0.0095, 0.044, 0.096, 1.1],
                          [0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110,
                           0.22, 0.24, 0.130, 0.0170, 0.072, 0.150, 1.4],
                          [0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190,
                           0.41, 0.44, 0.220, 0.0330, 0.120, 0.260, 2.0],
                          [0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300,
                           0.63, 0.67, 0.350, 0.0500, 0.190, 0.410, 3.4]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 1                         # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a Linear IC data model instance.
        """

        super(Linear, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lambdab_count = []

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.technology = 0
        self.package = 0
        self.n_transistors = 0
        self.n_pins = 0
        self.years_production = 0.0
        self.case_temperature = 0.0
        self.C1 = 0.0
        self.C2 = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
        Method to set the Linear IC data model attributes.

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
            self.n_transistors = int(values[136])
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
        Method to retrieve the current values of the Linear IC data model
        attributes.

        :return: (technology, package, n_transistors, n_pins, years_production,
                  case_temperature, C1, C2, piL)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (self.technology, self.package, self.n_transistors,
                             self.n_pins, self.years_production,
                             self.case_temperature, self.C1, self.C2, self.piL)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Linear IC data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate; current McCabe Complexity metrix = 16.
        from math import exp

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            if self.n_transistors > 0 and self.n_transistors < 101:
                self._lambdab_count = self._lst_lambdab_count[0]
            elif self.n_transistors > 100 and self.n_transistors < 301:
                self._lambdab_count = self._lst_lambdab_count[1]
            elif self.n_transistors > 300 and self.n_transistors < 1001:
                self._lambdab_count = self._lst_lambdab_count[2]
            elif self.n_transistors > 1000 and self.n_transistors < 10001:
                self._lambdab_count = self._lst_lambdab_count[3]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = '(C1 * piT + C2 * piE) * piQ * piL'

            # Die complexity failure rate.
            if self.n_transistors > 0 and self.n_transistors < 101:
                self.C1 = self._C1[self.technology - 1][0]
            elif self.n_transistors > 100 and self.n_transistors < 301:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.n_transistors > 300 and self.n_transistors < 1001:
                self.C1 = self._C1[self.technology - 1][2]
            elif self.n_transistors > 1000 and self.n_transistors < 10001:
                self.C1 = self._C1[self.technology - 1][3]
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
            else:
                _constant = [3.6E-4, 1.08]
            self.C2 = _constant[0] * self.n_pins**_constant[1]
            self.hazard_rate_model['C2'] = self.C2

            # Learning factor.
            self.piL = 0.01 * exp(5.35 - 0.35 * self.years_production)
            self.hazard_rate_model['piL'] = self.piL

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return IntegratedCircuit.calculate_part(self)
