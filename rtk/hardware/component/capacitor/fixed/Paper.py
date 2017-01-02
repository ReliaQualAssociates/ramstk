#!/usr/bin/env python
"""
#######################################################
Hardware.Component.Capacitor.Fixed Package Paper Module
#######################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.fixed.Paper.py is part of the RTK
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


class Bypass(Capacitor):
    """
    The Paper, Fixed, Bypass capacitor data model contains the attributes and
    methods of a fixed paper bypass capacitor.  The attributes of a fixed paper
    bypass capacitor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 40

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specifications MIL-C-25 and MIL-C-12889.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.1
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 9.0, 5.0, 15.0, 6.0, 8.0, 17.0, 32.0, 22.0, 0.5, 12.0,
            32.0, 670.0]
    _piQ = [3.0, 7.0]
    _lambdab_count = [[0.0036, 0.0072, 0.330, 0.016, 0.055, 0.023, 0.030, 0.07,
                       0.13, 0.083, 0.0018, 0.044, 0.12, 2.1],
                      [0.0039, 0.0087, 0.042, 0.022, 0.070, 0.035, 0.047, 0.19,
                       0.35, 0.130, 0.0020, 0.056, 0.19, 2.5]]
    lst_ref_temp = [358.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 40                        # Subcategory ID in the common DB.

    def __init__(self):
        """
        Method to initialize a fixed paper bypass capacitor data model
        instance.
        """

        super(Bypass, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0              # MIL-C-25 or MIL-C-12889.
        self.spec_sheet = 0                 #
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

#    def set_attributes(self, values):
        """
        Method to set the Capacitor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

 #       _code = 0
  #      _msg = ''

   #     (_code, _msg) = Capacitor.set_attributes(self, values[:119])

    #    return(_code, _msg)

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Fixed Paper Bypass
        capacitor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            self._lambdab_count = self._lambdab_count[self.specification - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCV'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00086 * ((_stress / 0.4)**5 + 1) * \
                    exp(2.5 * ((self.temperature_active + 273) /
                               self.reference_temperature)**18)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow and zero division errors.
                return True

            # Capacitance correction factor.
            self.piCV = 1.2 * (self.capacitance * 1000000.0)**0.095
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)


class Feedthrough(Capacitor):
    """
    The Paper, Fixed, Feedthrough capacitor data model contains the attributes
    and methods of a fixed paper feedthrough capacitor.  The attributes of a
    fixed paper feedthrough capacitor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 41

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specification MIL-C-11693.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.2
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 9.0, 7.0, 15.0, 6.0, 8.0, 17.0, 28.0, 22.0, 0.5, 12.0,
            32.0, 570.0]
    _piQ = [1.0, 3.0, 10.0]
    _lambdab_count = [0.0047, 0.0096, 0.044, 0.034, 0.073, 0.030, 0.040, 0.094,
                      0.15, 0.11, 0.0024, 0.058, 0.18, 2.7]
    lst_ref_temp = [358.0, 398.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 41                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a fixed paper feedthrough capacitor data model
        instance.
        """

        super(Feedthrough, self).__init__()

        # Initialize public scalar attributes.
        self.spec_sheet = 0                 # Characteristic E, K, P, or W.
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
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
                    0.00115 * ((_stress / 0.4)**5 + 1) * \
                    exp(2.5 * ((self.temperature_active + 273) /
                               self.reference_temperature)**18)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 1.4 * (self.capacitance * 1000000.0)**0.12
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)


class Metallized(Capacitor):
    """
    The Fixed Metallized Paper capacitor data model contains the attributes
    and methods of a fixed metallized paper capacitor.  The attributes of a
    fixed metallized paper capacitor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 41

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0

    Covers specifications MIL-C-18312 and MIL-C-39022.

    Hazard Rate Models:
        #. MIL-HDBK-217F, section 10.4
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 6.0, 11.0, 20.0, 20.0, 0.5, 11.0,
            29.0, 530.0]
    _piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 7.0, 20.0]
    _lambdab_count = [0.0029, 0.0058, 0.023, 0.014, 0.041, 0.012, 0.018, 0.037,
                      0.066, 0.060, 0.0014, 0.032, 0.088, 1.5]
    lst_ref_temp = [358.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 43               # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a fixed metallized paper capacitor data model
        instance.
        """

        super(Metallized, self).__init__()

        # Initialize public scalar attributes.
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculates the hazard rate for the Fixed Metallized Paper
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
                    0.00069 * ((_stress / 0.4)**5 + 1) * \
                    exp(2.5 * ((self.temperature_active + 273) /
                               self.reference_temperature)**18)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

            # Capacitance correction factor.
            self.piCV = 1.2 * (self.capacitance * 1000000.0)**0.092
            self.hazard_rate_model['piCV'] = self.piCV

        return Capacitor.calculate_part(self)
