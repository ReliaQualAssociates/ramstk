#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Semiconductor Package Semiconductor Module
#############################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.Semiconductor.py is part of the
#       RTK Project
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
    The Semiconductor data model contains the attributes and methods of a
    Semiconductor component.  The attributes of a Semiconductor are:

    :cvar category: default value: 2

    :ivar int quality: default value: 0
    :ivar float q_override: default value: 0.0
    :ivar float base_hr: default value: 0.0
    :ivar float piQ: default value: 0.0
    :ivar float piE: default value: 0.0
    :ivar float piT: default value: 0.0
    :ivar str reason: default value: ""

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.
    """

    category = 2

    def __init__(self):
        """
        Method to initialize a Semiconductor data model instance.
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
        Method to set the Semiconductor data model attributes.

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
        Method to retrieve the current values of the Semiconductor data model
        attributes.

        :return: (quality, q_override, base_hr, piQ, piE, piT, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.q_override, self.base_hr,
                             self.piQ, self.piE, self.piT, self.reason)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Semiconductor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error = 0
        _messages = []

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
            try:
                self.hazard_rate_model['piQ'] = self.piQ
            except TypeError:
                _error = 100
                _messages.append(_(u"ERROR: Component {0:s} failed to "
                                   u"calculate.  No quality level specified "
                                   u"and no default quality level "
                                   u"exists.").format(self.name))

            # Set the environment pi factor for the model.
            self.piE = self._lst_piE[self.environment_active - 1]
            try:
                self.hazard_rate_model['piE'] = self.piE
            except TypeError:
                _error = 100
                _messages.append(_(u"ERROR: Component {0:s} failed to "
                                   u"calculate.  No operating environment "
                                   u"specified and no default operating "
                                   u"environment exists.").format(self.name))


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
