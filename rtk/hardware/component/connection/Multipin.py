#!/usr/bin/env python
"""
#####################################################
Hardware.Component.Connection Package Multipin Module
#####################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.Multipin.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    import Utilities as _util
    from hardware.component.connection.Connection import Model as Connection
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    from rtk.hardware.component.connection.Connection import Model as Connection

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Multipin(Connection):
    """
    The Multipin connection data model contains the attributes and methods of a
    multipin connection component.  The attributes of a multipin connection
    are:

    :cvar subcategory: default value: 8

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 15.1
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _quality = [1.0, 2.0]
    _piE = [[1.0, 1.0, 8.0, 5.0, 13.0, 3.0, 5.0, 8.0, 12.0, 19.0, 0.5, 10.0,
             27.0, 490.0],
            [2.0, 5.0, 21.0, 10.0, 27.0, 12.0, 18.0, 17.0, 25.0, 37.0, 0.8,
             20.0, 54.0, 970.0]]
    _piK = [1.0, 1.5, 2.0, 3.0, 4.0]
    _lambdab_count = [[0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23,
                       0.34, 0.37, 0.0054, 0.16, 0.42, 6.8],
                      [0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23,
                       0.34, 0.37, 0.0054, 0.16, 0.42, 6.8]]
                      #[0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23,
                      # 0.34, 0.37, 0.0054, 0.16, 0.42, 6.8],
                      #[0.012, 0.015, 0.13, 0.075, 0.21, 0.050, 0.10, 0.22,
                      # 0.32, 0.38, 0.0061, 0.16, 0.54, 7.3],
                      #[0.012, 0.015, 0.13, 0.075, 0.21, 0.050, 0.10, 0.22,
                      # 0.32, 0.38, 0.0061, 0.16, 0.54, 7.3]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 72                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a Multipin connection data model instance.
        """

        super(Multipin, self).__init__()

        # Initialize public scalar attributes.
        self.insert = 0                     # Insert material.
        self.specification = 0
        self.configuration = 0
        self.contact_gauge = 22
        self.n_active_contacts = 0
        self.piK = 0.0
        self.piP = 0.0
        self.amps_per_contact = 0.0
        self.mate_unmate_cycles = 0.0
        self.contact_temperature = 30.0

    def set_attributes(self, values):
        """
        Sets the Multi-Pin Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values)

        try:
            self.piK = float(values[100])
            self.piP = float(values[101])
            self.amps_per_contact = float(values[102])
            self.mate_unmate_cycles = float(values[103])
            self.contact_temperature = float(values[104])
            self.insert = int(values[117])
            self.specification = int(values[118])
            self.configuration = int(values[119])
            self.contact_gauge = int(values[120])
            self.n_active_contacts = int(values[121])
            # TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Multi-Pin Connection data model
        attributes.

        :return: (insert, specification, configuration, contact_gauge,
                  mate_unmate_cycles, n_active_contacts,
                  contact_temperature, amps_per_contact, piK, piP)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.insert, self.specification,
                             self.configuration, self.contact_gauge,
                             self.n_active_contacts, self.piK, self.piP,
                             self.amps_per_contact, self.mate_unmate_cycles,
                             self.contact_temperature)

        return _values

    def calculate(self):                    # pylint: disable=R0912
        """
        Calculates the hazard rate for the Multi-Pin Connection data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Base hazard rate.
            if self.configuration == 4:
                self._lambdab_count = self._lambdab_count[1]
            else:
                self._lambdab_count = self._lambdab_count[0]

            # Quality factor.
            self.piQ = self._quality[self.quality - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piE * piK * piP'

            # Calculate temperature rise.
            if self.contact_gauge == 22:
                self.temperature_rise = 0.989 * self.amps_per_contact**1.85
            elif self.contact_gauge == 20:
                self.temperature_rise = 0.64 * self.amps_per_contact**1.85
            elif self.contact_gauge == 16:
                self.temperature_rise = 0.274 * self.amps_per_contact**1.85
            elif self.contact_gauge == 12:
                self.temperature_rise = 0.1 * self.amps_per_contact**1.85

            To = self.temperature_rise + self.temperature_active

            # Base hazard rate.
            if self.configuration == 1:     # Rack and panel
                if self.specification in [1, 2]:
                    _constant = [0.431, -2073.6, 423.0, 4.66]
                else:
                    if self.insert in [1, 2, 3]:
                        _constant = [0.020, -1592.0, 473.0, 5.36]
                    else:
                        _constant = [0.431, -2073.6, 423.0, 4.66]   # pragma: no cover
            elif self.configuration == 2:   # Circular
                if self.specification == 1:
                    if self.insert in [1, 2, 3, 4, 5, 6]:
                        _constant = [0.431, -2073.6, 423.0, 4.66]   # pragma: no cover
                    else:
                        _constant = [0.770, -1528.8, 358.0, 4.72]
                elif self.specification == 2:                       # pragma: no cover
                    if self.insert in [1, 2, 3]:
                        _constant = [0.020, -1592.0, 473.0, 5.36]
                    elif self.insert in [4, 5, 6, 7, 8, 9]:
                        _constant = [0.431, -2073.6, 423.0, 4.66]
                    else:
                        _constant = [0.770, -1528.8, 358.0, 4.72]
                elif self.specification in [3, 4]:                  # pragma: no cover
                    if self.insert in [1, 2, 3]:
                        _constant = [0.020, -1592.0, 473.0, 5.36]
                    else:
                        _constant = [0.431, -2073.6, 423.0, 4.66]
                else:
                    _constant = [0.431, -2073.6, 423.0, 4.66]       # pragma: no cover
            elif self.configuration == 3:   # Power
                if self.specification in [1, 2, 3, 4, 5, 6, 7]:
                    _constant = [0.190, -1298.0, 373.0, 4.25]
                else:
                    if self.insert in [1, 2, 3, 4, 5, 6]:           # pragma: no cover
                        _constant = [0.431, -2073.6, 423.0, 4.66]
                    else:
                        _constant = [0.190, -1298.0, 373.0, 4.25]   # pragma: no cover
            else:                            # Coaxial/triaxial
                if self.insert in [1, 2, 3, 4, 5, 6]:               # pragma: no cover
                    _constant = [0.431, -2073.6, 423.0, 4.66]
                else:
                    _constant = [0.190, -1298.0, 373.0, 4.25]       # pragma: no cover

            self.base_hr = _constant[0] * \
                           exp((_constant[1] / (To + 273.0)) +
                               (((To + 273.0) / _constant[2])**_constant[3]))

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
