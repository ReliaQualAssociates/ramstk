#!/usr/bin/env python
"""
###################################################
Hardware.Component.Relay Package Solid State Module
###################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.relay.SolidState.py is part of the RTK Project
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
    from hardware.component.relay.Relay import Model as Relay
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    from rtk.hardware.component.relay.Relay import Model as Relay

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


class SolidState(Relay):
    """
    The SolidState Relay data model contains the attributes and methods of a
    SolidState Relay component.  The attributes of a SolidState Relay are:

    :cvar int subcategory: default value: 65

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 13.2.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piQ = [1.0, 4.0]
    _lst_piE = [
        1.0, 3.0, 12.0, 6.0, 17.0, 12.0, 19.0, 21.0, 32.0, 23.0, 0.4, 12.0,
        33.0, 590.0
    ]
    _lst_lambdab_count = [[
        0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2, 0.16, 4.8, 13.0,
        240.0
    ], [
        0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0, 12.0, 0.20, 5.0, 17.0,
        300.0
    ]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 65

    def __init__(self):
        """
        Method to initialize an Solid State Relay data model instance.
        """

        super(SolidState, self).__init__()

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Mechanical Relay data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab_count[self.construction - 1][
                self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Set the base hazard rate for the model.
            if self.construction == 1:
                self.base_hr = 0.4
            else:
                self.base_hr = 0.5
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality factor for the model.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

            # Set the environment factor for the model.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        return Relay.calculate_part(self)
