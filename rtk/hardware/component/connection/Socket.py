#!/usr/bin/env python
"""
<<<<<<< HEAD
#####################################################
Hardware.Component.Connection Package IC Socket Module
#####################################################
=======
######################################################
Hardware.Component.Connection Package IC Socket Module
######################################################
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.Socket.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
<<<<<<< HEAD
    import Configuration as _conf
    import Utilities as _util
    from hardware.component.connection.Connection import Model as Connection
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    from rtk.hardware.component.connection.Connection import Model as Connection
=======
    import Configuration
    import Utilities
    from hardware.component.connection.Connection import Model as Connection
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.connection.Connection import Model as \
                                                             Connection
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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


class Socket(Connection):
    """
    The Socket connection data model contains the attributes and methods of an
    IC socket connection component.  The attributes of an IC socket connection
    are:

<<<<<<< HEAD
    :cvar subcategory: default value: 8

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 15.3.
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
    :cvar int subcategory: the Connection subcategory.

    :ivar float base_hr: the MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar str reason: the reason(s) the Connection is overstressed.
    :ivar float piE: the MIL-HDBK-217FN2 operating environment factor.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 15.3.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piQ = [1.0, 2.0]
    _piE = [1.0, 3.0, 14.0, 6.0, 18.0, 8.0, 12.0, 11.0, 13.0, 25.0, 0.5, 14.0,
            36.0, 650.0]
    _lambdab_count = [0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015, 0.023, 0.021,
                      0.025, 0.048, 0.00097, 0.027, 0.070, 1.3]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 74                        # Subcategory ID in the common DB.

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a IC Socket connection data model instance.
=======
        Method to initialize a IC Socket connection data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Socket, self).__init__()

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
        self.n_active_contacts = 0
        self.piP = 0.0
        self.base_hr = 0.00042

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Multi-Pin Connection data model attributes.
=======
        Method to set the Multi-Pin Connection data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Connection.set_attributes(self, values)

        try:
            self.base_hr = 0.00042
            self.piP = float(values[100])
            self.n_active_contacts = int(values[117])
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
        Retrieves the current values of the Multi-Pin Connection data model
        attributes.
=======
        Method to retrieve the current values of the Multi-Pin Connection data
        model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: (n_active_contacts, piP)
        :rtype: tuple
        """

        _values = Connection.get_attributes(self)

        _values = _values + (self.n_active_contacts, self.piP)

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Multi-Pin Connection data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Multi-Pin Connection data
        model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Quality factor.
            self.piQ = self._piQ[self.quality - 1]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piE * piP'

            # Active pins correction factor.
            if self.n_active_contacts >= 2:
                self.piP = exp(((self.n_active_contacts - 1) / 10.0)**0.51064)
            else:
                self.piP = 0.0
            self.hazard_rate_model['piP'] = self.piP

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

<<<<<<< HEAD
        return Connection.calculate(self)
=======
        return Connection.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
