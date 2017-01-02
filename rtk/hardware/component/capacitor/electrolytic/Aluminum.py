#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.electrolytic.Aluminum.py is part of
#       the RTK Project
#
# All rights reserved.

"""
#############################################
Hardware Package Electrolytic Aluminum Module
#############################################
"""

import gettext
import locale

try:
    import Configuration
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

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


class Dry(Capacitor):
    """
    The dry aluminum electrolytic capacitor data model contains the
    attributes and methods of a dry aluminum electrolytic capacitor.  The
    attributes of a dry aluminum electrolytic capacitor are:

    :ivar piCV: default value: 0.0

    Covers specification MIL-C-62.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.15
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0, 28.0, 35.0, 27.0, 0.5, 14.0,
            38.0, 690.0]
    _piQ = [3.0, 10.0]
    _lambdab_count = [0.029, 0.081, 0.58, 0.24, 0.83, 0.73, 0.88, 4.3, 5.4,
                      2.0, 0.015, 0.68, 2.8, 28.0]
    lst_ref_temp = [358]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 54                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a dry aluminum electrolytic capacitor data model
        instance.
        """

        super(Dry, self).__init__()

        # Initialize public scalar attributes.
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Dry Aluminum capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.0028 * ((_stress / 0.55)**3 + 1) * \
                    exp(4.09 * ((self.temperature_active + 273) /
                                self.reference_temperature)**5.9)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow and zero division errors.
                return True

            # Capacitance correction factor.
            self.piCV = 0.34 * (self.capacitance * 1000000.0)**0.18
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)


class Wet(Capacitor):
    """
    The wet aluminum electrolytic capacitor data model contains the
    attributes and methods of a wet aluminum electrolytic capacitor.  The
    attributes of a wet aluminum electrolytic capacitor are:

    Covers specifications MIL-C-3965 and MIL-C-39006.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.13
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0, 28.0, 35.0, 27.0, 0.5, 14.0,
            38.0, 690.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lambdab_count = [0.024, 0.061, 0.42, 0.18, 0.59, 0.46, 0.55, 2.1, 2.6,
                      1.2, .012, 0.49, 1.7, 21.0]
    lst_ref_temp = [358.0, 378.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 53                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize the Wet Aluminum Electrolytic Capacitor Component
        Class.
        """

        super(Wet, self).__init__()

        # Define public scalar attributes.
        if self.hazard_rate_type < 3:       # MIL-HDBK-217FN2
            if self.max_rated_temperature == 105.0:
                self.reference_temperature = 378.0
            elif self.max_rated_temperature == 125.0:
                self.reference_temperature = 398.0
            else:
                self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Wet Aluminum capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00254 * ((_stress / 0.5)**3 + 1) * \
                    exp(5.09 * ((self.temperature_active + 273) /
                                self.reference_temperature)**5)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow and zero division errors.
                return True

            # Capacitance correction factor.
            self.piCV = 0.34 * (self.capacitance * 1000000.0)**0.18
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)
