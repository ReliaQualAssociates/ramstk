#!/usr/bin/env python
"""
###################################################
Hardware.Component.Resistor Package Resistor Module
###################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.Resistor.py is part of the RTK Project
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
    The Resistor data model contains the attributes and methods of a Resistor
    component.  The attributes of a Resistor are:

    :cvar int category: default value: 3

    :ivar int quality: the MIL-HDBK-217FN2 quality level.
    :ivar float q_override: the user-supplied quality factor.
    :ivar float resistance: the resistance (in ohms) of the resistor.
    :ivar float base_hr: the MIL-HDBK-217FN2 base hazard rate.
    :ivar float piQ: the MIL-HDBK-217FN2 quality factor.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar float piR: the MIL-HDBK-217FN2 resistance factor.
    :ivar str reason: default value: ""

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.
    """

    category = 3

    def __init__(self):
        """
        Method to initialize an Resistor data model instance.
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
        self.q_override = 0.0               # User-defined piQ.
        self.resistance = 0.0               # Nominal resistance value.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.piR = 0.0                      # Resistance range pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Method to set the Resistor data model attributes.

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
            self.resistance = float(values[97])
            self.base_hr = float(values[98])
            self.piQ = float(values[99])
            self.piE = float(values[100])
            self.piR = float(values[101])
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
        Method to retrieve the current values of the Resistor data model
        attributes.

        :return: (quality, q_override, resistance, base_hr, piQ, piE, piR,
                  reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.q_override, self.resistance,
                             self.base_hr, self.piQ, self.piE, self.piR,
                             self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Resistor data model.

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
        _keys = self.hazard_rate_model.keys()
        _values = self.hazard_rate_model.values()

        for i in range(len(_keys)):
            vars()[_keys[i]] = _values[i]

        self.hazard_rate_active = eval(self.hazard_rate_model['equation'])
        self.hazard_rate_active = (self.hazard_rate_active +
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
        self.hazard_rate_active = self.hazard_rate_active / Configuration.FRMULT

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False

    def _overstressed(self):
        """
        Method to determine whether the Resistor is overstressed based on it's
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
            if self.operating_power > 0.5 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              ". Operating power > 50% rated power.\n"
                _reason_num += 1
        else:
            if self.operating_power > 0.8 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                              ". Operating power > 80% rated power.\n"
                _reason_num += 1

        self.reason = _reason

        return False
