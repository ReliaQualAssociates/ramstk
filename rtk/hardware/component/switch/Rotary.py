#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Switch.Rotary Switch Package Rotary Module
#############################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Rotary.py is part of the RTK Project
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
    from hardware.component.switch.Switch import Model as \
        Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.switch.Switch import Model as \
        Switch

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


class Rotary(Switch):
    """
    The Rotary Switch data model contains the attributes and methods of a
    Rotary Switch component.  The attributes of a Rotary Switch are:

    :cvar int subcategory: the Switch subcategory.

    :ivar int construction: the MIL-HDBK-217FN2 construction input index.
    :ivar int load_type: the MIL-HDBK-217FN2 load type input index.
    :ivar int n_contacts: the MIL-HDBK-217FN2 number of active contacts input.
    :ivar float cycles_per_hour: the MIL-HDBK-217FN2 cycles per hour input.
    :ivar float piCYC: the MIL-HDBK-217FN2 cycles per hour factor.
    :ivar float piL:  the MIL-HDBK-217FN2 load type factor.

    Covers specification MIL-S-3786.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 14.3.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5,
                25.0, 67.0, 1200.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.33, 0.99, 5.9, 2.6, 9.5, 3.3, 5.9, 4.3, 7.2, 15.0,
                          0.16, 8.2, 22.0, 390.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 69

    def __init__(self):
        """
        Method to initialize a Rotary Switch data model instance.
        """

        super(Rotary, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.construction = 0
        self.load_type = 0
        self.n_contacts = 0                 # Number of active contacts
        self.cycles_per_hour = 0.0
        self.piCYC = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
        Method to set the Rotary Switch data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Switch.set_attributes(self, values)

        try:
            self.construction = int(values[117])
            self.load_type = int(values[118])
            self.n_contacts = int(values[119])
            self.cycles_per_hour = float(values[99])
            self.piCYC = float(values[100])
            self.piL = float(values[101])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Rotary Switch data model
        attributes.

        :return: (construction, load_type, n_contacts, cycles_per_hour, piCYC,
                  piL)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.construction, self.load_type,
                             self.n_contacts, self.cycles_per_hour, self.piCYC,
                             self.piL)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Rotary Switch data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 13.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piCYC * piL * piE'

            # Set the base hazard rate for the model.
            if self.quality == 1:       # MIL-SPEC
                if self.construction == 1:
                    self.base_hr = 0.0067 + 0.00003 * self.n_contacts
                else:
                    self.base_hr = 0.1 + 0.02 * self.n_contacts
            else:
                if self.construction == 2:
                    self.base_hr = 0.0067 + 0.00003 * self.n_contacts
                else:
                    self.base_hr = 0.1 + 0.06 * self.n_contacts
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the cycling factor for the model.
            if self.cycles_per_hour <= 1.0:
                self.piCYC = 1.0
            else:
                self.piCYC = float(self.cycles_per_hour)
            self.hazard_rate_model['piCYC'] = self.piCYC

            # Set the load stress factor for the model.
            _stress = self.operating_current / self.rated_current
            if self.load_type == 1:         # Resistive
                self.piL = exp((_stress / 0.8)**2.0)
            elif self.load_type == 2:       # Inductive
                self.piL = exp((_stress / 0.4)**2.0)
            elif self.load_type == 3:       # Lamp
                self.piL = exp((_stress / 0.2)**2.0)
            self.hazard_rate_model['piL'] = self.piL

        return Switch.calculate_part(self)
