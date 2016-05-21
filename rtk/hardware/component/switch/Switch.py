#!/usr/bin/env python
"""
###############################################
Hardware.Component.Switch Package Switch Module
###############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Switch.py is part of the RTK Project
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


class Model(Component):
    """
    The Switch data model contains the attributes and methods of a Switch
    component.  The attributes of a Switch are:

<<<<<<< HEAD
    :cvar lst_derate_criteria: default value: [[0.75, 0.75, 0.0],
                                               [0.9, 0.9, 0.0]]
    :cvar category: default value: 7

    :ivar quality: default value: 0
    :ivar q_override: default value: 0.0
    :ivar base_hr: default value: 0.0
    :ivar piE: default value: 0.0
    :ivar reason: default value: ""
=======
    :cvar list lst_derate_criteria: default value: [[0.75, 0.75, 0.0],
                                                    [0.9, 0.9, 0.0]]
    :cvar int category: default value: 7

    :ivar int quality: the MIL-HDBK-217FN2 quality index.
    :ivar float q_override: the user-defined quality factor.
    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.
    :ivar str reason: the reason(s) the switch is overstressed.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Hazard Rate Models:
        # MIL-HDBK-217F, section 14.
    """

<<<<<<< HEAD
    # Initialize class attributes.
=======
    # Define class attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    lst_derate_criteria = [[0.75, 0.75, 0.0], [0.9, 0.9, 0.0]]

    category = 7

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize an Switch data model instance.
=======
        Method to initialize a Switch data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Model, self).__init__()

        # Initialize public scalar attributes.
        self.quality = 0                    # Quality level.
        self.q_override = 0.0               # User-defined piQ.
        self.base_hr = 0.0                  # Base hazard rate.
        self.piQ = 0.0
        self.piE = 0.0                      # Environment pi factor.
        self.reason = ""                    # Overstress reason.

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Switch data model attributes.
=======
        Method to set the Switch data model attributes.
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
            self.quality = int(values[116])
            self.q_override = float(values[96])
            self.base_hr = float(values[97])
            self.piE = float(values[98])
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
        Retrieves the current values of the Switch data model attributes.
=======
        Method to retrieve the current values of the Switch data model
        attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: (quality, q_override, base_hr, piE, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.quality, self.q_override, self.base_hr,
                             self.piE, self.reason)

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Switch data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Switch data model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab_count[self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ_count[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

        elif self.hazard_rate_type == 2:
            # Set the environment pi factor for the model.
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

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False

    def _overstressed(self):
        """
<<<<<<< HEAD
        Determines whether the Switch is overstressed based on it's rated
        values and operating environment.
=======
        Method to determine whether the Switch is overstressed based on it's
        rated values and operating environment.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
<<<<<<< HEAD
=======
        _reason = ''
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if _harsh:
            if self.operating_current > 0.75 * self.rated_current:
                self.overstress = True
<<<<<<< HEAD
                self.reason = self.reason + str(_reason_num) + \
                              ". Operating current > 75% rated current.\n"
=======
                _reason = _reason + str(_reason_num) + \
                          ". Operating current > 75% rated current.\n"
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
                _reason_num += 1
        else:
            if self.operating_current > 0.90 * self.rated_current:
                self.overstress = True
<<<<<<< HEAD
                self.reason = self.reason + str(_reason_num) + \
                              ". Operating current > 90% rated current.\n"
                _reason_num += 1

=======
                _reason = _reason + str(_reason_num) + \
                          ". Operating current > 90% rated current.\n"
                _reason_num += 1

        self.reason = _reason

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        return False
