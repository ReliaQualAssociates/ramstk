#!/usr/bin/env python
"""
############################
Component Module Data Module
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

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
    import configuration as _conf
    from hardware.Hardware import Model as Hardware
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    from rtk.hardware.Hardware import Model as Hardware

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(Hardware):                        # pylint: disable=R0902
    """
    The Component data model contains the attributes and methods of a hardware
    Component item.  The attributes of an Component are:

    :ivar category_id: default value: 0
    :ivar subcategory_id: default value: 1
    :ivar junction_temperature: default value: 0.0
    :ivar knee_temperature: default value: 0.0
    :ivar thermal_resistance: default value: 0.0
    :ivar reference_temperature: default value: 0.0
    """

    def __init__(self):
        """
        Initialize an Component data model instance.
        """

        super(Model, self).__init__()

        # Initialize public disctionary attributes.
        self.dicAssemblies = {}
        self.dicComponents = {}

        # Initialize public scalar attributes.
        self.category_id = 0
        self.subcategory_id = 0
        self.junction_temperature = 0.0
        self.knee_temperature = 30.0
        self.thermal_resistance = 0.0
        self.reference_temperature = 30.0

    def set_attributes(self, values):
        """
        Sets the Component data model attributes.

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
                self.category_id = int(values[86])
                self.subcategory_id = int(values[87])
                self.junction_temperature = int(values[88])
                self.knee_temperature = float(values[89])
                self.thermal_resistance = float(values[90])
                self.reference_temperature = float(values[91])
            except IndexError as _err:
                _code = _error_handler(_err.args)
                _msg = "ERROR: Insufficient input values."
            except TypeError as _err:
                _code = _error_handler(_err.args)
                _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Assembly data model attributes.

        :return: (revision_id, hardware_id, alt_part_number, attachments,
                  cage_code, comp_ref_des, cost, cost_failure, cost_hour,
                  cost_type, description, duty_cycle, environment_active,
                  environment_dormant, figure_number, humidity, lcn, level,
                  manufacturer, mission_time, name, nsn, page_number,
                  parent_id, part, part_number, quantity, ref_des,
                  reliability_goal, reliability_goal_measure, remarks,
                  repairable, rpm, specification_number, temperature_active,
                  temperature_dormant, vibration, year_of_manufacture,
                  category_id, subcategory_id, junction_temperature,
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
    one or more Component data models.  The attributes of an Component data
    controller are:
    """

    def __init__(self):
        """
        Initializes an Component data controller instance.
        """

        pass
