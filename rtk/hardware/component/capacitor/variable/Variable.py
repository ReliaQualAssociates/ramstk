#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Capacitor.Variable Package Variable Module
#############################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.variable.Variable.py is part of the
#       RTK Project
#
# All rights reserved.

import gettext
import locale

try:
<<<<<<< HEAD
    import Configuration as _conf
    import Utilities as _util
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
=======
    import Configuration
    import Utilities
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

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


class AirTrimmer(Capacitor):
    """
    The Variable Air Trimmer capacitor data model contains the attributes and
    methods of a variable air trimmer capacitor.  The attributes of a variable
    air trimmer capacitor are:

<<<<<<< HEAD
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0
=======
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: the subcategory ID in the RTK common database.

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specification MIL-C-92.

    Hazard Rate Models:
<<<<<<< HEAD
        # MIL-HDBK-217F, section 10.18
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
        # MIL-HDBK-217FN2, section 10.18
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.5, 20.0,
            52.0, 950.0]
    _piQ = [5.0, 20.0]
    _lambdab_count = [0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1,
                      0.032, 2.5, 8.9, 100.0]
    lst_ref_temp = [358.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 57

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Variable Air Trimmer capacitor data model instance.
=======
        Method to initialize a Variable Air Trimmer capacitor data model
        instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(AirTrimmer, self).__init__()

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
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Variable Air Trimmer capacitor data
        model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Variable Air Trimmer
        capacitor data model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00000192 * ((_stress / 0.33)**3 + 1) * \
                    exp(10.8 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

<<<<<<< HEAD
        return Capacitor.calculate(self)
=======
        return Capacitor.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e


class Ceramic(Capacitor):
    """
    The Variable Ceramic capacitor data model contains the attributes and
    methods of a variable ceramic capacitor.  The attributes of a variable
    ceramic capacitor are:

<<<<<<< HEAD
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0
=======
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: the subcategory ID in the RTK common database.

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specification MIL-C-81.

    Hazard Rate Models:
<<<<<<< HEAD
        # MIL-HDBK-217F, section 10.16
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
        # MIL-HDBK-217FN2, section 10.16
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.4, 20.0,
            52.0, 950.0]
    _piQ = [4.0, 20.0]
    _lambdab_count = [0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1,
                      0.032, 1.9, 5.9, 85.0]
    lst_ref_temp = [358.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 55

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Variable Ceramic capacitor data model instance.
=======
        Method to initialize a Variable Ceramic capacitor data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Ceramic, self).__init__()

<<<<<<< HEAD
        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
=======
        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217FN2
            self.reference_temperature = 358.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Ceramic Chip capacitor data
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00224 * ((_stress / 0.17)**3 + 1) * \
                    exp(1.59 * ((self.temperature_active + 273) /
                                self.reference_temperature)**10.1)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

<<<<<<< HEAD
        return Capacitor.calculate(self)
=======
        return Capacitor.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e


class Piston(Capacitor):
    """
    The Variable Piston capacitor data model contains the attributes and
    methods of a variable piston capacitor.  The attributes of a variable
    piston capacitor are:

<<<<<<< HEAD
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0
=======
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: the subcategory ID in the RTK common database.

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specification MIL-C-14409.

    Hazard Rate Models:
<<<<<<< HEAD
        # MIL-HDBK-217F, section 10.17
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
        # MIL-HDBK-217FN2, section 10.17
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 3.0, 12.0, 7.0, 18.0, 3.0, 4.0, 20.0, 30.0, 32.0, 0.5, 18.0,
            46.0, 830.0]
    _piQ = [3.0, 10.0]
    _lambdab_count = [0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2,
                      0.16, 0.93, 3.2, 37.0]
    lst_ref_temp = [398.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 56

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Variable Piston capacitor data model instance.
=======
        Method to initialize a Variable Piston capacitor data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Piston, self).__init__()

<<<<<<< HEAD
        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 398.0

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
=======
        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217FN2
            self.reference_temperature = 398.0

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Ceramic Chip capacitor data
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00000073 * ((_stress / 0.33)**3 + 1) * \
                    exp(12.1 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

<<<<<<< HEAD
        return Capacitor.calculate(self)
=======
        return Capacitor.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e


class Vacuum(Capacitor):
    """
    The Variable Vacuum capacitor data model contains the attributes and
    methods of a variable vacuum capacitor.  The attributes of a variable
    vacuum capacitor are:

<<<<<<< HEAD
    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0
=======
    :cvar list _lst_piE: list of MIL-HDBK-217FN2 operating environment factor
                         values.
    :cvar list _lst_piQ: list of MIL-HDBK-217FN2 quality factor values.
    :cvar list _lst_lambdab_count: list of base hazard rate values for the
                                   MIL-HDBK-217FN2 parts count method.
    :cvar int subcategory: the subcategory ID in the RTK common database.

    :ivar int specification: default value: 0
    :ivar int spec_sheet: default value: 0
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specification MIL-C-23183.

    Hazard Rate Models:
<<<<<<< HEAD
        # MIL-HDBK-217F, section 10.19
    """

    # MIL-HDK-217F hazard rate calculation variables.
=======
        # MIL-HDBK-217FN2, section 10.19
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piCF = [0.10, 1.0]
    _piE = [1.0, 3.0, 14.0, 8.0, 27.0, 10.0, 18.0, 70.0, 108.0, 40.0, 0.5, 0.0,
            0.0, 0.0]
    _piQ = [3.0, 20.0]
    _lambdab_count = [0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0,
                      20.0, 0.0, 0.0, 0.0]
    lst_ref_temp = [358.0, 373.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 58

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Variable Vacuum capacitor data model instance.
=======
        Method to initialize a Variable Vacuum capacitor data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Vacuum, self).__init__()

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
        self.configuration = 1              # Fixed
        self.specification = 0
        self.spec_sheet = 0
        self.piCF = 0.0
<<<<<<< HEAD
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
=======
        if self.hazard_rate_type < 3:       # MIL-HDBK-217FN2
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            self.reference_temperature = 358.0

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Variable Vacuum capacitor data model attributes.
=======
        Method to set the Variable Vacuum capacitor data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Capacitor.set_attributes(self, values)

        try:
            self.configuration = int(values[119])
            self.piCF = float(values[104])
        except IndexError as _err:
<<<<<<< HEAD
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
=======
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
<<<<<<< HEAD
        Retrieves the current values of the Variable Vacuum capacitor data
        model attributes.
=======
        Method to retrieve the current values of the Variable Vacuum capacitor
        data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: (configuration, piCF)
        :rtype: tuple
        """

        _values = Capacitor.get_attributes(self)

        _values = _values + (self.configuration, self.piCF)

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Ceramic Chip capacitor data
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCF'
            self.piCF = self._piCF[self.configuration - 1]
            self.hazard_rate_model['piCF'] = self.piCF

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.0112 * ((_stress / 0.17)**3 + 1) * \
                    exp(1.59 * ((self.temperature_active + 273) /
                                self.reference_temperature)**10.1)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

<<<<<<< HEAD
        return Capacitor.calculate(self)
=======
        return Capacitor.calculate_part(self)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
