#!/usr/bin/env python
"""
################################################
Hardware.Component.Connection Package PCB Module
################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.PCB.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import configuration as _conf
    from hardware.component.connection.Connection import Model as Connection
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
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


class PCB(Connection):
    """
    The PCB connection data model contains the attributes and methods of a PCB
    connection component.  The attributes of a PCB connection are:

    :cvar subcategory: default value: 73

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 15.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _gauge = [2.100, 0.989, 0.640]
    _piQ = [1.0, 2.0]
    _piE = [[1.0, 3.0, 8.0, 5.0, 13.0, 6.0, 11.0, 6.0, 11.0, 19.0, 0.5, 10.0,
             27.0, 490.0],
            [2.0, 7.0, 17.0, 10.0, 26.0, 14.0, 22.0, 14.0, 22.0, 37.0, 0.8,
             20.0, 54.0, 970.0]]
    _lambdab_count = [0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085,
                      0.16, 0.19, 0.0027, 0.078, 0.21, 3.4]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 73                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a PCB connection data model instance.
        """

        super(PCB, self).__init__()

        # Initialize public scalar attributes.
        self.n_active_contacts = 0
        self.contact_gauge = 26
        self.amps_per_contact = 0.0
        self.mate_unmate_cycles = 0.0
        self.piK = 0.0
        self.piP = 0.0
        self.contact_temperature = 0.0

    def set_attributes(self, values):
        """
        Sets the PCB Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values)

        try:
            self.amps_per_contact = float(values[100])
            self.mate_unmate_cycles = float(values[101])
            self.piK = float(values[102])
            self.piP = float(values[103])
            self.contact_temperature = float(values[104])
            self.n_active_contacts = int(values[117])
            self.contact_gauge = int(values[118])
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

        :return: (n_active_contacts, contact_gauge, mate_unmate_cycles,
                  amps_per_contact, piK, piP, contact_temperature)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.n_active_contacts, self.contact_gauge,
                             self.amps_per_contact, self.mate_unmate_cycles,
                             self.piK, self.piP, self.contact_temperature)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the PCB Connection data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

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
                           exp((-2073.6 / (To + 273.0)) + \
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
                self.piK = 4.0                                      # pragma: no cover
            self.hazard_rate_model['piK'] = self.piK

            # Active pins correction factor.
            if self.n_active_contacts >= 2:
                self.piP = exp(((self.n_active_contacts - 1) / 10.0)**0.51064)
            else:
                self.piP = 0.0
            self.hazard_rate_model['piP'] = self.piP

            # Environmental correction factor.
            self.piE = self._piE[self.quality - 1][self.environment_active - 1]

        return Connection.calculate(self)
