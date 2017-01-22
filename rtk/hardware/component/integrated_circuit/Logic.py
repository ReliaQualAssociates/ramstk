#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.Logic.py is part of the RTK
#       Project
#
# All rights reserved.

"""
#########################################################
Hardware.Component.IntegratedCircuit Package Logic Module
#########################################################
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


class Logic(IntegratedCircuit):
    """
    The Logic IC data model contains the attributes and methods of a Logic IC
    component.  The attributes of a Logic IC are:

    :cvar subcategory: default value: 2

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _C1 = [[0.0025, 0.005, 0.01, 0.02, 0.04, 0.08],
           [0.01, 0.02, 0.04, 0.08, 0.16, 0.29]]
    _Ea = [[0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.45, 0.45, 0.5, 0.5, 0.6,
            0.6, 0.6],
           [0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35,
            0.35, 0.35, 0.35, 0.35]]
    _piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.25, 1.0, 2.0]
    _lst_lambdab_count = [[[0.0036, 0.012, 0.024, 0.024, 0.035, 0.025, 0.030,
                            0.032, 0.049, 0.047, 0.0036, 0.030, 0.069, 1.20],
                           [0.0060, 0.020, 0.038, 0.037, 0.055, 0.039, 0.048,
                            0.051, 0.077, 0.074, 0.0060, 0.046, 0.110, 1.90],
                           [0.0110, 0.035, 0.066, 0.065, 0.097, 0.070, 0.085,
                            0.091, 0.140, 0.130, 0.0110, 0.082, 0.190, 3.30],
                           [0.0330, 0.120, 0.220, 0.220, 0.330, 0.230, 0.280,
                            0.300, 0.460, 0.440, 0.0330, 0.280, 0.650, 12.0],
                           [0.0520, 0.170, 0.330, 0.330, 0.480, 0.340, 0.420,
                            0.450, 0.680, 0.650, 0.0520, 0.410, 0.950, 17.0],
                           [0.0750, 0.230, 0.440, 0.430, 0.630, 0.460, 0.560,
                            0.610, 0.900, 0.850, 0.0750, 0.530, 1.200, 21.0]],
                          [[0.0057, 0.015, 0.027, 0.027, 0.039, 0.029, 0.035,
                            0.039, 0.056, 0.052, 0.0057, 0.033, 0.074, 1.20],
                           [0.0100, 0.028, 0.045, 0.043, 0.062, 0.049, 0.057,
                            0.068, 0.092, 0.083, 0.0100, 0.053, 0.120, 1.90],
                           [0.0190, 0.047, 0.080, 0.077, 0.110, 0.088, 0.100,
                            0.120, 0.170, 0.150, 0.0190, 0.095, 0.210, 3.30],
                           [0.0490, 0.140, 0.250, 0.240, 0.360, 0.270, 0.320,
                            0.360, 0.510, 0.480, 0.0490, 0.300, 0.690, 12.0],
                           [0.0840, 0.220, 0.390, 0.370, 0.540, 0.420, 0.490,
                            0.560, 0.790, 0.720, 0.0840, 0.460, 1.000, 17.0],
                           [0.1300, 0.310, 0.530, 0.510, 0.730, 0.590, 0.690,
                            0.820, 1.100, 0.980, 0.1300, 0.830, 1.400, 21.0]]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 2                         # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a Logic IC data model instance.
        """

        super(Logic, self).__init__()

        # Initialize private list attributes.
        self._lambdab_count = []

        # Initialize public scalar attributes.
        self.technology = 0
        self.family = 0
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
        Sets the Logic IC data model attributes.

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
            self.family = int(values[135])
            self.package = int(values[136])
            self.n_gates = int(values[137])
            self.n_pins = int(values[138])
            self.years_production = float(values[139])
            self.case_temperature = float(values[140])
            self.C1 = float(values[141])
            self.C2 = float(values[142])
            self.piL = float(values[143])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Logic IC data model
        attributes.

        :return: (technology, family, package, n_gates, n_pins,
                  years_production, case_temperature, C1, C2, piL)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (self.technology, self.family, self.package,
                             self.n_gates, self.n_pins, self.years_production,
                             self.case_temperature, self.C1, self.C2, self.piL)

        return _values

    def calculate_part(self):

        """
        Calculates the hazard rate for the inductive Logic IC data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexixty metric = 20.
        from math import exp

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            if self.n_gates > 0 and self.n_gates < 101:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][0]
            elif self.n_gates > 100 and self.n_gates < 1001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][1]
            elif self.n_gates > 1000 and self.n_gates < 3001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][2]
            elif self.n_gates > 3000 and self.n_gates < 10001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][3]
            elif self.n_gates > 10000 and self.n_gates < 30001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][4]
            elif self.n_gates > 30000 and self.n_gates < 60001:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][5]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = '(C1 * piT + C2 * piE) * piQ * piL'

            # Die complexity failure rate.
            if self.n_gates > 0 and self.n_gates < 101:
                self.C1 = self._C1[self.technology - 1][0]
            elif self.n_gates > 100 and self.n_gates < 1001:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.n_gates > 1000 and self.n_gates < 3001:
                self.C1 = self._C1[self.technology - 1][2]
            elif self.n_gates > 3000 and self.n_gates < 10001:
                self.C1 = self._C1[self.technology - 1][3]
            elif self.n_gates > 10000 and self.n_gates < 30001:
                self.C1 = self._C1[self.technology - 1][4]
            elif self.n_gates > 30000 and self.n_gates < 60001:
                self.C1 = self._C1[self.technology - 1][5]
            self.hazard_rate_model['C1'] = self.C1

            # Temperature factor.
            self.junction_temperature = self.case_temperature + \
                                        self.operating_power * \
                                        self.thermal_resistance

            _Ea = self._Ea[self.technology - 1][self.family - 1]
            self.piT = 0.1 * exp((-_Ea / 8.617E-5) *
                                 ((1.0 / (self.junction_temperature + 273.0)) -
                                  (1.0 / 296.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Package failure rate.
            if self.package in [1, 2, 3]:
                _constant = [2.8E-4, 1.08]
            elif self.package == 4:
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
