#!/usr/bin/env python
"""
##############################################################
Hardware.Component.Resistor.Variable Package Thermistor Module
##############################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.variable.Thermistor.py is part of the
#       RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.resistor.Resistor import Model as Resistor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.resistor.Resistor import Model as Resistor

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


class Thermistor(Resistor):
    """
    The Thermistor resistor data model contains the attributes and methods of
    a Thermistor resistor.  The attributes of a Thermistor resistor are:

    :cvar list _lst_piR: list of MIL-HDBK-217FN2 resistance factor values.
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 32

    :ivar int type: index in the MIL-HDBK-217FN2 type list.

    Covers specifications MIL-T-23648.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.8
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 5.0, 21.0, 11.0, 24.0, 11.0, 30.0, 16.0, 42.0, 37.0, 0.5,
                20.0, 53.0, 950.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [1.0, 15.0]
    _lst_lambdab_count = [0.065, 0.32, 1.4, 0.71, 1.6, 0.71, 1.9, 1.0, 2.7,
                          2.4, 0.032, 1.3, 3.4, 62.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 32                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Thermistor resistor data model instance.
        """

        super(Thermistor, self).__init__()

        self.type = 0

    def set_attributes(self, values):
        """
        Method to set the Thermistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.type = int(values[117])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Thermistor data model
        attributes.

        :return: (type)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.type, )

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Thermistor resistor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            if self.type == 1:              # Bead
                self.base_hr = 0.021
            elif self.type == 2:            # Disk
                self.base_hr = 0.065
            elif self.type == 3:            # Rod
                self.base_hr = 0.105
            self.hazard_rate_model['lambdab'] = self.base_hr

        return Resistor.calculate_part(self)
