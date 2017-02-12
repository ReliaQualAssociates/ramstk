#!/usr/bin/env python
"""
################################################
Transistor Package Unijunction Transistor Module
################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.transistor.Unijunction.py is part
#       of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    from rtk.hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor

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


class Unijunction(Semiconductor):
    """
    The Unijunction Transistor data model contains the attributes and methods
    of a Unijunction Transistor component.  The attributes of a Unijunction
    Transistor are:

    :cvar subcategory: default value: 16

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.5.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                14.0, 32.0, 320.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_lambdab_count = [0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80, 0.74, 1.6,
                          0.66, 0.0079, 0.31, 0.88, 6.4]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 16

    def __init__(self):
        """
        Initialize a Unijunction Transistor data model instance.
        """

        super(Unijunction, self).__init__()

        # Initialize public scalar attributes.
        self.base_hr = 0.0083

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Unijunction Transistor
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piQ * piE'

            # Set the base hazard rate for the model.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
            self.piT = exp(-2483.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the Unijunction Transistor is overstressed
        based on it's rated values and operating environment.

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
            if self.operating_power > 0.70 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 70% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.75 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 70% rated voltage.\n"
                _reason_num += 1
            if self.junction_temperature > 125.0:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
                _reason_num += 1
        else:
            if self.operating_power > 0.90 * self.rated_power:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating power > 90% rated power.\n"
                _reason_num += 1
            if self.operating_voltage > 0.90 * self.rated_voltage:
                self.overstress = True
                _reason = _reason + str(_reason_num) + \
                          ". Operating voltage > 90% rated voltage.\n"
                _reason_num += 1

        self.reason = _reason

        return False
