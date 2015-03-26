#!/usr/bin/env python
"""
####################################################
Hardware.Component.Miscellaneous Package Fuse Module
####################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.miscellaneous.Fuse.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import calculations as _calc
    import configuration as _conf
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    from rtk.hardware.component.Component import Model as Component

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
    elif 'invalid literal for int() with base 10' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        print message
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Fuse(Component):
    """
    The Fuse data model contains the attributes and methods of a Fuse
    component.  The attributes of an Fuse are:

    :cvar category: default value: 10
    :cvar subcategory: default value: 82

    :ivar base_hr: default value: 0.0
    :ivar piE: default value: 0.0
    :ivar reason: default value: ""

    Hazard Rate Models:
        # MIL-HDBK-217F, section 22.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 8.0, 5.0, 11.0, 9.0, 12.0, 15.0, 18.0, 16.0, 0.9,
                10.0, 21.0, 230.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    category = 10
    subcategory = 82

    def __init__(self):
        """
        Initialize an Fuse data model instance.
        """

        super(Fuse, self).__init__()

        # Initialize public scalar attributes.
        self.base_hr = 0.01                 # Base hazard rate.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Sets the Fuse data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.piE = float(values[96])
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
        Retrieves the current values of the Fuse data model
        attributes.

        :return: (base_hr, piE, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.base_hr, self.piE, self.reason)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Fuse data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            self.hazard_rate_model['lambdab'] = self.base_hr

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piE'

            # Set the model's base hazard rate.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        self.hazard_rate_active = _calc.calculate_part(self.hazard_rate_model)
        self.hazard_rate_active = self.hazard_rate_active * \
            self.quantity / 1000000.0

        # Calculate the component dormant hazard rate.
        self.hazard_rate_dormant = _calc.dormant_hazard_rate(
            self.category_id, self.subcategory_id, self.environment_active,
            self.environment_dormant, self.hazard_rate_active)

        # Calculate the component logistics hazard rate.
        self.hazard_rate_logistics = self.hazard_rate_active + \
            self.hazard_rate_dormant + self.hazard_rate_software

        # Calculate the component logistics MTBF.
        try:
            self.mtbf_logistics = 1.0 / self.hazard_rate_logistics
        except ZeroDivisionError:           # pragma: no cover
            self.mtbf_logistics = 0.0

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage

        return False
