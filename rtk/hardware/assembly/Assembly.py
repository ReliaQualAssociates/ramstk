#!/usr/bin/env python
"""
###########################
Assembly Module Data Module
###########################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.assembly.Assembly.py is part of The RTK Project
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
    The Assembly data model contains the attributes and methods of a hardware
    Assembly item.  The attributes of an Assembly are:

    :ivar dicAssemblies: Dictionary of the Assembly data models that are
                         children of this data model.  Key is the Hardware ID;
                         value is a pointer to the Assembly data model
                         instance.
    :ivar dicComponents: Dictionary of the Component data models that are
                         children of this data model.  Key is the Hardware ID;
                         value is a pointer to the Component data model
                         instance.

    :ivar cost_type: default value: 0
    :ivar repairable: default value: 1
    :ivar total_part_quantity: default value: 0
    :ivar total_power_dissipation: default value: 0
    :ivar detection_fr: default value: 0.0
    :ivar detection_percent: default value: 0.0
    :ivar isolation_fr: default value: 0.0
    :ivar isolation_percent: default value: 0.0
    :ivar percent_isolation_group_ri: default value: 0.0
    :ivar percent_isolation_single_ri: default value: 0.0
    """

    def __init__(self):
        """
        Initialize an Assembly data model instance.
        """

        super(Model, self).__init__()

        # Initialize public disctionary attributes.
        self.dicAssemblies = {}
        self.dicComponents = {}

        # Initialize public scalar attributes.
        self.cost_type = 0
        self.repairable = 1
        self.total_part_quantity = 0
        self.total_power_dissipation = 0

        # Maintainability attributes.
        self.detection_fr = 0.0
        self.detection_percent = 0.0
        self.isolation_fr = 0.0
        self.isolation_percent = 0.0
        self.percent_isolation_group_ri = 0.0
        self.percent_isolation_single_ri = 0.0

    def set_attributes(self, values):
        """
        Sets the Assembly data model attributes.

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
                self.cost_type = int(values[86])
                self.repairable = int(values[87])
                self.total_part_quantity = int(values[88])
                self.total_power_dissipation = float(values[89])
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
                  cost_type, repairable, total_part_quantity,
                  total_power_dissipation)
        :rtype: tuple
        """

        _values = Hardware.get_attributes(self)

        _values = _values + (self.cost_type, self.repairable,
                             self.total_part_quantity,
                             self.total_power_dissipation)

        return _values


class Assembly(object):
    """
    The Assembly data controller provides an interface between the Assembly
    data model and an RTK view model.  A single Assembly controller can manage
    one or more Assembly data models.  The attributes of an Assembly data
    controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar dicHardware: Dictionary of the Assembly data models managed.
                       Key is the Hardware ID; value is a pointer to the
                       Assembly data model instance.
    """

    def __init__(self):
        """
        Initializes an Assembly data controller instance.
        """

        pass
