#!/usr/bin/env python
"""
##################################################
Hardware.Component.Relay Package Mechanical Module
##################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.relay.Mechanical.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.relay.Relay import Model as Relay
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.relay.Relay import Model as Relay

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


class Mechanical(Relay):
    """
    The Mechanical Relay data model contains the attributes and methods of a
    Mechanical Relay component.  The attributes of a Mechanical Relay are:

    :cvar int subcategory: default value: 64

    :ivar int temperature_rating: default value: 0
    :ivar int load_type: default value: 0
    :ivar int contact_form: default value: 0
    :ivar int contact_rating: default value: 0
    :ivar int application: default value: 0
    :ivar float cycles_per_hour: default value: 0.0
    :ivar float piL: default value: 0.0
    :ivar float piCYC: default value: 0.0
    :ivar float piC: default value: 0.0
    :ivar float piF: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 13.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piC = [1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 4.25, 5.5, 8.0]
    _lst_piF = [[[[4.0, 8.0], [6.0, 18.0], [1.0, 3.0], [4.0, 8.0], [7.0, 14.0],
                  [7.0, 14.0]]],
                [[[3.0, 6.0], [5.0, 10.0], [6.0, 12.0]],
                 [[5.0, 10.0], [2.0, 6.0], [6.0, 12.0], [100.0, 100.0],
                  [10.0, 20.0]],
                 [[10.0, 20.0], [100.0, 100.0]],
                 [[6.0, 12.0], [1.0, 3.0]],
                 [[25.0, 0.0], [6.0, 0.0]],
                 [[10.0, 20.0]],
                 [[9.0, 12.0]],
                 [[10.0, 20.0], [5.0, 10.0], [5.0, 10.0]]],
                [[[20.0, 40.0], [5.0, 10.0]],
                 [[3.0, 6.0], [1.0, 3.0], [2.0, 6.0], [3.0, 6.0], [2.0, 6.0],
                  [2.0, 6.0]]],
                [[[7.0, 14.0], [12.0, 24.0], [10.0, 20.0], [5.0, 10.0]]]]
    _lst_piQ_count = [0.6, 3.0, 9.0]
    _lst_piQ_stress = [0.10, 0.30, 0.45, 0.60, 1.0, 1.5, 3.0, 3.0]
    _lst_piE = [[1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0, 0.50,
                 25.0, 66.0, 0.0],
                [2.0, 5.0, 44.0, 24.0, 78.0, 15.0, 20.0, 28.0, 38.0, 140.0,
                 1.0, 72.0, 200.0, 0.0]]
    _lst_lambdab_count = [[0.13, 0.28, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0,
                           0.66, 3.5, 10.0, 0.0],
                          [0.43, 0.89, 6.9, 3.6, 12.0, 3.4, 4.4, 6.2, 6.7,
                           22.0, 0.21, 11.0, 32.0, 0.0],
                          [0.13, 0.26, 2.1, 1.1, 3.8, 1.1, 1.4, 1.9, 2.0, 7.0,
                           0.66, 3.5, 10.0, 0.0],
                          [0.11, 0.23, 1.8, 0.92, 3.3, 0.96, 1.2, 2.1, 2.3,
                           6.5, 0.54, 3.0, 9.0, 0.0],
                          [0.29, 0.60, 4.8, 2.4, 8.2, 2.3, 2.9, 4.1, 4.5, 15.0,
                           0.14, 7.6, 22.0, 0.0],
                          [0.88, 1.8, 14.0, 7.4, 26.0, 7.1, 9.1, 13.0, 14.0,
                           46.0, 0.44, 24.0, 67.0, 0.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 64

    def __init__(self):
        """
        Method to initialize an Mechanical Relay data model instance.
        """

        super(Mechanical, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.temperature_rating = 0
        self.load_type = 0
        self.contact_form = 0
        self.contact_rating = 0
        self.application = 0
        self.cycles_per_hour = 0.0
        self.piL = 0.0
        self.piCYC = 0.0
        self.piC = 0.0
        self.piF = 0.0

    def set_attributes(self, values):
        """
        Method to set the Mechanical Relay data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Relay.set_attributes(self, values)

        try:
            self.temperature_rating = int(values[118])
            self.load_type = int(values[119])
            self.contact_form = int(values[120])
            self.contact_rating = int(values[121])
            self.application = int(values[122])
            self.cycles_per_hour = float(values[100])
            self.piL = float(values[101])
            self.piCYC = float(values[102])
            self.piC = float(values[103])
            self.piF = float(values[104])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mechanical Relay data
        model attributes.

        :return: (temperature_rating, load_type, contact_form, contact_rating,
                  application, cycles_per_hour, piL, piCYC, piC, piF)
        :rtype: tuple
        """

        _values = Relay.get_attributes(self)

        _values = _values + (self.temperature_rating, self.load_type,
                             self.contact_form, self.contact_rating,
                             self.application, self.cycles_per_hour, self.piL,
                             self.piCYC, self.piC, self.piF)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Mechanical Relay data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write calculate_part; current McCabe Complexity metric = 15.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab_count[self.construction - 1][self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ_count[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piL * piC * piCYC * piF * piQ * piE'

            # Set the base hazard rate for the model.
            if self.temperature_rating == 1:
                self.base_hr = 0.0055 * \
                               exp(((self.temperature_active + 273.0) /
                                    352.0)**15.7)
            else:
                self.base_hr = 0.0054 * \
                               exp(((self.temperature_active + 273.0) /
                                    377.0)**10.4)
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the load stress factor for the model.
            _stress = self.operating_current / self.rated_current
            if self.load_type == 1:         # Resistive
                self.piL = exp((_stress / 0.8)**2.0)
            elif self.load_type == 2:       # Inductive
                self.piL = exp((_stress / 0.4)**2.0)
            else:                           # Lamp, et. al.
                self.piL = exp((_stress / 0.2)**2.0)
            self.hazard_rate_model['piL'] = self.piL

            # Set the contact form factor for the model.
            self.piC = self._lst_piC[self.contact_form - 1]
            self.hazard_rate_model['piC'] = self.piC

            # Set the quality factor for the model.
            self.piQ = self._lst_piQ_stress[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

            # Set the cycling, application and construction, and environment
            # factors for the model.
            if self.quality < 7:            # MIL-SPEC
                if self.cycles_per_hour >= 1.0:
                    self.piCYC = self.cycles_per_hour / 10.0
                else:
                    self.piCYC = 0.1
                self.piF = self._lst_piF[self.contact_rating - 1][self.application - 1][self.construction - 1][0]
                self.piE = self._lst_piE[0][self.environment_active - 1]
            else:
                if self.cycles_per_hour > 1000.0:
                    self.piCYC = (self.cycles_per_hour / 100.0)**2.0
                elif(self.cycles_per_hour >= 10.0 and
                     self.cycles_per_hour <= 1000.0):
                    self.piCYC = self.cycles_per_hour / 10.0
                else:
                    self.piCYC = 1.0
                self.piF = self._lst_piF[self.contact_rating - 1][self.application - 1][self.construction - 1][1]
                self.piE = self._lst_piE[1][self.environment_active - 1]
            self.hazard_rate_model['piCYC'] = self.piCYC
            self.hazard_rate_model['piF'] = self.piF
            self.hazard_rate_model['piE'] = self.piE

        return Relay.calculate_part(self)
