#!/usr/bin/env python
"""
###################################################
Hardware.Component.Connection Package Solder Module
###################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.Solder.py is part of the RTK Project
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
    from hardware.component.connection.Connection import Model as Connection
except ImportError:                         # pragma: no cover
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
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class PTH(Connection):
    """
    The Plated Through Hole (PTH) connection data model contains the attributes
    and methods of a PTH connection component.  The attributes of a PTH
    connection are:

    :cvar int subcategory: the Connection subcategory.

    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar str reason: the reason(s) the Connection is overstressed.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 16.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piQ = [1.0, 2.0]
    _piE = [1.0, 2.0, 7.0, 5.0, 13.0, 5.0, 8.0, 16.0, 28.0, 19.0, 0.5, 10.0,
            27.0, 500.0]
    _lambdab_count = [0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 043, 0.85, 1.5, 1.0,
                      0.027, 0.53, 1.4, 27.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 75                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a PTH connection data model instance.
        """

        super(PTH, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.piC = 0.0
        self.technology = 0
        self.n_wave_soldered = 0
        self.n_hand_soldered = 0
        self.n_circuit_planes = 0

    def set_attributes(self, values):
        """
        Method to set the PTH Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values[:133])

        try:
            self.piC = float(values[133])
            self.technology = int(values[134])
            self.n_wave_soldered = int(values[135])
            self.n_hand_soldered = int(values[136])
            self.n_circuit_planes = int(values[137])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the PCB Connection data model
        attributes.

        :return: (piC, technology, n_wave_soldered, n_hand_soldered,
                  n_circuit_planes)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.piC, self.technology, self.n_wave_soldered,
                             self.n_hand_soldered, self.n_circuit_planes)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the PTH Connection data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * (N1 * piC + N2 * (piC + 13.0)) * piQ * piE'

            # Base hazard rate.
            if self.technology == 1:
                self.base_hr = 0.000041
            else:
                self.base_hr = 0.00026

            # Number of PTH factor.
            self.hazard_rate_model['N1'] = self.n_wave_soldered
            self.hazard_rate_model['N2'] = self.n_hand_soldered

            # Complexity factor.
            if self.n_circuit_planes > 2 and self.technology == 1:
                self.hazard_rate_model['piC'] = 0.65 * \
                    self.n_circuit_planes**0.63
            else:
                self.hazard_rate_model['piC'] = 1.0

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return Connection.calculate_part(self)


class NonPTH(Connection):
    """
    The Non-Plated Through Hole (PTH) connection data model contains the
    attributes and methods of a Non-PTH connection component.  The attributes
    of a Non-PTH connection are:

    :cvar int subcategory: the Connection subcategory.

    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar str reason: the reason(s) the Connection is overstressed.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 17.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lambdab = [0.00012, 0.00026, 0.0026, 0.000069, 0.00005, 0.00014]
    _piQ = [1.0, 1.0, 2.0, 20.0]
    _piE = [1.0, 2.0, 7.0, 4.0, 11.0, 4.0, 6.0, 6.0, 8.0, 16.0, 0.5, 9.0, 24.0,
            420.0]
    _lambdab_count = [[0.00012, 0.00024, 0.00084, 0.00048, 0.0013, 0.00048,
                       0.00072, 0.00072, 0.00096, 0.0019, 0.00005, 0.0011,
                       0.0029, 0.050],
                      [0.00026, 0.00052, 0.0018, 0.0010, 0.0029, 0.0010,
                       0.0016, 0.0016, 0.0021, 0.0042, 0.00013, 0.0023, 0.0062,
                       0.11],
                      [0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010, 0.016,
                       0.016, 0.021, 0.042, 0.0013, 0.023, 0.062, 1.1],
                      [0.000069, 0.000138, 0.000483, 0.000276, 0.000759,
                       0.000276, 0.000414, 0.000414, 0.000552, 0.001104,
                       0.000035, 0.000621, 0.001656, 0.02898],
                      [0.000050, 0.000100, 0.000350, 0.000200, 0.000550,
                       0.000200, 0.000300, 0.000300, 0.000400, 0.000800,
                       0.000025, 0.000450, 0.001200, 0.021000],
                      [0.00014, 0.00028, 0.00096, 0.00056, 0.0015, 0.00056,
                       0.00084, 0.00084, 0.0011, 0.0022, 0.00007, 0.0013,
                       0.0034, 0.059]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 76                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a Non-PTH connection data model instance.
        """

        super(NonPTH, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.connection_type = 0

    def set_attributes(self, values):
        """
        Method to set the Non-PTH Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values[:133])

        try:
            self.connection_type = int(values[133])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the PCB Connection data model
        attributes.

        :return: (connection_type)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.connection_type, )

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Non-PTH Connection data
        model.


        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        # Quality factor.
        if self.connection_type == 3:
            self.piQ = self._piQ[self.quality - 1]
        else:
            self.piQ = 1.0
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            self._lambdab_count = self._lambdab_count[self.connection_type - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            self.base_hr = self._lambdab[self.connection_type - 1]

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return Connection.calculate_part(self)
