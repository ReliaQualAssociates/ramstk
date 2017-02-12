#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.inductor.Inductor.py is part of the RTK
#       Project
#
# All rights reserved.

"""
###################################################
Hardware.Component.Inductor Package Inductor Module
###################################################
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
    The Inductor data model contains the attributes and methods of a inductor
    component.  The attributes of a Inductor are:

    :cvar int category: default value: 5

    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar str reason: default value: ""
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 11.
    """

    category = 5

    def __init__(self):
        """
        Method to initialize a Inductor data model instance.
        """

        super(Model, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.
        self.lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Define public scalar attributes.
        self.quality = 0                    # Quality level.
        self.specification = 0              # Index of governing specification.
        self.insulation_class = 0           # Index of insulation class.
        self.q_override = 0.0               # User-defined quality factor.
        self.base_hr = 0.0                  # Base hazard rate.
        self.reason = ""                    # Overstress reason.
        self.piQ = 1.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.hot_spot_temperature = 0.0     # Hot spot temperature.

    def set_attributes(self, values):
        """
        Method to set the Inductor data model attributes.

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
            self.base_hr = float(values[128])
            self.piQ = float(values[129])
            self.piE = float(values[130])
            self.hot_spot_temperature = float(values[131])
            self.quality = int(values[132])
            self.specification = int(values[133])
            self.insulation_class = int(values[134])
            self.reason = str(values[135])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Inductor data model
        attributes.

        :return: (q_override, base_hr, piQ, piE, quality, reason,
                  specification, insulation_class, hot_spot_temperature)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.q_override, self.base_hr, self.piQ, self.piE,
                             self.hot_spot_temperature,  self.quality, 
                             self.specification, self.insulation_class, self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Inductor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.hazard_rate_type == 1:
            # Base hazard rate.
            try:
                self.hazard_rate_model['lambdab'] = \
                    self._lambdab_count[self.environment_active - 1]
            except AttributeError:
                # TODO: Handle attribute error.
                return True

            # Quality correction factor.
            try:
                self.hazard_rate_model['piQ'] = self.piQ
            except AttributeError:
                # TODO: Handle attribute error.
                return True

        elif self.hazard_rate_type == 2:
            # Set the model's base hazard rate.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
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
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False

    def _overstressed(self):
        """
        Method to determine whether the Inductor is overstressed based on it's
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
            if self.operating_voltage > 0.5 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                    _(u". Operating voltage > 50% rated voltage.\n")
                _reason_num += 1
            if self.operating_current > 0.6 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                    _(u". Operating current > 60% rated current.\n")
                _reason_num += 1
            if self.max_rated_temperature - self.hot_spot_temperature < 15.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                    _(u". Operating temperature within 15.0C of maximum rated "
                      u"temperature.\n")
                _reason_num += 1
        else:
            if self.operating_voltage > 0.9 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                    _(u". Operating voltage > 90% rated voltage.\n")
                _reason_num += 1
            if self.operating_current > 0.9 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                    _(u". Operating current > 90% rated current.\n")
                _reason_num += 1

        self.reason = _reason


        return False
