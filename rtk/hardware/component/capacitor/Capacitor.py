#!/usr/bin/env python
"""
#################################
Capacitor Sub-Package Data Module
#################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.Capacitor.py is part of the RTK Project
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
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(Component):
    """
    The Capacitor data model contains the attributes and methods of a capacitor
    component.  The attributes of a Capacitor are:

    :ivar quality: default value: 0
    :ivar q_override: default value: 0.0
    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0
    :ivar acvapplied: default value: 0.0
    :ivar capacitance: default value: 0.0
    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piQ: default value: 0.0
    :ivar piE: default value: 0.0
    :ivar piCV: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.
    """

    category = 4

    def __init__(self):
        """
        Initialize a Capacitor data model instance.
        """

        super(Model, self).__init__()

        # Initialize public scalar attributes.
        self.quality = 0                    # Quality category.
        self.q_override = 0.0               # Quality override.
        self.specification = 0              # Specification.
        self.spec_sheet = 0                 # Specification sheet.
        self.acvapplied = 0.0               # Applied AC voltage.
        self.capacitance = 0.0              # Capacitance.
        self.base_hr = 0.0                  # Base hazard rate.
        self.reason = ""                    # Overstress reason.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.piCV = 0.0                     # Capacitance correction factor.

    def set_attributes(self, values):
        """
        Sets the Capacitor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:92])

        try:
            self.quality = int(values[92])
            self.q_override = float(values[93])
            self.specification = int(values[94])
            self.spec_sheet = int(values[95])
            self.acvapplied = float(values[96])
            self.capacitance = float(values[97])
            self.base_hr = float(values[98])
            self.reason = str(values[99])
            self.piQ = float(values[100])
            self.piE = float(values[101])
            self.piCV = float(values[102])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Capacitor data model attributes.

        :return: (quality, q_override, specification, spec_sheet,
                  acvapplied, capacitance, base_hr, reason, piQ, piE, piCV)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.q_override, self.specification,
                             self.spec_sheet, self.acvapplied,
                             self.capacitance, self.base_hr, self.reason,
                             self.piQ, self.piE, self.piCV)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Capacitor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp, sqrt

        # Quality correction factor.
        try:
            self.piQ = self._piQ[self.quality - 1]
        except AttributeError:
            # TODO: Handle attribute error.
            return True
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            # Base hazard rate.
            self.hazard_rate_model['lambdab'] = self._lambdab_count[self.environment_active - 1]

        elif self.hazard_rate_type == 2:
            # Environmental correction factor.
            try:
                self.piE = self._piE[self.environment_active - 1]
            except AttributeError:
                # TODO: Handle attribute error.
                return True
            self.hazard_rate_model['piE'] = self.piE

            # Capacitance correction factor.
            self.hazard_rate_model['piCV'] = 0.34 * self.capacitance**0.186

        # Calculate component active hazard rate.
        self.hazard_rate_active = _calc.calculate_part(self.hazard_rate_model)
        self.hazard_rate_active = self.hazard_rate_active * \
                                  self.quantity / 1000000.0

        # Calculate the component dormant hazard rate.
        self.hazard_rate_dormant = _calc.dormant_hazard_rate(
            self.category_id, self.subcategory_id, self.environment_active,
            self.environment_dormant, self.hazard_rate_active)

        # Calculate the component predicted hazard rate.
        self.hazard_rate_logistics = self.hazard_rate_active + \
                                     self.hazard_rate_dormant + \
                                     self.hazard_rate_software

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage + self.acvapplied / \
                             self.rated_voltage

        return False

    def _overstressed(self):
        """
        Determines whether the Capacitor is overstressed based on it's rated
        values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason = ""
        _reason_num = 1
        _harsh = True

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if _harsh:
            if self.operating_voltage > 0.60 * self.rated_voltage:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                              _(u". Operating voltage > 60% rated voltage.\n")
                _reason_num += 1
            if self.max_rated_temperature - self.temperature_active <= 10.0:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                              _(u". Operating temperature within 10.0C of "
                                u"maximum rated temperature.\n")
                _reason_num += 1
        else:
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                              _(u". Operating voltage > 90% rated voltage.\n")
                _reason_num += 1

        return False
