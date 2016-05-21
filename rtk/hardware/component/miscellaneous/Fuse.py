#!/usr/bin/env python
"""
####################################################
Hardware.Component.Miscellaneous Package Fuse Module
####################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.miscellaneous.Fuse.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import calculations as _calc
<<<<<<< HEAD
    import Configuration as _conf
    import Utilities as _util
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.calculations as _calc
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
=======
    import Configuration
    import Utilities
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.calculations as _calc
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    from rtk.hardware.component.Component import Model as Component

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


class Fuse(Component):
    """
    The Fuse data model contains the attributes and methods of a Fuse
    component.  The attributes of an Fuse are:

<<<<<<< HEAD
    :cvar category: default value: 10
    :cvar subcategory: default value: 82

    :ivar base_hr: default value: 0.0
    :ivar piE: default value: 0.0
    :ivar reason: default value: ""

    Hazard Rate Models:
        # MIL-HDBK-217F, section 22.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
    :cvar int category: the Component category.
    :cvar int subcategory: the Component subcategory.

    :ivar float base_hr: the base/generic hazard rate.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar str reason: the reason(s) the Fuse is overstressed.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 22.1.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 2.0, 8.0, 5.0, 11.0, 9.0, 12.0, 15.0, 18.0, 16.0, 0.9,
                10.0, 21.0, 230.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

<<<<<<< HEAD
    category = 10
    subcategory = 82

    def __init__(self):
        """
        Initialize an Fuse data model instance.
=======
    category = 6
    subcategory = 3

    def __init__(self):
        """
        Method to initialize an Fuse data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Fuse, self).__init__()

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
        self.base_hr = 0.01                 # Base hazard rate.
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Fuse data model attributes.
=======
        Method to set the Fuse data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.piE = float(values[96])
<<<<<<< HEAD
            # TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
=======
# TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
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
        Retrieves the current values of the Fuse data model
=======
        Method to retrieve the current values of the Fuse data model
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        attributes.

        :return: (base_hr, piE, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.base_hr, self.piE, self.reason)

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Fuse data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Fuse data model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            self.hazard_rate_model['lambdab'] = self.base_hr

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piE'

            # Set the model's base hazard rate.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        self.hazard_rate_active = _calc.calculate_part(self.hazard_rate_model)
        self.hazard_rate_active = (self.hazard_rate_active +
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
<<<<<<< HEAD
        self.hazard_rate_active = self.hazard_rate_active / _conf.FRMULT
=======
        self.hazard_rate_active = self.hazard_rate_active / \
                                  Configuration.FRMULT
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False
