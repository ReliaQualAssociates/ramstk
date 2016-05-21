#!/usr/bin/env python
"""
###################################################
Hardware.Component.Relay Package Solid State Module
###################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.relay.SolidState.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
<<<<<<< HEAD
    import Configuration as _conf
    from hardware.component.relay.Relay import Model as Relay
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
=======
    import Configuration
    from hardware.component.relay.Relay import Model as Relay
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    from rtk.hardware.component.relay.Relay import Model as Relay

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


class SolidState(Relay):
    """
    The SolidState Relay data model contains the attributes and methods of a
    SolidState Relay component.  The attributes of a SolidState Relay are:

<<<<<<< HEAD
    :cvar subcategory: default value: 65

    Hazard Rate Models:
        # MIL-HDBK-217F, section 13.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
    :cvar int subcategory: default value: 65

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 13.2.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piQ = [1.0, 4.0]
    _lst_piE = [1.0, 3.0, 12.0, 6.0, 17.0, 12.0, 19.0, 21.0, 32.0, 23.0, 0.4,
                12.0, 33.0, 590.0]
    _lst_lambdab_count = [[0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2,
                           0.16, 4.8, 13.0, 240.0],
                          [0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0,
                           12.0, 0.20, 5.0, 17.0, 300.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 65

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize an SolidState Relay data model instance.
=======
        Method to initialize an Solid State Relay data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(SolidState, self).__init__()

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Mechanical Relay data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Mechanical Relay data
        model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab_count[self.construction - 1][self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Set the base hazard rate for the model.
            if self.construction == 1:
                self.base_hr = 0.4
            else:
                self.base_hr = 0.5
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality factor for the model.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

            # Set the environment factor for the model.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

<<<<<<< HEAD
        return Relay.calculate(self)
=======
        return Relay.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
