#!/usr/bin/env python
"""
#######################################################
Hardware.Component.Capacitor.Fixed Package Glass Module
#######################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.fixed.Glass.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration as _conf
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Glass(Capacitor):
    """
    The Glass capacitor data model contains the attributes and methods of a
    glass capacitor.  The attributes of a glass capacitor are:

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
    _piE = [1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.03, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0]
    _lambdab_count = [0.00032, 0.00096, 0.0059, 0.0029, 0.0094, 0.0044, 0.0062,
                      0.035, 0.045, 0.020, 0.00016, 0.0076, 0.030, 0.29]
    lst_ref_temp = [398.0, 473.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 48

    def __init__(self):
        """
        Initialize a Ceramic Chip capacitor data model instance.
        """

        super(Glass, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 398.0

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
                    0.000000000825 * ((_stress / 0.5)**4 + 1) * \
                    exp(16.0 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 0.62 * (self.capacitance * 1000000.0)**0.14
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate(self)
