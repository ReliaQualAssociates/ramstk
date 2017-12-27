#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.Memory.py is part of
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
##########################################################
Hardware.Component.IntegratedCircuit Package Memory Module
##########################################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.integrated_circuit.IntegratedCircuit import \
         Model as IntegratedCircuit
except ImportError:  # pragma: no cover
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
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Memory(IntegratedCircuit):
    """
    The Memory IC data model contains the attributes and methods of a
    Memory IC component.  The attributes of a Memory IC are:

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [
        1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0, 34.0,
        610.0
    ]
    _piQ = [0.25, 1.0, 2.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 3  # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a Memory IC data model instance.
        """

        super(Memory, self).__init__()

        # Initialize private list attributes.
        self._lambdab_count = []

        # Initialize public scalar attributes.
        self.part_type = 0
        self.technology = 0
        self.package = 0
        self.ecc = 0
        self.memory_size = 0
        self.n_cycles = 0
        self.n_pins = 0
        self.manufacturing = 0
        self.years_production = 0.0
        self.case_temperature = 0.0
        self.life_op_hours = 0.0
        self.C1 = 0.0
        self.C2 = 0.0
        self.piL = 0.0
        self.lambda_cyc = 0.0

    def set_attributes(self, values):
        """
        Sets the Memory IC data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = IntegratedCircuit.set_attributes(self, values[:134])

        try:
            self.part_type = int(values[134])
            self.technology = int(values[135])
            self.package = int(values[136])
            self.ecc = int(values[137])
            self.memory_size = int(values[138])
            self.n_cycles = int(values[139])
            self.n_pins = int(values[140])
            self.manufacturing = int(values[141])
            self.years_production = float(values[142])
            self.case_temperature = float(values[143])
            self.life_op_hours = float(values[144])
            self.C1 = float(values[145])
            self.C2 = float(values[146])
            self.piL = float(values[147])
            self.lambda_cyc = float(values[148])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except (TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return (_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Memory IC data model
        attributes.

        :return: (part_type, technology, package, ecc, memory_size, n_cycles,
                  n_pins, years_production, case_temperature, life_op_hours,
                  C1, C2, piL, lambda_cyc, manufacturing)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (
            self.part_type, self.technology, self.package, self.ecc,
            self.memory_size, self.n_cycles, self.n_pins, self.manufacturing,
            self.years_production, self.case_temperature, self.life_op_hours,
            self.C1, self.C2, self.piL, self.lambda_cyc)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Memory IC data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model[
                'equation'] = '(C1 * piT + C2 * piE + lambdacyc) * piQ * piL'

            # Temperature factor.
            self.junction_temperature = self.case_temperature + \
                                        self.operating_power * \
                                        self.thermal_resistance

            self.piT = 0.1 * exp((-0.6 / 8.617E-5) *
                                 ((1.0 / (self.junction_temperature + 273.0)) -
                                  (1.0 / 296.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Package failure rate.
            if self.package in [1, 2, 3]:
                _constant = [2.8E-4, 1.08]
            elif self.package == 4:
                _constant = [9.0E-5, 1.51]
            elif self.package == 5:
                _constant = [3.0E-5, 1.82]
            elif self.package == 6:
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


class DRAM(Memory):
    """
    The DRAM data model contains the attributes and methods of a DRAM
    component.  The attributes of a DRAM IC are:

    :cvar subcategory: default value: 7

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2.
    """

    _C1 = [0.0013, 0.0025, 0.005, 0.01]
    _lst_lambdab_count = [[
        0.0040, 0.014, 0.027, 0.027, 0.040, 0.029, 0.035, 0.040, 0.059, 0.055,
        0.0040, 0.034, 0.080, 1.4
    ], [
        0.0055, 0.019, 0.039, 0.034, 0.051, 0.039, 0.047, 0.056, 0.079, 0.070,
        0.0055, 0.043, 0.100, 1.7
    ], [
        0.0074, 0.023, 0.043, 0.040, 0.060, 0.049, 0.058, 0.076, 0.100, 0.084,
        0.0074, 0.051, 0.120, 1.9
    ], [
        0.0110, 0.032, 0.057, 0.053, 0.077, 0.070, 0.080, 0.120, 0.150, 0.110,
        0.0110, 0.067, 0.150, 2.3
    ]]

    subcategory = 7

    def __init__(self):
        """
        Initialize a DRAM data model instance.
        """

        super(DRAM, self).__init__()

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the DRAM data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor DRAM.calculate_part; current McCabe Complexity metric = 11.
        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            if self.memory_size < 16001:
                self._lambdab_count = self._lst_lambdab_count[0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self._lambdab_count = self._lst_lambdab_count[1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self._lambdab_count = self._lst_lambdab_count[2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self._lambdab_count = self._lst_lambdab_count[3]

        elif self.hazard_rate_type == 2:
            # Die complexity failure rate.
            if self.memory_size < 16001:
                self.C1 = self._C1[0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self.C1 = self._C1[1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self.C1 = self._C1[2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self.C1 = self._C1[3]
            self.hazard_rate_model['C1'] = self.C1

            self.hazard_rate_model['lambdacyc'] = 0.0

        return Memory.calculate_part(self)


class EEPROM(Memory):
    """
    The EEPROM data model contains the attributes and methods of an EEPROM
    component.  The attributes of a EEPROM IC are:

    :cvar subcategory: default value: 6

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2.
    """

    _C1 = [[0.0094, 0.019, 0.038, 0.075], [0.00085, 0.0017, 0.0034, 0.0068]]
    _piECC = [1.0, 0.72, 0.68]
    _lst_lambdab_count = [[[
        0.010, 0.028, 0.050, 0.046, 0.067, 0.082, 0.070, 0.10, 0.13, 0.096,
        0.010, 0.058, 0.13, 1.9
    ], [
        0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18, 0.21, 0.140,
        0.017, 0.081, 0.18, 2.3
    ], [
        0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.160, 0.30, 0.33, 0.190,
        0.028, 0.110, 0.23, 2.3
    ], [
        0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56, 0.61, 0.330,
        0.053, 0.190, 0.39, 3.4
    ]], [[
        0.0049, 0.018, 0.036, 0.036, 0.053, 0.037, 0.046, 0.049, 0.075, 0.072,
        0.0048, 0.045, 0.11, 1.9
    ], [
        0.0061, 0.022, 0.044, 0.043, 0.064, 0.046, 0.056, 0.062, 0.093, 0.087,
        0.0062, 0.054, 0.13, 2.3
    ], [
        0.0072, 0.024, 0.048, 0.045, 0.067, 0.051, 0.061, 0.073, 0.100, 0.092,
        0.0072, 0.057, 0.13, 2.3
    ], [
        0.0120, 0.038, 0.071, 0.068, 0.100, 0.080, 0.095, 0.120, 0.180, 0.140,
        0.0120, 0.086, 0.20, 3.3
    ]]]

    subcategory = 6

    def __init__(self):
        """
        Initialize a EEPROM data model instance.
        """

        super(EEPROM, self).__init__()

        self.piECC = 0.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the EEPROM data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor EEPROM.calculate_part; current McCabe Complexity metric = 23.
        from math import exp

        self.hazard_rate_model = {}

        self.piQ = self._piQ[self.quality - 1]

        if self.hazard_rate_type == 1:
            if self.memory_size < 16001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][3]

        elif self.hazard_rate_type == 2:
            # Die complexity failure rate.
            if self.memory_size < 16001:
                self.C1 = self._C1[self.technology - 1][0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self.C1 = self._C1[self.technology - 1][2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self.C1 = self._C1[self.technology - 1][3]
            self.hazard_rate_model['C1'] = self.C1

            # Error correction code failure rate.
            self.piECC = self._piECC[self.ecc - 1]

            # Programming cycles failure rate.
            if self.manufacturing == 1:  # FLOTOX
                _A1 = 6.817E-6 * self.n_cycles
                _A2 = 0.0
                _B1 = ((self.memory_size / 16000.0)**0.5) * \
                      exp((-0.15 / 8.63E-5) *
                          ((1.0 / (self.junction_temperature + 273.0)) -
                           (1.0 / 333.0)))
                _B2 = 0.0
            else:
                if self.n_cycles < 101:
                    _A1 = 0.0097
                elif self.n_cycles > 100 and self.n_cycles < 201:
                    _A1 = 0.014
                elif self.n_cycles > 200 and self.n_cycles < 501:
                    _A1 = 0.023
                elif self.n_cycles > 500 and self.n_cycles < 1001:
                    _A1 = 0.033
                elif self.n_cycles > 1000 and self.n_cycles < 3001:
                    _A1 = 0.061
                elif self.n_cycles > 3000 and self.n_cycles < 7001:
                    _A1 = 0.14
                else:
                    _A1 = 0.3

                if self.n_cycles < 300001:
                    _A2 = 0.0
                elif self.n_cycles > 300000 and self.n_cycles < 400001:
                    _A2 = 1.1
                else:
                    _A2 = 2.3

                _B1 = ((self.memory_size / 64000.0)**0.25) * \
                      exp((-0.12 / 8.63E-5) *
                          ((1.0 / (self.junction_temperature + 273.0)) -
                           (1.0 / 303.0)))
                _B2 = ((self.memory_size / 64000.0)**0.25) * \
                      exp((-0.1 / 8.63E-5) *
                          ((1.0 / (self.junction_temperature + 273.0)) -
                           (1.0 / 303.0)))

            self.lambda_cyc = (_A1 * _B1 + _A2 * _B2 / self.piQ) * self.piECC
            self.hazard_rate_model['lambdacyc'] = self.lambda_cyc

        return Memory.calculate_part(self)


class ROM(Memory):
    """
    The ROM data model contains the attributes and methods of a ROM component.
    The attributes of a ROM IC are:

    :cvar subcategory: default value: 5

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2.
    """

    _C1 = [[0.0094, 0.019, 0.038, 0.075], [0.00085, 0.0017, 0.0034, 0.0068]]
    _lst_lambdab_count = [[[
        0.010, 0.028, 0.050, 0.046, 0.067, 0.062, 0.070, 0.10, 0.13, 0.096,
        0.010, 0.058, 0.13, 1.9
    ], [
        0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18, 0.21, 0.140,
        0.017, 0.081, 0.18, 2.3
    ], [
        0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.180, 0.30, 0.33, 0.190,
        0.028, 0.110, 0.23, 2.3
    ], [
        0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56, 0.61, 0.330,
        0.053, 0.190, 0.39, 3.4
    ]], [[
        0.0047, 0.018, 0.036, 0.035, 0.053, 0.037, 0.045, 0.048, 0.074, 0.071,
        0.0047, 0.044, 0.11, 1.9
    ], [
        0.0059, 0.022, 0.043, 0.042, 0.063, 0.045, 0.055, 0.060, 0.090, 0.086,
        0.0059, 0.053, 0.13, 2.3
    ], [
        0.0067, 0.023, 0.045, 0.044, 0.066, 0.048, 0.059, 0.068, 0.099, 0.089,
        0.0067, 0.055, 0.13, 2.3
    ], [
        0.0110, 0.036, 0.068, 0.066, 0.098, 0.075, 0.090, 0.110, 0.150, 0.140,
        0.0110, 0.083, 0.20, 3.3
    ]]]

    subcategory = 5

    def __init__(self):
        """
        Initialize a ROM data model instance.
        """

        super(ROM, self).__init__()

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the ROM data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor ROM.calculate_part; current McCabe Complexity metric = 11.
        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            if self.memory_size < 16001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][3]

        elif self.hazard_rate_type == 2:
            # Die complexity failure rate.
            if self.memory_size < 16001:
                self.C1 = self._C1[self.technology - 1][0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self.C1 = self._C1[self.technology - 1][2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self.C1 = self._C1[self.technology - 1][3]
            self.hazard_rate_model['C1'] = self.C1

            self.hazard_rate_model['lambdacyc'] = 0.0

        return Memory.calculate_part(self)


class SRAM(Memory):
    """
    The SRAM data model contains the attributes and methods of a SRAM
    component.  The attributes of a SRAM IC are:

    :cvar subcategory: default value: 8

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2.
    """

    _C1 = [[0.0062, 0.011, 0.021, 0.042], [0.0062, 0.011, 0.021, 0.042]]
    _lst_lambdab_count = [[[
        0.0075, 0.023, 0.043, 0.041, 0.060, 0.050, 0.058, 0.077, 0.10, 0.084,
        0.0075, 0.052, 0.12, 1.9
    ], [
        0.0120, 0.033, 0.058, 0.054, 0.079, 0.072, 0.083, 0.120, 0.15, 0.110,
        0.0120, 0.069, 0.15, 2.3
    ], [
        0.0180, 0.045, 0.074, 0.065, 0.095, 0.100, 0.110, 0.190, 0.22, 0.140,
        0.0180, 0.084, 0.18, 2.3
    ], [
        0.0330, 0.079, 0.130, 0.110, 0.160, 0.180, 0.200, 0.350, 0.39, 0.240,
        0.0330, 0.140, 0.30, 3.4
    ]], [[
        0.0079, 0.022, 0.038, 0.034, 0.050, 0.048, 0.054, 0.083, 0.10, 0.073,
        0.0079, 0.044, 0.098, 1.4
    ], [
        0.0140, 0.034, 0.057, 0.050, 0.073, 0.077, 0.085, 0.140, 0.17, 0.110,
        0.0140, 0.065, 0.140, 1.8
    ], [
        0.0230, 0.053, 0.084, 0.071, 0.100, 0.120, 0.130, 0.250, 0.27, 0.160,
        0.0230, 0.092, 0.190, 1.9
    ], [
        0.0430, 0.092, 0.140, 0.110, 0.160, 0.220, 0.230, 0.460, 0.49, 0.260,
        0.0430, 0.150, 0.300, 2.3
    ]]]

    subcategory = 8

    def __init__(self):
        """
        Method to initialize a SRAM data model instance.
        """

        super(SRAM, self).__init__()

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the SRAM data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor SRAM.calculate_part; current McCabe Complexity metric = 11.
        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            if self.memory_size < 16001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self._lambdab_count = self._lst_lambdab_count[self.technology
                                                              - 1][3]

        elif self.hazard_rate_type == 2:
            # Die complexity failure rate.
            if self.memory_size < 16001:
                self.C1 = self._C1[self.technology - 1][0]
            elif self.memory_size > 16000 and self.memory_size < 64001:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.memory_size > 64000 and self.memory_size < 256001:
                self.C1 = self._C1[self.technology - 1][2]
            elif self.memory_size > 256000 and self.memory_size < 1000001:
                self.C1 = self._C1[self.technology - 1][3]
            self.hazard_rate_model['C1'] = self.C1

            self.hazard_rate_model['lambdacyc'] = 0.0

        return Memory.calculate_part(self)
