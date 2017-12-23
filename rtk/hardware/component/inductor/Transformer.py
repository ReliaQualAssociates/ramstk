#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.inductor.Transformer.py is part of the RTK
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
######################################################
Hardware.Component.Inductor Package Transformer Module
######################################################
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


class Transformer(Inductor):
    """
    The Transformer data model contains the attributes and methods of a
    Transformer component.  The attributes of a Transformer are:

    :cvar int subcategory: default value: 62

    :ivar int family: the index in the transformer family list.
    :ivar float power_loss: the power dissipation in watts of the transformer.
                            Used to calculate the temperature rise of the
                            transformer.
    :ivar float case_area: the radiating surface area in square inches of the
                           transformer case.  Used to calculate the temperature
                           rise of the transformer.
    :ivar float weight: the weight in pounds of the transformer.  Used to
                        calculate the temperature rise of the transformer.
    :ivar float input_power: the input power in watts of the transformer.  Used
                             to calculate the temperature rise of the
                             transformer.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 11.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [
        1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0, 34.0,
        610.0
    ]
    _piQ = [[1.5, 5.0], [3.0, 7.5], [8.0, 30.0], [12.0, 30.0]]
    _lambdab_count = [[
        0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22,
        0.035, 0.11, 0.31, 4.7
    ], [
        0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011,
        0.37, 1.2, 16.0
    ], [
        0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052, 0.11,
        0.0018, 0.053, 0.16, 2.3
    ], [
        0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015,
        0.42, 1.2, 19.0
    ]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 62  # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a Transformer data model instance.
        """

        super(Transformer, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.family = 0
        self.power_loss = 0.0
        self.case_area = 0.0
        self.weight = 0.0
        self.input_power = 0.0

    def set_attributes(self, values):
        """
        Method to set the Transformer data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Inductor.set_attributes(self, values[:136])

        try:
            self.power_loss = float(values[136])
            self.case_area = float(values[137])
            self.weight = float(values[138])
            self.input_power = float(values[139])
            self.family = int(values[140])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except (TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return (_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Transformer data model
        attributes.

        :return: (family, power_loss, case_area, weight, input_power)
        :rtype: tuple
        """

        _values = Inductor.get_attributes(self)

        _values = _values + (self.power_loss, self.case_area, self.weight,
                             self.input_power, self.family)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the inductive Transformer data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor calculate_part; current McCabe Complexity metric = 12.
        from math import exp

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.family - 1][self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            self._lambdab_count = self._lambdab_count[self.family - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Hot spot temperature.
            if self.power_loss > 0.0 and self.case_area > 0.0:
                self.hot_spot_temperature = self.temperature_active + \
                    1.1 * (125.0 * self.power_loss / self.case_area)
            elif self.power_loss > 0.0 and self.weight > 0.0:
                self.hot_spot_temperature = self.temperature_active + \
                    1.1 * (11.5 * self.power_loss / self.weight**0.6766)
            elif self.input_power > 0.0 and self.weight > 0.0:
                self.hot_spot_temperature = self.temperature_active + \
                    1.1 * (2.1 * self.input_power / self.weight**0.6766)

            # Base hazard rate.
            if self.insulation_class == 1:
                _constant = [0.0018, 329.0, 15.6]
            elif self.insulation_class == 2:
                _constant = [0.002, 352.0, 14.0]
            elif self.insulation_class == 3:
                _constant = [0.0018, 364.0, 8.7]
            elif self.insulation_class == 4:
                _constant = [0.002, 400.0, 10.0]
            elif (self.specification in [1, 2] and self.insulation_class == 5):
                _constant = [0.00125, 398.0, 3.8]
            elif (self.specification in [1, 2] and self.insulation_class == 6):
                _constant = [0.00159, 477.0, 8.4]

            self.base_hr = _constant[0] * \
                           exp(((self.hot_spot_temperature + 273.0) /
                                _constant[1])**_constant[2])

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return Inductor.calculate_part(self)
