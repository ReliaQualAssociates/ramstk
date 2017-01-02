#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.Capacitor.py is part of the RTK
#       Project
#
# All rights reserved.

"""
#################################
Hardware Package Capacitor Module
#################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.Component import Model as Component

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


class Model(Component):
    """
    The Capacitor data model contains the attributes and methods of a capacitor
    component.  The attributes of a Capacitor are:

    :cvar list lst_derate_criteria: default value: [[0.6, 0.6, 0.0],
                                                    [0.9, 0.9, 0.0]]
    :cvar int category: default value: 4

    :ivar int quality: default value: 0
    :ivar float q_override: default value: 0.0
    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0
    :ivar float acvapplied: default value: 0.0
    :ivar float capacitance: default value: 0.0
    :ivar float base_hr: default value: 0.0
    :ivar str reason: default value: ""
    :ivar float piQ: default value: 0.0
    :ivar float piE: default value: 0.0
    :ivar float piCV: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.
    """

    # Define class attributes.

    lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

    category = 4

    def __init__(self):
        """
        Method to initialize a Capacitor data model instance.
        """

        super(Model, self).__init__()

        # Define public scalar attributes.
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
        Method to set the Capacitor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:127])
        
        try:
            self.q_override = float(values[127])
            self.acvapplied = float(values[128])
            self.capacitance = float(values[129])
            self.base_hr = float(values[130])
            self.piQ = float(values[131])
            self.piE = float(values[132])
            self.piCV = float(values[133])
            self.quality = int(values[134])
            self.specification = int(values[135])
            self.spec_sheet = int(values[136])
            self.reason = str(values[137])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Capacitor data model
        attributes.

        :return: (q_override, acvapplied, capacitance, base_hr, piQ, piE, piCV,
                  quality, specification, spec_sheet, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.q_override, self.acvapplied, self.capacitance, 
                             self.base_hr, self.piQ, self.piE, self.piCV, 
                             self.quality, self.specification, self.spec_sheet, 
                             self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Capacitor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Quality correction factor.
        try:
            self.piQ = self._piQ[self.quality - 1]
        except AttributeError:
            # TODO: Handle attribute error.
            return True
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            # Base hazard rate.
            self.hazard_rate_model['lambdab'] = \
                self._lambdab_count[self.environment_active - 1]

        elif self.hazard_rate_type == 2:
            # Set the model's base hazard rate.
            self.base_hr = self.hazard_rate_model['lambdab']

            # Set the model's environmental correction factor.
            try:
                self.piE = self._piE[self.environment_active - 1]
            except AttributeError:
                # TODO: Handle attribute error.
                return True
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        _keys = self.hazard_rate_model.keys()
        _values = self.hazard_rate_model.values()

        for i in range(len(_keys)):
            vars()[_keys[i]] = _values[i]

        self.hazard_rate_active = eval(self.hazard_rate_model['equation'])
        self.hazard_rate_active = (self.hazard_rate_active +
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
        self.hazard_rate_active = self.hazard_rate_active / \
                                  Configuration.FRMULT

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = (self.operating_voltage + self.acvapplied) / \
                             self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False

    def _overstressed(self):
        """
        Method to determine whether the Capacitor is overstressed based on it's
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
            if self.operating_voltage > 0.60 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating voltage > 60% rated voltage.\n")
                _reason_num += 1
            if self.max_rated_temperature - self.temperature_active <= 10.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating temperature within 10.0C of "
                                u"maximum rated temperature.\n")
                _reason_num += 1
        else:
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating voltage > 90% rated voltage.\n")
                _reason_num += 1

        self.reason = _reason

        return False
