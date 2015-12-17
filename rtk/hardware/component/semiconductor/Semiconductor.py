#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Semiconductor Package Semiconductor Module
#############################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.Semiconductor.py is part of the
#       RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import calculations as _calc
    import Configuration as _conf
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.calculations as _calc
    import rtk.Configuration as _conf
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


class Model(Component):
    """
    The Semiconductor data model contains the attributes and methods of a
    Semiconductor component.  The attributes of a Semiconductor are:

    :cvar category: default value: 2

    :ivar quality: default value: 0
    :ivar q_override: default value: 0.0
    :ivar base_hr: default value: 0.0
    :ivar piQ: default value: 0.0
    :ivar piE: default value: 0.0
    :ivar piT: default value: 0.0
    :ivar reason: default value: ""

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.
    """

    category = 2

    def __init__(self):
        """
        Initialize an Semiconductor data model instance.
        """

        super(Model, self).__init__()

        # Initialize public list attributes.
        self.lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Initialize public scalar attributes.
        self.quality = 0                    # Quality level.
        self.q_override = 0.0               # User-defined piQ.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.piT = 0.0                      # Temperature pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Sets the Semiconductor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.quality = int(values[116])
            self.q_override = float(values[96])
            self.base_hr = float(values[97])
            self.piQ = float(values[98])
            self.piE = float(values[99])
            self.piT = float(values[100])
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
        Retrieves the current values of the Semiconductor data model
        attributes.

        :return: (quality, q_override, base_hr, piQ, piE, piT, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.q_override, self.base_hr,
                             self.piQ, self.piE, self.piT, self.reason)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Semiconductor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab_count[self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ_count[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

        elif self.hazard_rate_type == 2:
            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ_stress[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

            # Set the environment pi factor for the model.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        self.hazard_rate_active = _calc.calculate_part(self.hazard_rate_model)
        self.hazard_rate_active = (self.hazard_rate_active + \
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
        self.hazard_rate_active = self.hazard_rate_active / _conf.FRMULT

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False
