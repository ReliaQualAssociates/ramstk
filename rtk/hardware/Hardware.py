#!/usr/bin/env python
"""
################################
Hardware Package Hardware Module
################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.Hardware.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    #from hardware.component.capacitor.Capacitor import Model as _cap
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    #from rtk.hardware.component.capacitor.Capacitor import Model as _cap

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

# TODO: Fix all docstrings; copy-paste errors.
class Model(object):                        # pylint: disable=R0902
    """
    The Hardware data model contains the attributes and methods of a Hardware
    item.  The Hardware class is a meta-class for the Assembly and Component
    classes.  A :class:`rtk.hardware.BoM` will consist of one or more Hardware
    items.  The attributes of a Hardware item are:

    :ivar revision_id: default value: None
    :ivar requirement_id: default value: None
    :ivar description: default value: ''
    :ivar code: default value: ''
    :ivar requirement_type: default value: ''
    :ivar priority: default value: 1
    :ivar specification: default value: ''
    :ivar page_number: default value: ''
    :ivar figure_number: default value: ''
    :ivar derived: default value: 0
    :ivar owner: default value: ''
    :ivar validated: default value: 0
    :ivar validated_date: default value: 719163
    :ivar parent_id: default value: -1
    """

    def __init__(self):
        """
        Initialize a Hardware data model instance.
        """

        # Initialize public list attributes.
        self.rt_inputs = []
        self.mt_inputs = []

        # Initialize public scalar attributes.
        self.revision_id = None
        self.hardware_id = None
        self.alt_part_number = ''
        self.attachments = ''
        self.cage_code = ''
        self.comp_ref_des = ''
        self.cost = 0.0
        self.cost_failure = 0.0
        self.cost_hour = 0.0
        self.description = ''
        self.duty_cycle = 100.0
        self.environment_active = 0
        self.environment_dormant = 0
        self.figure_number = ''
        self.humidity = 50.0
        self.lcn = ''
        self.level = 1
        self.manufacturer = 0
        self.mission_time = 10.0
        self.name = ''
        self.nsn = ''
        self.overstress = 0
        self.page_number = ''
        self.parent_id = 0
        self.part = 0
        self.part_number = ''
        self.quantity = 1
        self.ref_des = ''
        self.reliability_goal = 1.0
        self.reliability_goal_measure = 0
        self.remarks = ''
        self.rpm = 0.0
        self.specification_number = ''
        self.tagged_part = 0
        self.temperature_active = 30.0
        self.temperature_dormant = 30.0
        self.vibration = 0.0
        self.year_of_manufacture = 2014

        # Stress attributes.
        self.current_ratio = 1.0
        self.max_rated_temperature = 0.0
        self.min_rated_temperature = 0.0
        self.operating_current = 0.0
        self.operating_power = 0.0
        self.operating_voltage = 0.0
        self.power_ratio = 1.0
        self.rated_current = 1.0
        self.rated_power = 1.0
        self.rated_voltage = 1.0
        self.temperature_rise = 0.0
        self.voltage_ratio = 1.0

        # Reliability attributes.
        self.add_adj_factor = 0.0
        self.availability_logistics = 1.0
        self.availability_mission = 1.0
        self.avail_log_variance = 0.0
        self.avail_mis_variance = 0.0
        self.failure_dist = 0
        self.failure_parameter_1 = 0.0
        self.failure_parameter_2 = 0.0
        self.failure_parameter_3 = 0.0
        self.hazard_rate_active = 0.0
        self.hazard_rate_dormant = 0.0
        self.hazard_rate_logistics = 0.0
        self.hazard_rate_method = 1
        self.hazard_rate_mission = 0.0
        self.hazard_rate_model = {}
        self.hazard_rate_percent = 0.0
        self.hazard_rate_software = 0.0
        self.hazard_rate_specified = 0.0
        self.hazard_rate_type = 1
        self.hr_active_variance = 0.0
        self.hr_dormant_variance = 0.0
        self.hr_logistics_variance = 0.0
        self.hr_mission_variance = 0.0
        self.hr_specified_variance = 0.0
        self.mtbf_logistics = 0.0
        self.mtbf_mission = 0.0
        self.mtbf_specified = 0.0
        self.mtbf_log_variance = 0.0
        self.mtbf_miss_variance = 0.0
        self.mtbf_spec_variance = 0.0
        self.mult_adj_factor = 1.0
        self.reliability_logistics = 1.0
        self.reliability_mission = 1.0
        self.rel_log_variance = 0.0
        self.rel_miss_variance = 0.0
        self.survival_analysis = 0

        # Maintainability attributes.
        self.detection_fr = 0.0
        self.detection_percent = 0.0
        self.isolation_fr = 0.0
        self.isolation_percent = 0.0
        self.mcmt = 0.0
        self.mcmt_variance = 0.0
        self.mmt = 0.0
        self.mmt_variance = 0.0
        self.mpmt = 0.0
        self.mpmt_variance = 0.0
        self.mttr = 0.0
        self.mttr_variance = 0.0
        self.mttr_add_adj_factor = 0.0
        self.mttr_mult_adj_factor = 1.0
        self.mttr_specified = 0.0
        self.mttr_spec_variance = 0.0
        self.mttr_type = 1
        self.percent_isolation_group_ri = 0.0
        self.percent_isolation_single_ri = 0.0
        self.repair_dist = 0
        self.repair_parameter_1 = 0.0
        self.repair_parameter_2 = 0.0

    def set_attributes(self, values):
        """
        Sets the Hardware data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        (_code, _msg) = self._set_base_attributes(values[:38])
        (_code, _msg) = self._set_stress_attributes(values[38:50])
        (_code, _msg) = self._set_reliability_attributes(values[50:86])

        return(_code, _msg)

    def _set_base_attributes(self, values):
        """
        Sets the base Hardware attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.hardware_id = int(values[1])
            self.alt_part_number = str(values[2])
            self.attachments = str(values[3])
            self.cage_code = str(values[4])
            self.comp_ref_des = str(values[5])
            self.cost = float(values[6])
            self.cost_failure = float(values[7])
            self.cost_hour = float(values[8])
            self.description = str(values[9])
            self.duty_cycle = float(values[10])
            self.environment_active = int(values[11])
            self.environment_dormant = int(values[12])
            self.figure_number = str(values[13])
            self.humidity = float(values[14])
            self.lcn = str(values[15])
            self.level = int(values[16])
            self.manufacturer = int(values[17])
            self.mission_time = float(values[18])
            self.name = str(values[19])
            self.nsn = str(values[20])
            self.overstress = int(values[21])
            self.page_number = str(values[22])
            self.parent_id = int(values[23])
            self.part = int(values[24])
            self.part_number = str(values[25])
            self.quantity = int(values[26])
            self.ref_des = str(values[27])
            self.reliability_goal = float(values[28])
            self.reliability_goal_measure = int(values[29])
            self.remarks = str(values[30])
            self.rpm = float(values[31])
            self.specification_number = str(values[32])
            self.tagged_part = int(values[33])
            self.temperature_active = float(values[34])
            self.temperature_dormant = float(values[35])
            self.vibration = float(values[36])
            self.year_of_manufacture = int(values[37])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def _set_stress_attributes(self, values):
        """
        Sets the stres-specific Hardware attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.current_ratio = float(values[0])
            self.max_rated_temperature = float(values[1])
            self.min_rated_temperature = float(values[2])
            self.operating_current = float(values[3])
            self.operating_power = float(values[4])
            self.operating_voltage = float(values[5])
            self.power_ratio = float(values[6])
            self.rated_current = float(values[7])
            self.rated_power = float(values[8])
            self.rated_voltage = float(values[9])
            self.temperature_rise = float(values[10])
            self.voltage_ratio = float(values[11])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def _set_reliability_attributes(self, values):
        """
        Sets the reliability-specific Hardware attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.add_adj_factor = float(values[0])
            self.availability_logistics = float(values[1])
            self.availability_mission = float(values[2])
            self.avail_log_variance = float(values[3])
            self.avail_mis_variance = float(values[4])
            self.failure_dist = int(values[5])
            self.failure_parameter_1 = float(values[6])
            self.failure_parameter_2 = float(values[7])
            self.failure_parameter_3 = float(values[8])
            self.hazard_rate_active = float(values[9])
            self.hazard_rate_dormant = float(values[10])
            self.hazard_rate_logistics = float(values[11])
            self.hazard_rate_method = int(values[12])
            self.hazard_rate_mission = float(values[13])
            self.hazard_rate_model = str(values[14])
            self.hazard_rate_percent = float(values[15])
            self.hazard_rate_software = float(values[16])
            self.hazard_rate_specified = float(values[17])
            self.hazard_rate_type = int(values[18])
            self.hr_active_variance = float(values[19])
            self.hr_dormant_variance = float(values[20])
            self.hr_logistics_variance = float(values[21])
            self.hr_mission_variance = float(values[22])
            self.hr_specified_variance = float(values[23])
            self.mtbf_logistics = float(values[24])
            self.mtbf_mission = float(values[25])
            self.mtbf_specified = float(values[26])
            self.mtbf_log_variance = float(values[27])
            self.mtbf_miss_variance = float(values[28])
            self.mtbf_spec_variance = float(values[29])
            self.mult_adj_factor = float(values[30])
            self.reliability_logistics = float(values[31])
            self.reliability_mission = float(values[32])
            self.rel_log_variance = float(values[33])
            self.rel_miss_variance = float(values[34])
            self.survival_analysis = int(values[35])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Hardware data model attributes.

        :return: (revision_id, hardware_id, alt_part_number, attachments,
                  cage_code, comp_ref_des, cost, cost_failure, cost_hour,
                  cost_type, description, duty_cycle, environment_active,
                  environment_dormant, figure_number, humidity, lcn, level,
                  manufacturer, mission_time, name, nsn, page_number,
                  parent_id, part, part_number, quantity, ref_des,
                  reliability_goal, reliability_goal_measure, remarks,
                  repairable, rpm, specification_number, temperature_active,
                  temperature_dormant, vibration, year_of_manufacture)
        :rtype: tuple
        """

        _base_values = self._get_base_attributes()
        _stress_values = self._get_stress_attributes()
        _rel_values = self._get_reliability_attributes()

        _values = _base_values + _stress_values + _rel_values

        return _values

    def _get_base_attributes(self):
        """
        Retrieves the current values of the Hardware data model base
        attributes.

        :return: (revision_id, hardware_id, alt_part_number, attachments,
                  cage_code, comp_ref_des, cost, cost_failure, cost_hour,
                  description, duty_cycle, environment_active,
                  environment_dormant, figure_number, humidity, lcn, level,
                  manufacturer, mission_time, name, nsn, overstress,
                  page_number, parent_id, part, part_number, quantity, ref_des,
                  reliability_goal, reliability_goal_measure, remarks, rpm,
                  specification_number, tagged_part, temperature_active,
                  temperature_dormant, vibration, year_of_manufacture)
        :rtype: tuple
        """

        _values = (self.revision_id, self.hardware_id, self.alt_part_number,
                   self.attachments, self.cage_code, self.comp_ref_des,
                   self.cost, self.cost_failure, self.cost_hour,
                   self.description, self.duty_cycle, self.environment_active,
                   self.environment_dormant, self.figure_number, self.humidity,
                   self.lcn, self.level, self.manufacturer, self.mission_time,
                   self.name, self.nsn, self.overstress, self.page_number,
                   self.parent_id, self.part, self.part_number, self.quantity,
                   self.ref_des, self.reliability_goal,
                   self.reliability_goal_measure, self.remarks, self.rpm,
                   self.specification_number, self.tagged_part,
                   self.temperature_active, self.temperature_dormant,
                   self.vibration, self.year_of_manufacture)

        return _values

    def _get_stress_attributes(self):
        """
        Retrieves the current values of the Hardware data model stress
        attributes.

        :return: (current_ratio, max_rated_temperature, min_rated_temperature,
                  operating_current, operating_power, operating_voltage,
                  power_ratio, rated_current, rated_power, rated_voltage,
                  temperature_rise, voltage_ratio)
        :rtype: tuple
        """

        _values = (self.current_ratio, self.max_rated_temperature,
                   self.min_rated_temperature, self.operating_current,
                   self.operating_power, self.operating_voltage,
                   self.power_ratio, self.rated_current, self.rated_power,
                   self.rated_voltage, self.temperature_rise,
                   self.voltage_ratio)

        return _values

    def _get_reliability_attributes(self):
        """
        Retrieves the current values of the Hardware data model reliability
        attributes.

        :return: (add_adj_factor, availability_logistics, availability_mission,
                  avail_log_variance, avail_mis_variance, failure_dist,
                  failure_parameter_1, failure_parameter_2,
                  failure_parameter_3, hazard_rate_active, hazard_rate_dormant,
                  hazard_rate_logistics, hazard_rate_method,
                  hazard_rate_mission, hazard_rate_model, hazard_rate_percent,
                  hazard_rate_software, hazard_rate_specified,
                  hazard_rate_type, hr_active_variance, hr_dormant_variance,
                  hr_logistics_variance, hr_mission_variance,
                  hr_specified_variance, mtbf_logistics, mtbf_mission,
                  mtbf_specified, mtbf_log_variance, mtbf_miss_variance,
                  mtbf_spec_variance, mult_adj_factor, reliability_logistics,
                  reliability_mission, rel_log_variance, rel_miss_variance,
                  survival_analysis)
        :rtype: tuple
        """

        _values = (self.add_adj_factor, self.availability_logistics,
                   self.availability_mission, self.avail_log_variance,
                   self.avail_mis_variance, self.failure_dist,
                   self.failure_parameter_1, self.failure_parameter_2,
                   self.failure_parameter_3, self.hazard_rate_active,
                   self.hazard_rate_dormant, self.hazard_rate_logistics,
                   self.hazard_rate_method, self.hazard_rate_mission,
                   self.hazard_rate_model, self.hazard_rate_percent,
                   self.hazard_rate_software, self.hazard_rate_specified,
                   self.hazard_rate_type, self.hr_active_variance,
                   self.hr_dormant_variance, self.hr_logistics_variance,
                   self.hr_mission_variance, self.hr_specified_variance,
                   self.mtbf_logistics, self.mtbf_mission, self.mtbf_specified,
                   self.mtbf_log_variance, self.mtbf_miss_variance,
                   self.mtbf_spec_variance, self.mult_adj_factor,
                   self.reliability_logistics, self.reliability_mission,
                   self.rel_log_variance, self.rel_miss_variance,
                   self.survival_analysis)

        return _values

    def calculate_hardware(self):
        """
        Calculates various hardware attributes.
        """

        self._calculate_cost()

        return False

    def _calculate_cost(self):
        """
        Calculates costs associated with the hardware.
        """

        try:
            self.cost_failure = self.cost / \
                (self.hazard_rate_logistics * self.mission_time)
        except ZeroDivisionError:
            # TODO: Handle errors.
            pass

        try:
            self.cost_hour = self.cost / self.mission_time
        except ZeroDivisionError:
            # TODO: Handle errors.
            pass

        return False

    def _calculate_stress(self):
        """
        Calculates various hardware stresses.
        """

        pass

    def _calculate_reliability(self):
        """
        Calulates various hardware reliability metrics.
        """

        pass


class Hardware(object):
    """
    The Hardware data controller provides an interface between the Hardware
    data model and an RTK view model.  A single Hardware controller can manage
    one or more Hardware data models.  The attributes of a Hardware data
    controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar _last_id: the last Hardware ID used.
    :ivar dicHardware: Dictionary of the Hardware data models managed.
                       Key is the Hardware ID; value is a pointer to the
                       Hardware data model instance.
    """

    def __init__(self):
        """
        Initializes an Hardware data controller instance.
        """

        pass
