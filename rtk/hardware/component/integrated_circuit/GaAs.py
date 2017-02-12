#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.GaAs.py is part of
#       the RTK Project
#
# All rights reserved.

"""
########################################################
Hardware.Component.IntegratedCircuit Package GaAs Module
########################################################
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


class GaAs(IntegratedCircuit):
    """
    The GaAs IC data model contains the attributes and methods of a
    GaAs IC component.  The attributes of a GaAs IC are:

    :cvar subcategory: default value: 3

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _Ea = [1.5, 1.5, 1.5, 1.4]
    _piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.25, 1.0, 2.0]
    _piA = [1.0, 3.0, 3.0, 1.0]
    _C1 = [[4.5, 7.2], [4.5, 7.2], [4.5, 7.2], [25.0, 51.0]]

    _lst_lambdab_count = [[0.019, 0.034, 0.046, 0.039, 0.052, 0.065, 0.068,
                           0.11, 0.12, 0.076, 0.019, 0.049, 0.086, 0.61],
                          [0.025, 0.047, 0.067, 0.058, 0.079, 0.091, 0.097,
                           0.15, 0.17, 0.11, 0.025, 0.073, 0.14, 1.3],
                          [0.0085, 0.030, 0.057, 0.057, 0.084, 0.060, 0.073,
                           0.080, 0.12, 0.11, 0.0085, 0.071, 0.17, 3.0],
                          [0.0140, 0.053, 0.100, 0.100, 0.150, 0.110, 0.130,
                           0.140, 0.22, 0.21, 0.0140, 0.130, 0.31, 5.5]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 9                         # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a GaAs IC data model instance.
        """

        super(GaAs, self).__init__()

        # Initialize private list attributes.
        self._lambdab_count = []

        # Initialize public scalar attributes.
        self.application = 0
        self.package = 0
        self.n_elements = 0
        self.n_pins = 0
        self.years_production = 0.0
        self.case_temperature = 0.0
        self.C1 = 0.0
        self.C2 = 0.0
        self.piL = 0.0
        self.piA = 0.0

    def set_attributes(self, values):
        """
        Sets the GaAs IC data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = IntegratedCircuit.set_attributes(self, values[:134])

        try:
            self.application = int(values[134])
            self.package = int(values[135])
            self.n_elements = int(values[136])
            self.n_pins = int(values[137])
            self.years_production = float(values[138])
            self.case_temperature = float(values[139])
            self.C1 = float(values[140])
            self.C2 = float(values[141])
            self.piL = float(values[142])
            self.piA = float(values[143])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the GaAs IC data model attributes.

        :return: (application, package, n_elements, n_pins, years_production,
                  case_temperature, C1, C2, piL, piA)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (self.application, self.package, self.n_elements,
                             self.n_pins, self.years_production,
                             self.case_temperature, self.C1, self.C2, self.piL,
                             self.piA)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the GaAs IC data model.

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

            if self.application < 4 and self.n_elements < 11:
                self._lambdab_count = self._lst_lambdab_count[0]
            elif self.application < 4 and self.n_elements > 10:
                self._lambdab_count = self._lst_lambdab_count[1]
            elif self.application == 4 and self.n_elements < 1001:
                self._lambdab_count = self._lst_lambdab_count[2]
            else:
                self._lambdab_count = self._lst_lambdab_count[3]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = '(C1 * piT * piA + C2 * piE) * piQ * piL'

            # Die complexity factor.
            if (self.application < 4 and self.n_elements < 101) or \
               (self.application == 4 and self.n_elements < 1001):
                self.C1 = self._C1[self.application - 1][0]
            else:
                self.C1 = self._C1[self.application - 1][1]
            self.hazard_rate_model['C1'] = self.C1

            # Temperature factor.
            self.junction_temperature = self.case_temperature + \
                                        self.operating_power * \
                                        self.thermal_resistance

            _Ea = self._Ea[self.application - 1]
            self.piT = 0.1 * exp((-_Ea / 8.617E-5) *
                                 ((1.0 / (self.junction_temperature + 273.0)) -
                                  (1.0 / 423.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Application factor.
            self.piA = self._piA[self.application - 1]
            self.hazard_rate_model['piA'] = self.piA

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
