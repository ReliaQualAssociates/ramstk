#!/usr/bin/env python
"""
#####################################################################
Hardware.Component.Switch.Thumbwheel Switch Package Thumbwheel Module
#####################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Thumbwheel.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
<<<<<<< HEAD
    import Configuration as _conf
    import Utilities as _util
    from hardware.component.switch.Switch import Model as \
        Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
=======
    import Configuration
    import Utilities
    from hardware.component.switch.Switch import Model as \
        Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    from rtk.hardware.component.switch.Switch import Model as \
        Switch

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Thumbwheel(Switch):
    """
    The Thumbwheel Switch data model contains the attributes and methods of a
    Thumbwheel Switch component.  The attributes of a Thumbwheel Switch are:

<<<<<<< HEAD
    :cvar subcategory: default value: 70

    :ivar load_type: default value: 0
    :ivar n_contacts: default value: 0
    :ivar cycles_per_hour: default value: 0.0
    :ivar base_hr2: default value: 0.0
    :ivar piN: default value: 0.0
    :ivar piCYC: default value: 0.0
    :ivar piL: default value: 0.0
=======
    :cvar int subcategory: Switch subcategory.

    :ivar int load_type: the MIL-HDBK-217FN2 load type input index.
    :ivar int n_contacts: the MIL-HDBK-217FN2 number of active contacts input.
    :ivar float cycles_per_hour: the MIL-HDBK-217FN2 cycles per hour input.
    :ivar float base_hr2: the MIL-HDBK-217FN2 active contacts base hazard rate.
    :ivar float piN: the MIL-HDBK-217FN2 number of active contacts factor.
    :ivar float piCYC: the MIL-HDBK-217FN2 cycles per hour factor.
    :ivar float piL: the MIL-HDBK-217FN2 load type factor.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specification MIL-S-22710.

    Hazard Rate Models:
<<<<<<< HEAD
        # MIL-HDBK-217F, section 14.4.
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
        # MIL-HDBK-217FN2, section 14.4.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5,
                25.0, 67.0, 1200.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.56, 1.7, 10.0, 4.5, 16.0, 5.6, 10.0, 7.3, 12.0,
                          26.0, 0.26, 14.0, 38.0, 670.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 70

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Thumbwheel Switch data model instance.
=======
        Method to initialize a Thumbwheel Switch data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Thumbwheel, self).__init__()

<<<<<<< HEAD
        # Initialize public scalar attributes.
=======
        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.load_type = 0
        self.n_contacts = 0                 # Number of active contacts
        self.cycles_per_hour = 0.0
        self.base_hr2 = 0.0
        self.piN = 0.0
        self.piCYC = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Thumbwheel Switch data model attributes.
=======
        Method to set the Thumbwheel Switch data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Switch.set_attributes(self, values)

        try:
            self.load_type = int(values[117])
            self.n_contacts = int(values[118])
            self.cycles_per_hour = float(values[99])
            self.base_hr2 = float(values[100])
            self.piN = float(values[101])
            self.piCYC = float(values[102])
            self.piL = float(values[103])
        except IndexError as _err:
<<<<<<< HEAD
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
=======
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
<<<<<<< HEAD
        Retrieves the current values of the Thumbwheel Switch data model
        attributes.
=======
        Method to retrieve the current values of the Thumbwheel Switch data
        model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: (load_type, n_contacts, cycles_per_hour, base_hr2, piN, piCYC,
                  piL)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.load_type, self.n_contacts,
                             self.cycles_per_hour, self.base_hr2, self.piN,
                             self.piCYC, self.piL)

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Thumbwheel Switch data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Thumbwheel Switch data
        model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = '(lambdab + piN * lambdab2) * piCYC * piL * piE'

            # Set the base hazard rate for the model.
            if self.quality == 1:       # MIL-SPEC
                self.base_hr = 0.0067
                self.base_hr2 = 0.062
            else:
                self.base_hr = 0.086
                self.base_hr2 = 0.089
            self.hazard_rate_model['lambdab'] = self.base_hr
            self.hazard_rate_model['lambdab2'] = self.base_hr2

            # Set the number of active contacts factor for the model.
            self.piN = float(self.n_contacts)
            self.hazard_rate_model['piN'] = self.piN

            # Set the cycling factor for the model.
            if self.cycles_per_hour <= 1.0:
                self.piCYC = 1.0
            else:
                self.piCYC = float(self.cycles_per_hour)
            self.hazard_rate_model['piCYC'] = self.piCYC

            # Set the load stress factor for the model.
            _stress = self.operating_current / self.rated_current
            if self.load_type == 1:         # Resistive
                self.piL = exp((_stress / 0.8)**2.0)
            elif self.load_type == 2:       # Inductive
                self.piL = exp((_stress / 0.4)**2.0)
            elif self.load_type == 3:       # Lamp
                self.piL = exp((_stress / 0.2)**2.0)
            self.hazard_rate_model['piL'] = self.piL

<<<<<<< HEAD
        return Switch.calculate(self)
=======
        return Switch.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
