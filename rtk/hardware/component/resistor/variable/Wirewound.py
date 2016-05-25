#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Resistor.Variable Package Wirewound Module
#############################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.resistor.variable.Wirewound.py is part of the
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


class VarWirewound(Resistor):
    """
    The Wirewound Variable resistor data model contains the attributes and
    methods of a Wirewound Variable resistor.  The attributes of a Wirewound
    Variable resistor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 33

    :ivar int n_taps: the number of taps on the potentiometer.
    :ivar float piTAPS: the MIL-HDBK-217FN2 taps factor.
    :ivar float piV: the MIL-HDBK-217FN2 voltage stress factor.

    Covers specifications MIL-R-27208 and MIL-R-39015.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.9
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 12.0, 6.0, 20.0, 5.0, 8.0, 9.0, 15.0, 33.0, 0.5,
                18.0, 48.0, 870.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [0.02, 0.06, 0.2, 0.6, 3.0, 10.0]
    _lst_lambdab_count = [0.025, 0.055, 0.35, 0.15, 0.58, 0.16, 0.26, 0.35,
                          0.58, 1.1, 0.013, 0.52, 1.6, 24.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 33                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Wirewound Variable resistor data model instance.
        """

        super(VarWirewound, self).__init__()

        self.n_taps = 3
        self.piTAPS = 0.0
        self.piV = 0.0

    def set_attributes(self, values):
        """
        Method to set the Wirewound Variable resistor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.n_taps = int(values[117])
            self.piTAPS = float(values[104])
            self.piV = float(values[105])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Wirewound Variable
        resistor data model attributes.

        :return: (n_taps, piTAPS, piV)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_taps, self.piTAPS, self.piV)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Wirewound Variable resistor
        data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write calculate_part; current McCabe Complexity metric = 12.
        from math import exp, sqrt

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piTAPS * piR * piV * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                self.base_hr = 0.0062 * \
                               exp(((self.temperature_active + 273.0) /
                                    358.0)**5.0) * \
                               exp(_stress * ((self.temperature_active +
                                               273.0) / 273.0))
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Potentiometer taps factor.
            self.piTAPS = (self.n_taps**1.5 / 25.0) + 0.792
            self.hazard_rate_model['piTAPS'] = self.piTAPS

            # Resistance factor.
            if self.resistance >= 10.0 and self.resistance <= 2000.0:
                self.piR = 1.0
            elif self.resistance > 2000.0 and self.resistance <= 5000.0:
                self.piR = 1.4
            elif self.resistance > 5000.0 and self.resistance <= 20000.0:
                self.piR = 2.0
            self.hazard_rate_model['piR'] = self.piR

            # Voltage factor.
            _v_applied = sqrt(self.resistance * self.operating_power)
            if _v_applied / self.rated_voltage <= 0.1:
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.1 and
                 _v_applied / self.rated_voltage <= 0.2):
                self.piV = 1.05
            elif(_v_applied / self.rated_voltage > 0.2 and
                 _v_applied / self.rated_voltage <= 0.6):
                self.piV = 1.00
            elif(_v_applied / self.rated_voltage > 0.6 and
                 _v_applied / self.rated_voltage <= 0.7):
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.7 and
                 _v_applied / self.rated_voltage <= 0.8):
                self.piV = 1.22
            elif(_v_applied / self.rated_voltage > 0.8 and
                 _v_applied / self.rated_voltage <= 0.9):
                self.piV = 1.40
            elif _v_applied / self.rated_voltage > 0.9:
                self.piV = 2.00
            self.hazard_rate_model['piV'] = self.piV

        return Resistor.calculate_part(self)


class PrecisionWirewound(Resistor):
    """
    The Precision Wirewound Variable resistor data model contains the
    attributes and methods of a Precision Wirewound Variable resistor.  The
    attributes of a Precision Wirewound Variable resistor are:

    :cvar list _lst_piC: list of MIL-HDBK-217FN2 construction factor values.
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count.
    :cvar int subcategory: default value: 34

    :ivar int n_taps: the number of taps on the potentiometer.
    :ivar int construction: the index in the construction list of the
                            potentiometer.
    :ivar float piTAPS: the MIL-HDBK-217FN2 taps factor.
    :ivar float piV: the MIL-HDBK-217FN2 voltage stress factor.
    :ivar float piC: the MIL-HDBK-217FN2 construction factor.

    Covers specifications MIL-R-12934.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.10
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piC = [2.0, 1.0, 3.0, 1.5]
    _lst_piE = [1.0, 2.0, 18.0, 8.0, 30.0, 8.0, 12.0, 13.0, 18.0, 53.0, 0.5,
                29.0, 76.0, 1400.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [2.5, 5.0]
    _lst_lambdab_count = [0.33, 0.73, 7.0, 2.9, 12.0, 3.5, 5.3, 7.1, 9.8, 23.0,
                          0.16, 11.0, 33.0, 510.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 34                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Precision Wirewound Variable resistor data model
        instance.
        """

        super(PrecisionWirewound, self).__init__()

        self.n_taps = 3
        self.construction = 0
        self.piTAPS = 0.0
        self.piV = 0.0
        self.piC = 0.0

    def set_attributes(self, values):
        """
        Method to set the Precision Wirewound Variable resistor data model
        attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.n_taps = int(values[117])
            self.construction = int(values[118])
            self.piTAPS = float(values[104])
            self.piV = float(values[105])
            self.piC = float(values[106])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Precision Wirewound
        Variable resistor data model attributes.

        :return: (n_taps, construction, piTAPS, piV, piC)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_taps, self.construction, self.piTAPS,
                             self.piV, self.piC)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Precision Wirewound
        Variable resistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write calculate_part; current McCabe Complexity metric = 15.
        from math import exp, sqrt

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piTAPS * piC * piR * piV * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                self.base_hr = 0.0735 * \
                               exp(1.03 * ((self.temperature_active + 273.0) /
                                           358.0)**4.45) * \
                               exp((_stress / 2.74) *
                                   ((self.temperature_active + 273.0) /
                                    273.0)**3.51)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Potentiometer taps factor.
            self.piTAPS = (self.n_taps**1.5 / 25.0) + 0.792
            self.hazard_rate_model['piTAPS'] = self.piTAPS

            # Resistance factor.
            if self.resistance >= 100.0 and self.resistance <= 10000.0:
                self.piR = 1.0
            elif self.resistance > 10000.0 and self.resistance <= 20000.0:
                self.piR = 1.1
            elif self.resistance > 20000.0 and self.resistance <= 50000.0:
                self.piR = 1.4
            elif self.resistance > 50000.0 and self.resistance <= 100000.0:
                self.piR = 2.0
            elif self.resistance > 100000.0 and self.resistance <= 200000.0:
                self.piR = 2.5
            elif self.resistance > 200000.0 and self.resistance <= 500000.0:
                self.piR = 3.5
            self.hazard_rate_model['piR'] = self.piR

            # Voltage factor.
            _v_applied = sqrt(self.resistance * self.operating_power)
            if _v_applied / self.rated_voltage <= 0.1:
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.1 and
                 _v_applied / self.rated_voltage <= 0.2):
                self.piV = 1.05
            elif(_v_applied / self.rated_voltage > 0.2 and
                 _v_applied / self.rated_voltage <= 0.6):
                self.piV = 1.00
            elif(_v_applied / self.rated_voltage > 0.6 and
                 _v_applied / self.rated_voltage <= 0.7):
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.7 and
                 _v_applied / self.rated_voltage <= 0.8):
                self.piV = 1.22
            elif(_v_applied / self.rated_voltage > 0.8 and
                 _v_applied / self.rated_voltage <= 0.9):
                self.piV = 1.40
            elif _v_applied / self.rated_voltage > 0.9:
                self.piV = 2.00
            self.hazard_rate_model['piV'] = self.piV

            # Construction factor.
            self.piC = self._lst_piC[self.construction - 1]
            self.hazard_rate_model['piC'] = self.piC

        return Resistor.calculate_part(self)


