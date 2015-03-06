#!/usr/bin/env python
"""
######################################################
Hardware.Component.Capacitor.Fixed Package Mica Module
######################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.fixed.Mica.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import configuration as _conf
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Button(Capacitor):
    """
    The Mica Button capacitor data model contains the attributes and methods of
    a mica button capacitor.  The attributes of a mica button capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specifications MIL-C-11272 and MIL-C-23269.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.9
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 10.0, 5.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [5.0, 15.0]
    _lambdab_count = [0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14, 0.47, 0.60,
                      0.48, 0.0091, 0.25, 0.68, 11.0]
    lst_ref_temp = [358.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 47

    def __init__(self):
        """
        Initialize a Mica Button capacitor data model instance.
        """

        super(Button, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
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
                    0.0053 * ((_stress / 0.4)**3 + 1) * \
                    exp(1.2 * ((self.temperature_active + 273) /
                               self.reference_temperature)**6.3)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.31 * (self.capacitance * 1000000.0)**0.23
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate(self)


class Mica(Capacitor):
    """
    The Mica capacitor data model contains the attributes and methods of
    a mica capacitor.  The attributes of a mica capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specifications MIL-C-5 and MIL-C-39001.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.7
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 6.0, 15.0]
    _lambdab_count = [0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068, 0.0095,
                      0.054, 0.069, 0.031, 0.00025, 0.012, 0.046, 0.45]
    lst_ref_temp = [343.0, 358.0, 398.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 46

    def __init__(self):
        """
        Initialize a Mica Button capacitor data model instance.
        """

        super(Mica, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 343.0

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
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
                    0.00000000086 * ((_stress / 0.4)**3 + 1) * \
                    exp(16.0 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.45 * (self.capacitance * 1000000.0)**0.14
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate(self)
