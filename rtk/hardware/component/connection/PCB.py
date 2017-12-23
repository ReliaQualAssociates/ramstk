#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.PCB.py is part of the RTK
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
################################################
Hardware.Component.Connection Package PCB Module
################################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.connection.Connection import Model as Connection
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.connection.Connection import Model as \
                                                             Connection

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


class PCB(Connection):
    """
    The PCB connection data model contains the attributes and methods of a PCB
    connection component.  The attributes of a PCB connection are:

    :cvar int subcategory: the Connection subcategory.

    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar str reason: the reason(s) the Connection is overstressed.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 15.2.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _gauge = [2.100, 0.989, 0.640]
    _piQ = [1.0, 2.0]
    _piE = [[
        1.0, 3.0, 8.0, 5.0, 13.0, 6.0, 11.0, 6.0, 11.0, 19.0, 0.5, 10.0, 27.0,
        490.0
    ], [
        2.0, 7.0, 17.0, 10.0, 26.0, 14.0, 22.0, 14.0, 22.0, 37.0, 0.8, 20.0,
        54.0, 970.0
    ]]
    _lambdab_count = [
        0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085, 0.16, 0.19,
        0.0027, 0.078, 0.21, 3.4
    ]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 73  # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a PCB connection data model instance.
        """

        super(PCB, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.amps_per_contact = 0.0
        self.mate_unmate_cycles = 0.0
        self.piK = 0.0
        self.piP = 0.0
        self.contact_temperature = 0.0
        self.n_active_contacts = 0
        self.contact_gauge = 26

    def set_attributes(self, values):
        """
        Method to set the PCB Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values[:133])

        try:
            self.amps_per_contact = float(values[133])
            self.mate_unmate_cycles = float(values[134])
            self.piK = float(values[135])
            self.piP = float(values[136])
            self.contact_temperature = float(values[137])
            self.n_active_contacts = int(values[138])
            self.contact_gauge = int(values[139])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except (TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return (_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the PCB Connection data model
        attributes.

        :return: (amps_per_contact, mate_unmate_cycles, piK, piP, 
                  contact_temperature, n_active_contacts, contact_gauge)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.amps_per_contact, self.mate_unmate_cycles,
                             self.piK, self.piP, self.contact_temperature,
                             self.n_active_contacts, self.contact_gauge)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the PCB Connection data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor calculate_part; current McCabe Complexity metric = 13.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Quality factor.
            self.piQ = self._piQ[self.quality - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piE * piK * piP'

            # Calculate temperature rise.
            if self.contact_gauge == 26:
                self.temperature_rise = 2.1 * self.amps_per_contact**1.85
            elif self.contact_gauge == 22:
                self.temperature_rise = 0.989 * self.amps_per_contact**1.85
            elif self.contact_gauge == 20:
                self.temperature_rise = 0.64 * self.amps_per_contact**1.85

            To = self.temperature_rise + self.temperature_active

            self.base_hr = 0.216 * \
                           exp((-2073.6 / (To + 273.0)) +
                               (((To + 273.0) / 423.0)**4.66))
            self.contact_temperature = To

            # Mate/Unmate cycles correction factor.
            if self.mate_unmate_cycles <= 0.05:
                self.piK = 1.0
            elif self.mate_unmate_cycles > 0.05 and \
                 self.mate_unmate_cycles <= 0.5:
                self.piK = 1.5
            elif self.mate_unmate_cycles > 0.5 and \
                 self.mate_unmate_cycles <= 5:
                self.piK = 2.0
            elif self.mate_unmate_cycles > 5 and \
                 self.mate_unmate_cycles <= 50:
                self.piK = 3.0
            else:
                self.piK = 4.0

            self.hazard_rate_model['piK'] = self.piK

            # Active pins correction factor.
            if self.n_active_contacts >= 2:
                self.piP = exp(((self.n_active_contacts - 1) / 10.0)**0.51064)
            else:
                self.piP = 0.0
            self.hazard_rate_model['piP'] = self.piP

            # Environmental correction factor.
            self.piE = self._piE[self.quality - 1][self.environment_active - 1]

        return Connection.calculate_part(self)
