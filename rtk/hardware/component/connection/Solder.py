#!/usr/bin/env python
"""
###################################################
Hardware.Component.Connection Package Solder Module
###################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.Solder.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    from hardware.component.connection.Connection import Model as Connection
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.hardware.component.connection.Connection import Model as Connection

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'invalid literal for int() with base 10' in message[0]:
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class PTH(Connection):
    """
    The Plated Through Hole (PTH) connection data model contains the attributes
    and methods of a PTH connection component.  The attributes of a PTH
    connection are:

    :cvar subcategory: default value: 75

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 16.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
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
        Initialize a PTH connection data model instance.
        """

        super(PTH, self).__init__()

        # Initialize public scalar attributes.
        self.technology = 0
        self.n_wave_soldered = 0
        self.n_hand_soldered = 0
        self.n_circuit_planes = 0
        self.piQ = 0.0
        self.piC = 0.0

    def set_attributes(self, values):
        """
        Sets the PTH Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values)

        try:
            self.piQ = float(values[98])
            self.piC = float(values[100])
            self.technology = int(values[117])
            self.n_wave_soldered = int(values[118])
            self.n_hand_soldered = int(values[119])
            self.n_circuit_planes = int(values[120])
            # TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the PCB Connection data model
        attributes.

        :return: (technology, n_wave_soldered, n_hand_soldered,
                  n_circuit_planes, piC)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.technology, self.n_wave_soldered,
                             self.n_hand_soldered, self.n_circuit_planes,
                             self.piC)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the PTH Connection data model.

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

        return Connection.calculate(self)


class NonPTH(Connection):
    """
    The Non-Plated Through Hole (PTH) connection data model contains the
    attributes and methods of a Non-PTH connection component.  The attributes
    of a Non-PTH connection are:

    :cvar subcategory: default value: 76

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 17.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
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
        Initialize a Non-PTH connection data model instance.
        """

        super(NonPTH, self).__init__()

        # Initialize public scalar attributes.
        self.connection_type = 0
        self.piQ = 0.0

    def set_attributes(self, values):
        """
        Sets the Non-PTH Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values)

        try:
            self.piQ = float(values[98])
            self.connection_type = int(values[117])
            # TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the PCB Connection data model
        attributes.

        :return: (connection_type)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.connection_type, 0)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Non-PTH Connection data model.

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

        return Connection.calculate(self)
