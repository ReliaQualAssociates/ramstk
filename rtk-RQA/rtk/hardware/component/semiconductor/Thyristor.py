#!/usr/bin/env python
"""
#########################################################
Hardware.Component.Semiconductor Package Thyristor Module
#########################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.Thyristor.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor

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


class Thyristor(Semiconductor):
    """
    The Thyristor data model contains the attributes and methods of a
    Thyristor component.  The attributes of a Thyristor
    are:

    :cvar subcategory: default value: 21

    :ivar piR: default value: 0.0
    :ivar piS: default value: 0.0

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.10.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                14.0, 32.0, 320.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_lambdab_count = [0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14,
                          0.14, 0.31, 0.12, 0.0012, 0.053, 0.16, 1.1]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 21

    def __init__(self):
        """
        Method to initialize a Thyristor data model instance.
        """

        super(Thyristor, self).__init__()

        # Initialize public scalar attributes.
        self.base_hr = 0.0022               # Base hazard rate.
        self.piR = 0.0                      # Current rating pi factor.
        self.piS = 0.0                      # Voltage stress pi factor.

    def set_attributes(self, values):
        """
        Method to set the Thyristor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.piR = float(values[101])
            self.piS = float(values[102])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Thyristor data model
        attributes.

        :return: (piR, piS)
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.piR, self.piS)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Thyristor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piR * piS * piQ * piE'

            # Set the base hazard rate for the model.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-3082.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Set the current rating factor for the model.
            self.piR = self.rated_current**0.40
            self.hazard_rate_model['piR'] = self.piR

            # Set the voltage stress factor for the model.
            _stress = self.operating_voltage / self.rated_voltage
            if _stress <= 0.3:              # pragma: no cover
                self.piS = 0.1
            else:
                self.piS = _stress**1.9
            self.hazard_rate_model['piS'] = self.piS

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the Thyristor is overstressed based on it's
        rated values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
        _reason = ''
        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if _harsh:
            if self.operating_current > 0.70 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating current > 70% rated current.\n"
                _reason_num += 1
            if self.operating_voltage > 0.70 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 70% rated voltage.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
                _reason_num += 1
        else:
            if self.operating_current > 0.90 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating current > 90% rated current.\n"
                _reason_num += 1
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 90% rated voltage.\n"
                _reason_num += 1

        self.reason = _reason


        return False
