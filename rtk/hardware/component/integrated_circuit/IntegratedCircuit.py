#!/usr/bin/env python
"""
#######################################################################
Hardware.Component.IntegratedCircuit Package Integrated Circtuit Module
#######################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.IntegratedCircuit.py is part
#       of the RTK Project
#
# All rights reserved.

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
    The Integrated Circuit data model contains the attributes and methods of an
    integrated Circuit component.  The attributes of an Integrated Circuit are:

    :cvar category: default value: 5

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.
    """

    category = 1

    def __init__(self):
        """
        Method to initialize an Integrated Circuit data model instance.
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
        self.q_override = 0.0               # User-defined quality factor.
        self.base_hr = 0.0                  # Base hazard rate.
        self.reason = ""                    # Overstress reason.
        self.piQ = 1.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.piT = 0.0                      # Temperature pi factor.

    def set_attributes(self, values):
        """
        Method to set the Integrated Circuit data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.q_override = float(values[96])
            self.base_hr = float(values[97])
            self.piQ = float(values[98])
            self.piE = float(values[99])
            self.piT = float(values[100])
            self.quality = int(values[116])
            self.reason = ''               # FIXME: See bug 181.
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Integrated Circuit data
        model attributes.

        :return: (q_override, base_hr, piQ, piE, quality, reason,
                  specification, insulation_class, hot_spot_temperature)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.q_override, self.base_hr, self.piQ, self.piE,
                             self.piT, self.quality, self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Integrated Circuit data
        model.

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
        Method to determine whether the Integrated Circuit is overstressed
        based on it's rated values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor _overstressed; current McCabe Complexity metric = 11.
        _reason_num = 1
        _reason = ''
        _harsh = True
# TODO: Set max junction temperature based on device type.
        # if self.subcategory == 9:           # GaAs
        #     _max_junction_temp = 135.0
        # else:
        _max_junction_temp = 125.0

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if _harsh:
            if self.operating_voltage > 1.05 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating voltage > 105% rated voltage.\n")
                _reason_num += 1
            if self.operating_voltage < 0.95 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating voltage < 95% rated voltage.\n")
                _reason_num += 1
            if self.operating_current > 0.80 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating current > 80% rated current.\n")
                _reason_num += 1
            if self.junction_temperature > _max_junction_temp:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Junction temperature > %fC.\n").format(
                                  _max_junction_temp)
                _reason_num += 1
        else:
            if self.operating_voltage > 1.05 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating voltage > 105% rated voltage.\n")
                _reason_num += 1
            if self.operating_voltage < 0.95 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating voltage < 95% rated voltage.\n")
                _reason_num += 1
            if self.operating_current > 0.90 * self.rated_current:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              _(u". Operating current > 90% rated current.\n")
                _reason_num += 1

        self.reason = _reason

        return False
