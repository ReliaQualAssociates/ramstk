#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.inductor.Coil.py is part of the RTK Project
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
###############################################
Hardware.Component.Inductor Package Coil Module
###############################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.inductor.Inductor import Model as Inductor
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.inductor.Inductor import Model as Inductor

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


class Coil(Inductor):
    """
    The inductive Coil data model contains the attributes and methods of an
    inductive Coil component.  The attributes of an inductive Coil are:

    :cvar int subcategory: default value: 63

    :ivar int construction: the index in the construction list for the Coil.
    :ivar float piC: the MIL-HDBK-217FN2 construction factor.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 11.2.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piC = [1.0, 2.0]
    _piE = [
        1.0, 4.0, 12.0, 5.0, 16.0, 5.0, 7.0, 6.0, 8.0, 24.0, 0.5, 13.0, 34.0,
        610.0
    ]
    _piQ = [0.03, 0.1, 0.3, 1.0, 4.0, 20.0]
    _lambdab_count = [[
        0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022,
        0.052, 0.00083, 0.25, 0.073, 1.1
    ], [
        0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044, 0.10,
        0.0017, 0.05, 0.15, 2.2
    ]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 63  # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize an inductive Coil data model instance.
        """

        super(Coil, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.construction = 0
        self.piC = 0.0

    def set_attributes(self, values):
        """
        Method to set the inductive Coil data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Inductor.set_attributes(self, values[:136])

        try:
            self.piC = float(values[136])
            self.construction = int(values[137])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except (TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return (_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the inductive Coil data model
        attributes.

        :return: (technology, n_wave_soldered, n_hand_soldered,
                  n_circuit_planes, piC)
        :rtype: tuple
        """

        _values = Inductor.get_attributes(self)

        _values = _values + (self.piC, self.construction)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the inductive Coil data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor calculate_part; current McCabe Complexity metric = 11.
        from math import exp

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            self._lambdab_count = self._lambdab_count[self.construction - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piC * piQ * piE'

            # Hot spot temperature.
            if self.specification == 2:
                if self.insulation_class == 1:
                    self.hot_spot_temperature = self.temperature_active + 16.5
                else:
                    self.hot_spot_temperature = self.temperature_active + 38.5
            else:
                self.hot_spot_temperature = self.temperature_active + 16.5

            # Base hazard rate.
            if self.specification == 1 and self.insulation_class == 1:
                _constant = [0.000335, 329.0, 15.6]
            elif (self.specification == 1 and self.insulation_class == 2) or \
                 (self.specification == 2 and self.insulation_class == 1):
                _constant = [0.000379, 352.0, 14.0]
            elif (self.specification == 1 and self.insulation_class == 3) or \
                 (self.specification == 2 and self.insulation_class == 2):
                _constant = [0.000319, 364.0, 8.7]
            elif (self.specification == 1 and self.insulation_class == 4) or \
                 (self.specification == 2 and self.insulation_class == 3):
                _constant = [0.00035, 409, 10.0]

            self.base_hr = _constant[0] * \
                           exp(((self.hot_spot_temperature + 273.0) /
                                _constant[1])**_constant[2])

            # Construction factor.
            self.piC = self._piC[self.construction - 1]
            self.hazard_rate_model['piC'] = self.piC

            # Quality factor.
            self.piQ = self._piQ[self.quality - 1]

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return Inductor.calculate_part(self)
