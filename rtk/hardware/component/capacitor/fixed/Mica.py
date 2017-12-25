#!/usr/bin/env python
"""
######################################################
Hardware.Component.Capacitor.Fixed Package Mica Module
######################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.fixed.Mica.py is part of the RTK
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

import gettext
import locale

try:
    import Configuration
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

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


class Button(Capacitor):
    """
    The Mica Button capacitor data model contains the attributes and methods of
    a mica button capacitor.  The attributes of a mica button capacitor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: the subcategory ID in the RTK common database.

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specifications MIL-C-11272 and MIL-C-23269.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.9
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [
        1.0, 2.0, 10.0, 5.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0, 34.0,
        610.0
    ]
    _piQ = [5.0, 15.0]
    _lambdab_count = [
        0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14, 0.47, 0.60, 0.48, 0.0091,
        0.25, 0.68, 11.0
    ]
    lst_ref_temp = [358.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 47

    def __init__(self):
        """
        Method to initialize a Mica Button capacitor data model instance.
        """

        super(Button, self).__init__()

        # Define public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:  # MIL-HDBK-217FN2
            self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Ceramic Chip capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.0053 * ((_stress / 0.4)**3 + 1) * \
                    exp(1.2 * ((self.temperature_active + 273) /
                               self.reference_temperature)**6.3)
            except (OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.31 * (self.capacitance * 1000000.0)**0.23
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)


class Mica(Capacitor):
    """
    The Mica capacitor data model contains the attributes and methods of
    a mica capacitor.  The attributes of a mica capacitor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: the subcategory ID in the RTK common database.

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specifications MIL-C-5 and MIL-C-39001.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.7
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [
        1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0, 34.0,
        610.0
    ]
    _piQ = [0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 6.0, 15.0]
    _lambdab_count = [
        0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068, 0.0095, 0.054, 0.069,
        0.031, 0.00025, 0.012, 0.046, 0.45
    ]
    lst_ref_temp = [343.0, 358.0, 398.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 46

    def __init__(self):
        """
        Method to initialize a Mica Button capacitor data model instance.
        """

        super(Mica, self).__init__()

        # Define public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:  # MIL-HDBK-217
            self.reference_temperature = 343.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Ceramic Chip capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00000000086 * ((_stress / 0.4)**3 + 1) * \
                    exp(16.0 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except (OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.45 * (self.capacitance * 1000000.0)**0.14
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)
