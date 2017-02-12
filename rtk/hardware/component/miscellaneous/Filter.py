#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.miscellaneous.Filter.py is part of the RTK
#       Project
#
# All rights reserved.

"""
######################################################
Hardware.Component.Miscellaneous Package Filter Module
######################################################
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


class Filter(Component):
    """
    The Filter data model contains the attributes and methods of a Filter
    component.  The attributes of an Filter are:

    :cvar int category: the Component category.
    :cvar int subcategory: the Component subcategory.

    :ivar int quality: the MIL-HDBK-217FN2 quality list index.
    :ivar int specification: the specification list index.
    :ivar int style: the style list index.
    :ivar float q_override: the user-defined quality factor.
    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar float piQ: the MIL-HDBK-217FN2 quality factor.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar str reason: the reason(s) the Filter is overstressed.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 21.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 6.0, 4.0, 9.0, 7.0, 9.0, 11.0, 13.0, 11.0, 0.8, 7.0,
                15.0, 120.0]
    _lst_piQ = [1.0, 2.9]
    _lst_lambdab = [[0.022, 0.12], [0.12, 0.27]]
    _lst_lambdab_count = [[0.022, 0.044, 0.13, 0.088, 0.20, 0.15, 0.20, 0.24,
                           0.29, 0.24, 0.018, 0.15, 0.33, 2.6],
                          [0.12, 0.24, 0.72, 0.48, 1.1, 0.84, 1.1, 1.3, 1.6,
                           1.3, 0.096, 0.84, 1.8, 1.4],
                          [0.27, 0.54, 1.6, 1.1, 2.4, 1.9, 2.4, 3.0, 3.5, 3.0,
                           0.22, 1.9, 4.1, 32.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    category = 6
    subcategory = 2

    def __init__(self):
        """
        Method to initialize an Filter data model instance.
        """

        super(Filter, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.quality = 0                    # Quality index.
        self.specification = 0              # Governing specification.
        self.style = 0                      # Filter style.
        self.q_override = 0.0               # User-defined quality factor.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
        Method to set the Filter data model attributes.

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
            self.quality = int(values[131])
            self.specification = int(values[132])
            self.style = int(values[133])
            self.reason = str(values[134])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Filter data model
        attributes.

        :return: (quality, specification, style, q_override, base_hr, piQ, piE,
                  reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.q_override, self.base_hr, self.piQ, self.piE,
                             self.quality, self.specification, self.style, 
                             self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Filter data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        # Set the model's quality correction factor.
        self.piQ = self._lst_piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            self.base_hr = self._lst_lambdab_count[self.style - 1][self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Set the model's base hazard rate.
            self.base_hr = self._lst_lambdab[self.specification - 1][self.style - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
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
        self.hazard_rate_active = self.hazard_rate_active / \
                                  Configuration.FRMULT

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False
