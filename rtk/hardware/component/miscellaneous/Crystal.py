#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.miscellaneous.Crystal.py is part of the RTK
#       Project
#
# All rights reserved.

"""
#######################################################
Hardware.Component.Miscellaneous Package Crystal Module
#######################################################
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


class Crystal(Component):
    """
    The Crystal data model contains the attributes and methods of a Crystal
    component.  The attributes of an Crystal are:

    :cvar int category: the Component category.

    :ivar int quality: the MIL-HDBK-217FN2 quality list index.
    :ivar float q_override: the user-defined quality factor.
    :ivar float frequency: the operating frequency of the Crystal.
    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar float piQ: the MIL-HDBK-217FN2 quality factor.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar str reason: the reason(s) the Crystal is overstressed.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 19.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 10.0, 6.0, 16.0, 12.0, 17.0, 22.0, 28.0, 23.0, 0.5,
                13.0, 32.0, 500.0]
    _lst_piQ = [1.0, 2.1]
    _lst_lambdab_count = [0.032, 0.096, 0.32, 0.19, 0.51, 0.38, 0.54, 0.70,
                          0.90, 0.74, 0.016, 0.42, 1.0, 16.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    category = 6
    subcategory = 1

    def __init__(self):
        """
        Method to initialize a Crystal data model instance.
        """

        super(Crystal, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.quality = 0                    # Quality index.
        self.q_override = 0.0               # User-defined quality factor.
        self.frequency = 0.0                # Operating frquency (MHz).
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Method to set the Crystal data model attributes.

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
            self.frequency = float(values[128])
            self.base_hr = float(values[129])
            self.piQ = float(values[130])
            self.piE = float(values[131])
            self.quality = int(values[132])
            self.reason = str(values[133])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Crystal data model
        attributes.

        :return: (quality, q_override, base_hr, piQ, piE, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.q_override, self.frequency, self.base_hr, self.piQ, 
                             self.piE, self.quality, self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Crystal data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            self.base_hr = self._lst_lambdab_count[self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Set the model's base hazard rate.
            self.base_hr = 0.013 * self.frequency**0.23
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

            # Set the model's quality correction factor.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

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

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False
