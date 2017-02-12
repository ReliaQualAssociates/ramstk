#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Switch.Toggle Switch Package Toggle Module
#############################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Toggle.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.switch.Switch import Model as Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.switch.Switch import Model as Switch

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


class Toggle(Switch):
    """
    The Toggle Switch data model contains the attributes and methods of a
    Toggle Switch component.  The attributes of a Toggle Switch are:

    :cvar int subcategory: the Switch subcategory.

    :ivar int construction: the MIL-HDBK-217FN2 contruction index.
    :ivar int contact_form: the MIL-HDBK-217FN2 contact form index.
    :ivar int load_type: the MIL-HDBK-217FN2 load type index.
    :ivar float cycles_per_hour: the MIL-HDBK-217FN2 switch cycles per hour.
    :ivar float piCYC: the MIL-HDBK-217FN2 cycles factor.
    :ivar float piL: the MIL-HDBK-217FN2 load type factor.
    :ivar float piC: the MIL-HDBK-217FN2 contact form factor.

    Covers specifications MIL-S-3650, MIL-S-8805, MIL-S-8834, MIL-S-22885, and
    MIL-S-83731.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 14.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piC = [1.0, 1.5, 1.7, 2.0, 2.5, 3.0, 4.2, 5.5, 8.0]
    _lst_piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5,
                25.0, 67.0, 1200.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.0010, 0.0030, 0.018, 0.0080, 0.029, 0.010, 0.018,
                          0.013, 0.022, 0.046, 0.0005, 0.025, 0.067, 1.2]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 67

    def __init__(self):
        """
        Method to initialize a Toggle Switch data model instance.
        """

        super(Toggle, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.construction = 0
        self.contact_form = 0
        self.load_type = 0
        self.cycles_per_hour = 0.0
        self.piCYC = 0.0
        self.piL = 0.0
        self.piC = 0.0

    def set_attributes(self, values):
        """
        Method to set the Toggle Switch data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Switch.set_attributes(self, values)

        try:
            self.construction = int(values[117])
            self.contact_form = int(values[118])
            self.load_type = int(values[119])
            self.cycles_per_hour = float(values[99])
            self.piCYC = float(values[100])
            self.piL = float(values[101])
            self.piC = float(values[102])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Toggle Switch data model
        attributes.

        :return: (construction, contact_form, load_type, cycles_per_hour,
                  piCYC, piL, piC)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.construction, self.contact_form,
                             self.load_type, self.cycles_per_hour, self.piCYC,
                             self.piL, self.piC)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Toggle Switch data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 13.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piCYC * piL * piC * piE'

            # Set the base hazard rate for the model.
            if self.construction == 1:      # Snap-action
                if self.quality == 1:       # MIL-SPEC
                    self.base_hr = 0.00045
                else:
                    self.base_hr = 0.034
            else:                           # Non-snap action
                if self.quality == 1:       # MIL-SPEC
                    self.base_hr = 0.0027
                else:
                    self.base_hr = 0.040
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the cycling factor for the model.
            if self.cycles_per_hour <= 1.0:
                self.piCYC = 1.0
            else:
                self.piCYC = float(self.cycles_per_hour)
            self.hazard_rate_model['piCYC'] = self.piCYC

            # Set the load stress factor for the model.
            _stress = self.operating_current / self.rated_current
            if self.load_type == 1:         # Resistive
                self.piL = exp((_stress / 0.8)**2.0)
            elif self.load_type == 2:       # Inductive
                self.piL = exp((_stress / 0.4)**2.0)
            elif self.load_type == 3:       # Lamp
                self.piL = exp((_stress / 0.2)**2.0)
            self.hazard_rate_model['piL'] = self.piL

            # Set the contact form and quantity factor for the model.
            self.piC = self._lst_piC[self.contact_form - 1]
            self.hazard_rate_model['piC'] = self.piC

        return Switch.calculate_part(self)
