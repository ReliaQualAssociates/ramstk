#!/usr/bin/env python
"""
################################################
Hardware.Component.Switch Package Breaker Module
################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Breaker.py is part of the RTK Project
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


class Breaker(Switch):
    """
    The Breaker Switch data model contains the attributes and methods of a
    Breaker Switch component.  The attributes of a Breaker Switch are:

<<<<<<< HEAD
    :cvar subcategory: default value: 71

    :ivar construction: default value: 0
    :ivar contact_form: default value: 0
    :ivar use: default value: 0
    :ivar piC: default value: 0.0
    :ivar piU: default value: 0.0
    :ivar piQ: default value: 0.0
=======
    :cvar int subcategory: Switch subcategory

    :ivar int construction: the MIL-HDBK-217FN2 construction input index.
    :ivar int contact_form: the MIL-HDBK-217FN2 contact form input index.
    :ivar int use: the MIL-HDBK-217FN2 application input index.
    :ivar float piC: the MIL-HDBK-217FN2 configuration factor.
    :ivar float piU: the MIL-HDBK-217FN2 usage factor.
    :ivar float piQ: the MIL-HDBK-217FN2 quality factor.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specifications MIL-C-39019, MIL-C-55629, MIL-C-83383, and W-C-375.

    Hazard Rate Models:
<<<<<<< HEAD
        # MIL-HDBK-217F, section 14.5.
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
        # MIL-HDBK-217FN2, section 14.5.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piC = [1.0, 2.0, 3.0, 4.0]
    _lst_piE = [1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0, 0.5,
                25.0, 67.0, 0.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66, 0.72,
                          2.8, 0.030, 1.5, 4.0, 0.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 71

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Breaker Switch data model instance.
=======
        Method to initialize a Breaker Switch data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Breaker, self).__init__()

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
        self.construction = 0
        self.contact_form = 0
        self.use = 0
        self.piC = 0.0
        self.piU = 0.0
        self.piQ = 0.0

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Breaker Switch data model attributes.
=======
        Method to set the Breaker Switch data model attributes.
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
            self.construction = int(values[117])
            self.contact_form = int(values[118])
            self.use = int(values[119])
            self.piC = float(values[99])
            self.piU = float(values[100])
            self.piQ = float(values[101])
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
        Retrieves the current values of the Breaker Switch data model
=======
        Method to retrieve the current values of the Breaker Switch data model
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        attributes.

        :return: (construction, contact_form, use, piC, piU, piQ)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.construction, self.contact_form, self.use,
                             self.piC, self.piU, self.piQ)

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Breaker Switch data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Breaker Switch data model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piC * piU * piQ * piE'

            # Set the base hazard rate for the model.
            if self.construction == 1:      # Magnetic
                self.base_hr = 0.020
            elif self.construction == 2:    # Thermal
                self.base_hr = 0.038
            else:                           # Thermal-magnetic
                self.base_hr = 0.038
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the configuration factor for the model.
            self.piC = self._lst_piC[self.contact_form - 1]
            self.hazard_rate_model['piC'] = self.piC

            # Set the use factor for the model.
            if self.use == 1:
                self.piU = 1.0
            else:
                self.piU = 10.0
            self.hazard_rate_model['piU'] = self.piU

            # Set the quality factor for the model.
            if self.quality == 1:           # MIL-SPEC
                self.piQ = 1.0
            else:
                self.piQ = 8.4
            self.hazard_rate_model['piQ'] = self.piQ

<<<<<<< HEAD
        return Switch.calculate(self)
=======
        return Switch.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
