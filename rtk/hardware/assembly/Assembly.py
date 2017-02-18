#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.assembly.Assembly.py is part of The RTK Project
#
# All rights reserved.

"""
################################
Hardware Package Assembly Module
################################
"""

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
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


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
    :ivar int cost_type: indicates method used to determine cost of assembly.
                         * 0 = specified
                         * 1 = calculated
    :ivar int repairable: indicates whether or not the Assembly is repairable.
    :ivar int total_part_quantity: total number of components comprising the
                                   Assembly.
    :ivar float total_power_dissipation: the total power dissipation of the
                                         Assembly.
    :ivar float detection_fr: the hazard rate of the Assembly failures that are
                              detectable.
    :ivar float detection_percent: the percentage of the total Assembly hazard
                                   rate that is detectable.
    :ivar float isolation_fr: the hazard rate of the Assembly failures that are
                              isolable.
    :ivar float isolation_percent: the percentage of the total Assembly hazard
                                   rate that is isolable.
    :ivar float percent_isolation_group_ri: the percentage of the Assembly
                                            hazard rate that is isolable to a
                                            group of components.
    :ivar float percent_isolation_single_ri: the percentage of the Assembly
                                             hazard rate that is isolable to a
                                             single component.
    """

    def __init__(self):
        """
        Method to initialize an Assembly data model instance.
        """

        super(Model, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicAssemblies = {}
        self.dicComponents = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.cost_type = 0
        self.repairable = 1
        self.total_part_quantity = 0
        self.total_power_dissipation = 0
        self.detection_fr = 0.0
        self.detection_percent = 0.0
        self.isolation_fr = 0.0
        self.isolation_percent = 0.0
        self.percent_isolation_group_ri = 0.0
        self.percent_isolation_single_ri = 0.0

    def set_attributes(self, values):
        """
        Method to set the Assembly data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Hardware.set_attributes(self, values)

        _code.append(0)
        _msg.append('')

        if sum(_code) == 0:
            try:
                self.cost_type = int(values[38])
                self.repairable = int(values[39])
                self.total_part_quantity = int(values[40])
                self.total_power_dissipation = float(values[41])
            except IndexError as _err:
                _code[3] = Utilities.error_handler(_err.args)
                _msg[3] = _(u"ERROR: Insufficient input values.")
            except TypeError as _err:
                _code[3] = Utilities.error_handler(_err.args)
                _msg[3] = _(u"ERROR: Converting one or more inputs to correct "
                            u"data type.")

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Assembly data model
        attributes.

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
    one or more Assembly data models.  The Assembly data controller is
    currently unused.
    """

    def __init__(self):
        """
        Method to initialize an Assembly data controller instance.
        """

        pass