class SemiPrecisionWirewound(Resistor):
    """
    The Semi-Precision Wirewound Variable resistor data model contains the
    attributes and methods of a Semi-Precision Wirewound Variable resistor.
    The attributes of a Semi-Precision Wirewound Variable resistor are:

    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 parts stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 35

    :ivar int n_taps: the number of taps on the potentiometer.
    :ivar float piTAPS: the MIL-HDBK-217FN2 taps factor.
    :ivar float piV: the MIL-HDBK-217FN2 voltage stress factor.

    Covers specifications MIL-R-19 and MIL-R-39002.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.11
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0, 0.5,
                0.0, 0.0, 0.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [2.0, 4.0]
    _lst_lambdab_count = [0.15, 0.35, 3.1, 1.2, 5.4, 1.9, 2.8, 0.0, 0.0, 9.0,
                          0.075, 0.0, 0.0, 0.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 35                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Semi-Precision Wirewound Variable resistor data
        model instance.
        """

        super(SemiPrecisionWirewound, self).__init__()

        self.n_taps = 3
        self.piTAPS = 0.0
        self.piV = 0.0

    def set_attributes(self, values):
        """
        Method to set the Semi-Precision Wirewound Variable resistor data model
        attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.n_taps = int(values[117])
            self.piTAPS = float(values[104])
            self.piV = float(values[105])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Semi-Precision Wirewound
        Variable resistor data model attributes.

        :return: (n_taps, piTAPS, piV)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_taps, self.piTAPS, self.piV)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Semi-Precision Wirewound
        Variable resistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write calculate_part; current McCabe Complexity metric = 12.
        from math import exp, sqrt

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piTAPS * piR * piV * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                self.base_hr = 0.0398 * \
                               exp(0.514 * ((self.temperature_active + 273.0) /
                                            313.0)**5.28) * \
                               exp((_stress / 1.44) *
                                   ((self.temperature_active + 273.0) /
                                    273.0)**4.46)
                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
# TODO: Handle overflow error.
                print "OverflowError in Semiprecision Wirewound."
                return True

            # Potentiometer taps factor.
            self.piTAPS = (self.n_taps**1.5 / 25.0) + 0.792
            self.hazard_rate_model['piTAPS'] = self.piTAPS

            # Resistance factor.
            if self.resistance >= 10.0 and self.resistance <= 2000.0:
                self.piR = 1.0
            elif self.resistance > 2000.0 and self.resistance <= 5000.0:
                self.piR = 1.4
            elif self.resistance > 5000.0 and self.resistance <= 10000.0:
                self.piR = 2.0
            self.hazard_rate_model['piR'] = self.piR

            # Voltage factor.
            _v_applied = sqrt(self.resistance * self.operating_power)
            if _v_applied / self.rated_voltage <= 0.1:
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.1 and
                 _v_applied / self.rated_voltage <= 0.2):
                self.piV = 1.05
            elif(_v_applied / self.rated_voltage > 0.2 and
                 _v_applied / self.rated_voltage <= 0.6):
                self.piV = 1.00
            elif(_v_applied / self.rated_voltage > 0.6 and
                 _v_applied / self.rated_voltage <= 0.7):
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.7 and
                 _v_applied / self.rated_voltage <= 0.8):
                self.piV = 1.22
            elif(_v_applied / self.rated_voltage > 0.8 and
                 _v_applied / self.rated_voltage <= 0.9):
                self.piV = 1.40
            elif _v_applied / self.rated_voltage > 0.9:
                self.piV = 2.00
            self.hazard_rate_model['piV'] = self.piV

        return Resistor.calculate_part(self)


class PowerWirewound(Resistor):
    """
    The Power Wirewound Variable resistor data model contains the attributes
    and methods of a Power Wirewound Variable resistor.  The attributes of a
    Power Wirewound Variable resistor are:

    :cvar list _lst_piC: list of MIL-HDBK-217FN2 construction factor values.
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ_count: list of quality factor values for the
                               MIL-HDBK-217FN2 parts count method.
    :cvar list _lst_piQ_stress: list of quality factor values for the
                                MIL-HDBK-217FN2 part stress method.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: default value: 36

    :ivar int n_taps: the number of taps on the potentiometer.
    :ivar int construction: the index in the construction list of the
                            potentiometer.
    :ivar float piTAPS: the MIL-HDBK-217FN2 taps factor.
    :ivar float piV: the MIL-HDBK-217FN2 voltage stress factor.
    :ivar float piC: the MIL-HDBK-217FN2 construction factor.

    Covers specifications MIL-R-22.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 9.12
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piC = [2.0, 1.0]
    _lst_piE = [1.0, 3.0, 16.0, 7.0, 28.0, 8.0, 12.0, 0.0, 0.0, 38.0, 0.5, 0.0,
                0.0, 0.0]
    _lst_piQ_count = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    _lst_piQ_stress = [2.0, 4.0]
    _lst_lambdab_count = [0.15, 0.34, 2.9, 1.2, 5.0, 1.6, 2.4, 0.0, 0.0, 7.6,
                          0.076, 0.0, 0.0, 0.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 36                        # Subcategory ID in rtkcom DB.

    def __init__(self):
        """
        Method to initialize a Power Wirewound Variable resistor data model
        instance.
        """

        super(PowerWirewound, self).__init__()

        self.n_taps = 3
        self.construction = 0
        self.piTAPS = 0.0
        self.piV = 0.0
        self.piC = 0.0

    def set_attributes(self, values):
        """
        Method to set the Power Wirewound Variable resistor data model
        attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Resistor.set_attributes(self, values)

        try:
            self.n_taps = int(values[117])
            self.construction = int(values[118])
            self.piTAPS = float(values[104])
            self.piV = float(values[105])
            self.piC = float(values[106])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Power Wirewound Variable
        resistor data model attributes.

        :return: (n_taps, construction, piTAPS, piV, piC)
        :rtype: tuple
        """

        _values = Resistor.get_attributes(self)

        _values = _values + (self.n_taps, self.construction, self.piTAPS,
                             self.piV, self.piC)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Power Wirewound Variable

        resistor data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write calculate_part; current McCabe Complexity metric = 12.
        from math import exp, sqrt

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piTAPS * piC * piR * piV * piQ * piE'

            # Base hazard rate.
            _stress = self.operating_power / self.rated_power
            try:
                self.base_hr = 0.0481 * \
                               exp(0.334 * ((self.temperature_active + 273.0) /
                                            298.0)**4.66) * \
                               exp((_stress / 1.47) *
                                   ((self.temperature_active + 273.0) /
                                    273.0)**2.83)

                self.hazard_rate_model['lambdab'] = self.base_hr
            except OverflowError:
                # TODO: Handle overflow error.
                return True

            # Potentiometer taps factor.
            self.piTAPS = (self.n_taps**1.5 / 25.0) + 0.792
            self.hazard_rate_model['piTAPS'] = self.piTAPS

            # Resistance factor.
            if self.resistance >= 1.0 and self.resistance <= 2000.0:
                self.piR = 1.0
            elif self.resistance > 2000.0 and self.resistance <= 5000.0:
                self.piR = 1.4
            elif self.resistance > 5000.0 and self.resistance <= 10000.0:
                self.piR = 2.0
            self.hazard_rate_model['piR'] = self.piR

            # Voltage factor.
            _v_applied = sqrt(self.resistance * self.operating_power)
            if _v_applied / self.rated_voltage <= 0.1:
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.1 and
                 _v_applied / self.rated_voltage <= 0.2):
                self.piV = 1.05
            elif(_v_applied / self.rated_voltage > 0.2 and
                 _v_applied / self.rated_voltage <= 0.6):
                self.piV = 1.00
            elif(_v_applied / self.rated_voltage > 0.6 and
                 _v_applied / self.rated_voltage <= 0.7):
                self.piV = 1.10
            elif(_v_applied / self.rated_voltage > 0.7 and
                 _v_applied / self.rated_voltage <= 0.8):
                self.piV = 1.22
            elif(_v_applied / self.rated_voltage > 0.8 and
                 _v_applied / self.rated_voltage <= 0.9):
                self.piV = 1.40
            elif _v_applied / self.rated_voltage > 0.9:
                self.piV = 2.00
            self.hazard_rate_model['piV'] = self.piV

            # Construction factor.
            self.piC = self._lst_piC[self.construction - 1]
            self.hazard_rate_model['piC'] = self.piC

        return Resistor.calculate_part(self)
