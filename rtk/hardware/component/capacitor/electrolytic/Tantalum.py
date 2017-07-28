#!/usr/bin/env python
"""
#############################################
Hardware Package Electrolytic Tantalum Module
#############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.electrolytic.Tantalum.py is part of
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
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

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


class Solid(Capacitor):
    """
    The solid tantalum electrolytic capacitor data model contains the
    attributes and methods of a solid tantalum electrolytic capacitor.  The
    attributes of a solid tantalum electrolytic capacitor are:

    :ivar effective_resistance: default value: 0.0
    :ivar piSR: default value: 0.0

    Covers specification MIL-C-39003.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.12
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0, 12.0, 20.0, 24.0, 0.4, 11.0,
            29.0, 530.0]
    _piQ = [0.001, 0.01, 0.03, 0.03, 0.1, 0.3, 1.0, 1.5, 10.0]
    _lambdab_count = [0.0018, 0.0039, 0.016, 0.0097, 0.028, 0.0091, 0.011,
                      0.034, 0.057, 0.055, 0.00072, 0.022, 0.066, 1.0]
    lst_ref_temp = [398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 51                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a solid tantalum electrolytic capacitor data model instance.
        """

        super(Solid, self).__init__()

        # Initialize public scalar attributes.
        self.effective_resistance = 0.0
        self.piSR = 0.0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 398.0

    def set_attributes(self, values):
        """
        Sets the Solid Tantalum capacitor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Capacitor.set_attributes(self, values[:138])

        try:
            self.effective_resistance = float(values[138])
            self.piSR = float(values[139])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Solid Tantalum capacitor data model
        attributes.

        :return: (effective_resistance, piSR)
        :rtype: tuple
        """

        _values = Capacitor.get_attributes(self)

        _values = _values + (self.effective_resistance, self.piSR)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Solid Tantalum capacitor
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Consider re-writing calculate; current McCabe Complexity metrix = 10.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV * piSR'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.base_hr = 0.00375 * ((_stress / 0.4)**3.0 + 1.0) * \
                               exp(2.6 * ((self.temperature_active + 273) /
                                          self.reference_temperature)**9.0)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = (self.capacitance * 1000000.0)**0.12
            self.hazard_rate_model['piCV'] = self.piCV

            # Series resistance correction factor.
            _srcf = self.effective_resistance / self.operating_voltage
            if _srcf > 0.8:
                self.piSR = 0.066
            elif _srcf < 0.8 and _srcf >= 0.6:
                self.piSR = 0.10
            elif _srcf < 0.6 and _srcf >= 0.4:
                self.piSR = 0.13
            elif _srcf < 0.4 and _srcf >= 0.2:
                self.piSR = 0.20
            elif _srcf < 0.2 and _srcf >= 0.1:
                self.piSR = 0.27
            elif _srcf < 0.1 and _srcf >= 0.0:
                self.piSR = 0.33
            else:
                self.piSR = 0.33
            self.hazard_rate_model['piSR'] = self.piSR

        return Capacitor.calculate_part(self)


class NonSolid(Capacitor):
    """
    Fixed Non-Solid Tantalum Electrolytic Capacitor Component Class.

    Covers specifications MIL-C-3965 and MIL-C-39006.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.13
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----
    _piC = [0.3, 1.0, 2.0, 2.5, 3.0]
    _piE = [1.0, 2.0, 10.0, 6.0, 16.0, 4.0, 8.0, 14.0, 30.0, 23.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0]
    _lambdab_count = [0.0061, 0.013, 0.069, 0.039, 0.11, 0.031, 0.061, 0.13,
                      0.29, 0.18, 0.0030, 0.069, 0.26, 4.0]
    lst_ref_temp = [358.0, 398.0, 448.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 52                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize the Fixed Non-Solid Tantalum Electrolytic
        Capacitor Component Class.
        """

        super(NonSolid, self).__init__()

        # Initialize public scalar attributes.
        self.construction = 0
        self.piC = 0.0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            if self.max_rated_temperature == 125.0:
                self.reference_temperature = 398.0
            elif self.max_rated_temperature == 175.0:
                self.reference_temperature = 448.0
            else:
                self.reference_temperature = 358.0

    def set_attributes(self, values):
        """
        Method to set the Non-Solid Tantalum capacitor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Capacitor.set_attributes(self, values[:138])

        try:
            self.construction = int(values[138])
            self.piC = float(values[139])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Non-Solid Tantalum
        capacitor data model attributes.

        :return: (construciton, piCV)
        :rtype: tuple
        """

        _values = Capacitor.get_attributes(self)

        _values = _values + (self.construction, self.piC)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Non-Solid Tantalum
        capacitor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV * piC'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00165 * ((_stress / 0.4)**3 + 1) * \
                    exp(2.6 * ((self.temperature_active + 273) /
                               self.reference_temperature)**9)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.82 * (self.capacitance * 1000000.0)**0.066
            self.hazard_rate_model['piCV'] = self.piCV

            # Construction factor.
            self.piC = self._piC[self.construction - 1]
            self.hazard_rate_model['piC'] = self.piC

        return Capacitor.calculate_part(self)
