#!/usr/bin/env python
"""
#########################################################
Hardware.Component.Capacitor.Fixed Package Plastic Module
#########################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.fixed.Plastic.py is part of the RTK
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


class Film(Capacitor):
    """
    The Plastic Film capacitor data model contains the attributes and methods
    of a plastic film capacitor.  The attributes of a plastic film capacitor
    are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specifications MIL-C-14157 and MIL-C-19978.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.3
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0, 11.0, 20.0, 20.0, 0.5, 11.0,
            29.0, 530.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
    _lambdab_count = [0.0021, 0.0042, 0.017, 0.010, 0.030, 0.0068, 0.013,
                      0.026, 0.048, 0.044, 0.0010, 0.023, 0.063, 1.1]
    lst_ref_temp = [338.0, 358.0, 398.0, 443.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 42

    def __init__(self):
        """
        Initialize a Plastic Film capacitor data model instance.
        """

        super(Film, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 338.0

    def calculate(self):
        """
        Calculates the hazard rate for the Plastic Film capacitor data
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
                    0.0005 * ((_stress / 0.4)**5 + 1) * \
                    exp(2.5 * ((self.temperature_active + 273) /
                               self.reference_temperature)**18)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            if self.specification == 1:
                self.piCV = 1.6 * (self.capacitance * 1000000.0)**0.13
            elif self.specification == 2:
                self.piCV = 1.3 * (self.capacitance * 1000000.0)**0.077
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate(self)


class Plastic(Capacitor):
    """
    The Plastic capacitor data model contains the attributes and methods of
    a plastic capacitor.  The attributes of a plastic capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specifications MIL-C-55514.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.5
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 10.0, 5.0, 16.0, 6.0, 11.0, 18.0, 30.0, 23.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 10.0]
    _lambdab_count = [0.0041, 0.0083, 0.042, 0.021, 0.067, 0.026, 0.048, 0.086,
                      0.14, 0.10, 0.0020, 0.054, 0.15, 2.5]
    lst_ref_temp = [358.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 44

    def __init__(self):
        """
        Initialize a Plastic capacitor data model instance.
        """

        super(Plastic, self).__init__()

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
                    0.00099 * ((_stress / 0.4)**5 + 1) * \
                    exp(2.5 * ((self.temperature_active + 273) /
                               self.reference_temperature)**18)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 1.1 * (self.capacitance * 1000000.0)**0.085
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate(self)


class SuperMetallized(Capacitor):
    """
    The Super-Metallized Plastic capacitor data model contains the attributes
    and methods of a super-metallized plastic capacitor.  The attributes of a
    super-metallized plastic capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specifications MIL-C-83421.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.6
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 4.0, 8.0, 5.0, 14.0, 4.0, 6.0, 13.0, 20.0, 20.0, 0.5, 11.0,
            29.0, 530.0]
    _piQ = [0.02, 0.1, 0.3, 1.0, 10.0]
    _lambdab_count = [0.0023, 0.0092, 0.019, 0.012, 0.033, 0.0096, 0.014,
                      0.034, 0.053, 0.048, 0.0011, 0.026, 0.07, 1.2]
    lst_ref_temp = [398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 45

    def __init__(self):
        """
        Initialize a Super-Metallized Plastic capacitor data model instance.
        """

        super(SuperMetallized, self).__init__()

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
                    0.00055 * ((_stress / 0.4)**5 + 1) * \
                    exp(2.5 * ((self.temperature_active + 273) /
                               self.reference_temperature)**18)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 1.2 * (self.capacitance * 1000000.0)**0.092
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate(self)
