#!/usr/bin/env python
"""
#################################
Hardware Package Component Module
#################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.Component.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    from hardware.Hardware import Model as Hardware
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.Hardware import Model as Hardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(Hardware):                        # pylint: disable=R0902
    """
    The Component data model contains the attributes and methods of a hardware
    Component item.  The attributes of an Component are:

    :ivar int category_id: the ID of the component category.
    :ivar int subcategory_id: the ID of the component sub-category.
    :ivar float junction_temperature: the operating temperature of the
                                      component's junction.
    :ivar float knee_temperature: the temperature at which the component must
                                  begin being derated.
    :ivar float thermal_resistance: the junction-case or junction-ambient
                                    resistance to thermal transfer.
    :ivar float reference_temperature: the reference temperature for the
                                       component.
    """

    def __init__(self):
        """
        Method to initialize a Component data model instance.
        """

        super(Model, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.category_id = 0
        self.subcategory_id = 0
        self.junction_temperature = 0.0
        self.knee_temperature = 30.0
        self.thermal_resistance = 0.0
        self.reference_temperature = 30.0

    def set_attributes(self, values):
        """
        Method to set the Component data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Hardware.set_attributes(self, values[:86])

        if _code == 0:
            try:
                self.category_id = int(values[90])
                self.subcategory_id = int(values[91])
                self.junction_temperature = int(values[92])
                self.knee_temperature = float(values[93])
                self.thermal_resistance = float(values[94])
                self.reference_temperature = float(values[95])
            except IndexError as _err:
                _code = Utilities.error_handler(_err.args)
                _msg = _(u"ERROR: Insufficient input values.")
            except TypeError as _err:
                _code = Utilities.error_handler(_err.args)
                _msg = _(u"ERROR: Converting one or more inputs to correct "
                         u"data type.")

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Component data model
        attributes.

        :return: (category_id, subcategory_id, junction_temperature,
                  knee_temperature, thermal_resistance, reference_temperature)
        :rtype: tuple
        """

        _values = Hardware.get_attributes(self)

        _values = _values + (self.category_id, self.subcategory_id,
                             self.junction_temperature,
                             self.knee_temperature, self.thermal_resistance,
                             self.reference_temperature)

        return _values


class Component(object):
    """
    The Component data controller provides an interface between the Component
    data model and an RTK view model.  A single Component controller can manage
    one or more Component data models.  The Component data controller is
    currently unused.
    """

    def __init__(self):
        """
        Method to initialize a Component data controller instance.
        """

        pass
