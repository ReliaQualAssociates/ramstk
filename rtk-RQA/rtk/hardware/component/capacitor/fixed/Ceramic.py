#!/usr/bin/env python
"""
#########################################################
Hardware.Component.Capacitor.Fixed Package Ceramic Module
#########################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.fixed.Ceramic.py is part of the RTK
#       Project
#
# All rights reserved.

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


class Chip(Capacitor):
    """
    The Ceramic Chip capacitor data model contains the attributes and methods
    of a ceramic chip capacitor.  The attributes of a ceramic chip capacitor
    are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 40

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specifications MIL-C-20 and MIL-C-55681.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.11
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 10.0, 5.0, 17.0, 4.0, 8.0, 16.0, 35.0, 24.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lambdab_count = [0.00078, 0.0022, 0.013, 0.0056, 0.023, 0.0077, 0.015,
                      0.053, 0.12, 0.048, 0.00039, 0.017, 0.065, 0.68]
    lst_ref_temp = [358.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 50                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Ceramic Chip capacitor data model instance.
        """

        super(Chip, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Ceramic Chip capacitor data
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
                    0.0000000025 * ((_stress / 0.3)**3 + 1) * \
                    exp(14.3 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.59 * (self.capacitance * 1000000.0)**0.12
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)


class General(Capacitor):
    """
    The General Ceramic capacitor data model contains the attributes and
    methods of a general ceramic capacitor.  The attributes of a general
    ceramic capacitor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 49

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specifications MIL-C-11015 and MIL-C-39014.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.10
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----------------------------------------------------------------- #
    _piE = [1.0, 2.0, 9.0, 5.0, 15.0, 4.0, 4.0, 8.0, 12.0, 20.0, 0.4, 13.0,
            34.0, 610.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0]
    _lambdab_count = [0.0036, 0.0074, 0.034, 0.019, 0.056, 0.015, 0.015, 0.032,
                      0.048, 0.077, 0.0014, 0.049, 0.13, 2.3]
    lst_ref_temp = [358.0, 398.0, 423.0]
    # ----------------------------------------------------------------- #

    subcategory = 49                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a General Ceramic capacitor data model instance.
        """

        super(General, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217FN2
            self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Fixed Paper Feedthrough
        capacitor data model.

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
                    0.0003 * ((_stress / 0.3)**3 + 1) * \
                    exp(((self.temperature_active + 273) /
                         self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.41 * (self.capacitance * 1000000.0)**0.11
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)
