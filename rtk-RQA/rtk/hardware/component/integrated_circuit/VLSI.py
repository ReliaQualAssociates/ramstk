#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.VLSI.py is part of
#       the RTK Project
#
# All rights reserved.

"""
########################################################
Hardware.Component.IntegratedCircuit Package VLSI Module
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


class VLSI(IntegratedCircuit):
    """
    The VLSI IC data model contains the attributes and methods of a
    VLSI IC component.  The attributes of a VLSI IC are:

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
    _C1 = [[4.5, 7.2], [25.0, 51.0]]
    _lst_lambdab_count = [[0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16,
                           0.16, 0.16, 0.16, 0.16, 0.16, 0.16],
                          [0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24,
                           0.24, 0.24, 0.24, 0.24, 0.24, 0.24]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 10                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a VLSI IC data model instance.
        """

        super(VLSI, self).__init__()

        # Initialize private list attributes.
        self._lambdab_count = []

        # Initialize public scalar attributes.
        self.application = 0
        self.package = 0
        self.n_pins = 0
        self.manufacturing = 0
        self.years_production = 0.0
        self.case_temperature = 0.0
        self.feature_size = 0.0
        self.esd_susceptibility = 1000.0
        self.lambda_bd = 0.0
        self.lambda_bp = 0.0
        self.lambda_eos = 0.0
        self.piMFG = 0.0
        self.piCD = 0.0
        self.piPT = 0.0
        self.die_area = 0.0

    def set_attributes(self, values):
        """
        Sets the VLSI IC data model attributes.

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
            self.n_pins = int(values[136])
            self.manufacturing = int(values[137])
            self.years_production = float(values[138])
            self.case_temperature = float(values[139])
            self.feature_size = float(values[140])
            self.esd_susceptibility = float(values[141])
            self.lambda_bd = float(values[142])
            self.lambda_bp = float(values[143])
            self.lambda_eos = float(values[144])
            self.piMFG = float(values[145])
            self.piCD = float(values[146])
            self.piPT = float(values[147])
            self.die_area = float(values[148])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the VLSI IC data model attributes.

        :return: (application, package, n_pins, manufacturing,
                  years_production, case_temperature, feature_size,
                  esd_susceptibility, lambda_bd, lambda_bp, lambda_eos,
                  piMFG, piCD, piPT, die_area)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (self.application, self.package, self.n_pins,
                             self.manufacturing, self.years_production,
                             self.case_temperature, self.feature_size,
                             self.esd_susceptibility, self.lambda_bd,
                             self.lambda_bp, self.lambda_eos, self.piMFG,
                             self.piCD, self.piPT, self.die_area)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the VLSI IC data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 13.
        from math import exp, log

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            self._lambdab_count = self._lst_lambdab_count[self.application - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambda_bd * piMFG * piT * piCD + lambda_bp * piE * piQ * piPT + lambda_eos'

            # Die base failure rate.
            if self.application == 1:
                self.lambda_bd = 0.16
            else:
                self.lambda_bd = 0.24
            self.hazard_rate_model['lambda_bd'] = self.lambda_bd

            # Package base failure rate.
            self.lambda_bp = 0.0022 + (1.72E-5 * self.n_pins)
            self.hazard_rate_model['lambda_bp'] = self.lambda_bp

            # Electrical overstress failure rate.
            self.lambda_eos = (-log(1.0 - 0.00057 * exp(-0.0002 * self.esd_susceptibility))) / 0.00876
            self.hazard_rate_model['lambda_eos'] = self.lambda_eos

            # Manufacturing process factor.
            if self.manufacturing == 1:
                self.piMFG = 0.55
            else:
                self.piMFG = 2.0
            self.hazard_rate_model['piMFG'] = self.piMFG

            # Temperature factor.
            self.junction_temperature = self.case_temperature + \
                                        self.operating_power * \
                                        self.thermal_resistance

            self.piT = 0.1 * exp((-0.35 / 8.617E-5) *
                                 ((1.0 / (self.junction_temperature + 273.0)) -
                                  (1.0 / 296.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Die complexity factor.
            self.piCD = (0.64 * (self.die_area / 0.21) *
                         (2.0 / self.feature_size)**2.0) + 0.36
            self.hazard_rate_model['piCD'] = self.piCD

            # Package type factor.
            if self.package == 1:           # Hermetic DIP
                self.piPT = 1.0
            elif self.package == 2:         # Non-Hermetic DIP
                self.piPT = 1.3
            elif self.package == 3:         # Hermetic PGA
                self.piPT = 2.2
            elif self.package == 4:         # Non-Hermetic PGA
                self.piPT = 2.9
            elif self.package == 5:         # Hermetic SMT
                self.piPT = 4.7
            elif self.package == 6:         # Non-Hermetic SMT
                self.piPT = 6.1
            self.hazard_rate_model['piPT'] = self.piPT

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return IntegratedCircuit.calculate_part(self)
