#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.Hardware.py is part of The RTK Project
#
# All rights reserved.

"""
################################
Hardware Package Hardware Module
################################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):                        # pylint: disable=R0902
    """
    The Hardware data model contains the attributes and methods of a Hardware
    item.  The Hardware class is a meta-class for the Assembly and Component
    classes.  A :py:class:`rtk.hardware.BoM.BoM` will consist of one or more
    Hardware items.  The attributes of a Hardware item are:

    :ivar int revision_id: the Revision ID the Hardware item is associated
                           with.
    :ivar int hardware_id: the ID in the RTK Project database of the Hardware
                           item.
    :ivar str alt_part_number: the alternative part number.
    :ivar str attachments: the URL of any attachments.
    :ivar str cage_code: the CAGE Code of the Hardware item.
    :ivar str comp_ref_des: the composite reference designator.
    :ivar float cost: the cost of the Hardware item.
    :ivar float cost_failure: the operating cost per failure.
    :ivar float cost_hour: the operating cost per mission hour.
    :ivar str description: the noun description of the Hardware item.
    :ivar float duty_cycle: the duty cycle.
    :ivar int environment_active: the index of the active ambient environment.
    :ivar int environment_dormant: the index of the dormant ambient evironment.
    :ivar str figure_number: the figure number in the applicable specification.
    :ivar float humidity: the operating ambient humidity.
    :ivar str lcn: the Logistics Control Number of the Hardware item.
    :ivar int level: the indenture level of the Hardware item.
    :ivar int manufacturer: the index of the manufacturer.
    :ivar float mission_time: the mission time of the Hardware item.
    :ivar str name: the noun name of the Hardware item.
    :ivar str nsn: the National Stock Number of the Hardware item.
    :ivar int overstress: indicates whether the Hardware item is overstressed.
    :ivar str page_number: the page number in the applicable specification.
    :ivar int parent_id: the Hardware ID of the parent Hardware item.
    :ivar int part: indicates whether the Hardware item is an Assembly (0) or
                    a Component (1).
    :ivar str part_number: the part number of the Hardware item.
    :ivar int quantity: the quantity of the Hardware item in the design.
    :ivar str ref_des: the reference designator of the Hardware item.
    :ivar float reliability_goal: the reliability goal for the Hardware item.
    :ivar int reliability_goal_measure: the measurement method of the
                                        reliability goal.
    :ivar str remarks: any associated user remarks.
    :ivar float rpm: the operating revolutions per minute.
    :ivar str specification_number: the applicable specification.
    :ivar int tagged_part: indicator for user-defined use.
    :ivar float temperature_active: the active operating ambient temperature.
    :ivar float temperature_dormant: the dormant ambient temperature.
    :ivar float vibration: the operating vibration level.
    :ivar int year_of_manufacture: the year the Hardware item was manufactured.
    :ivar float current_ratio: the ratio of operating current to rated current.
    :ivar float max_rated_temperature: the maximum rated temperature.
    :ivar float min_rated_temperature: the minimum rated temperature.
    :ivar float operating_current: the operating current.
    :ivar float operating_power: the operating power.
    :ivar float operating_voltage: the operating voltage.
    :ivar float power_ratio: the ratio of opertaing power to rated power.
    :ivar float rated_current: the rated current.
    :ivar float rated_power: the rated power.
    :ivar float rated_voltage: the rated voltage.
    :ivar float temperature_rise: the temperature rise of the Hardware item.
    :ivar float voltage_ratio: the ratio of operating voltage to rated voltage.
    :ivar float add_adj_factor: the hazard rate additive adjustment factor.
    :ivar float availability_logistics: the logistics availability.
    :ivar float availability_mission: the mission availability.
    :ivar float avail_log_variance: the variance of the logistics availability.
    :ivar float avail_mis_variance: the variance of the mission availability.
    :ivar int failure_dist: the index of the statistical distribution for the
                            hazard rate.
    :ivar float failure_parameter_1: the hazard rate distribution scale
                                     parameter.
    :ivar float failure_parameter_2: the hazard rate distribution shape
                                     parameter.
    :ivar float failure_parameter_3: the hazard rate distribution location
                                     parameter.
    :ivar float hazard_rate_active: the active hazard rate.
    :ivar float hazard_rate_dormant: the dormant hazard rate.
    :ivar float hazard_rate_logistics: the logistics hazard rate.
    :ivar int hazard_rate_method: the method of assessing the hazard rate.
    :ivar float hazard_rate_mission: the mission hazard rate.
    :ivar int hazard_rate_model: the statistical hazard rate model.
    :ivar float hazard_rate_percent: the percent of the system hazard rate
                                     coming from the Hardware item.
    :ivar float hazard_rate_software: the hazard rate of any software
                                      associated with the Hardware.
    :ivar float hazard_rate_specified: the specified hazard rate.
    :ivar int hazard_rate_type: the type of hazard rate assessment.
    :ivar float hr_active_variance: the variance of the active hazard rate.
    :ivar float hr_dormant_variance: the variance of the dormant hazard rate.
    :ivar float hr_logistics_variance: the variance of the logistics hazard
                                       rate.
    :ivar float hr_mission_variance: the variance of the mission hazard rate.
    :ivar float hr_specified_variance: the variance of the specified hazard
                                       rate.
    :ivar float mtbf_logistics: the logistice mean time between failure (MTBF).
    :ivar float mtbf_mission: the mission MTBF.
    :ivar float mtbf_specified: the specified MTBF.
    :ivar float mtbf_log_variance: the variance of the logistics MTBF.
    :ivar float mtbf_miss_variance: the variance of the mission MTBF.
    :ivar float mtbf_spec_variance: the variance of the specified MTBF.
    :ivar float mult_adj_factor: the hazard rate multiplicative adjustment
                                 factor.
    :ivar float reliability_logistics: the calculated logistics reliability.
    :ivar float reliability_mission: the calculated mission reliability.
    :ivar float rel_log_variance: the variance of the logistics reliability.
    :ivar float rel_miss_variance: the variance of the mission reliability.
    :ivar int survival_analysis: the index of the survival analysis applicable
                                 to the Hardware.
    :ivar float detection_fr:
    :ivar float detection_percent:
    :ivar float isolation_fr:
    :ivar float isolation_percent:
    :ivar float mcmt: the calculated mean corrective maintenance time (MCMT).
    :ivar float mcmt_variance: the variance of the MCMT.
    :ivar float mmt: the calculated mean maintenance time (MMT).
    :ivar float mmt_variance: the variance of the MMT.
    :ivar float mpmt: the calculated mean preventive maintenance time (MPMT).
    :ivar float mpmt_variance: the variance of the MPMT.
    :ivar float mttr: the calculated mean time to repair (MTTR).
    :ivar float mttr_variance: the variance of the calculate MTTR.
    :ivar float mttr_add_adj_factor: the MTTR additive adjustment factor.
    :ivar float mttr_mult_adj_factor: the MTTR multiplicative adjustment
                                      factor.
    :ivar float mttr_specified: the specified MTTR.
    :ivar float mttr_spec_variance: the variance of the specified MTTR.
    :ivar int mttr_type: the MTTR assessment type (specified or calculated).
    :ivar float percent_isolation_group_ri:
    :ivar float percent_isolation_single_ri:
    :ivar int repair_dist: the statistical repair distribution.
    :ivar float repair_parameter_1: the repair distribution scale parameter.
    :ivar float repair_parameter_2: the repair distribution shape parameter.
    """

    def __init__(self):
        """
        Method to initialize a Hardware data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.
        self.user_float = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.user_int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.user_varchar = ['', '', '', '', '']
        
        # Define public scalar attributes.
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
        self.reason = ''

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
        Method to set the Hardware data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        (_code, _msg) = self._set_base_attributes(values[:38])
        (_code, _msg) = self._set_stress_attributes(values[38:50])
        (_code, _msg) = self._set_reliability_attributes(values[50:86])
        (_code, _msg) = self._set_user_attributes(values[86:])

        return(_code, _msg)

    def _set_base_attributes(self, values):
        """
        Method to set the base Hardware attributes.

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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def _set_stress_attributes(self, values):
        """
        Method to set the stress-specific Hardware attributes.

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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def _set_reliability_attributes(self, values):
        """
        Method to set the reliability-specific Hardware attributes.

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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def _set_user_attributes(self,  values):
        """
        Method to set the user-defined Hardware attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''
        
        try:
            self.user_float[0] = float(values[0])
            self.user_float[1] = float(values[1])
            self.user_float[2] = float(values[2])
            self.user_float[3] = float(values[3])
            self.user_float[4] = float(values[4])
            self.user_float[5] = float(values[5])
            self.user_float[6] = float(values[6])
            self.user_float[7] = float(values[7])
            self.user_float[8] = float(values[8])
            self.user_float[9] = float(values[9])
            self.user_float[10] = float(values[10])
            self.user_float[11] = float(values[11])
            self.user_float[12] = float(values[12])
            self.user_float[13] = float(values[13])
            self.user_float[14] = float(values[14])
            self.user_float[15] = float(values[15])
            self.user_float[16] = float(values[16])
            self.user_float[17] = float(values[17])
            self.user_float[18] = float(values[18])
            self.user_float[19] = float(values[19])
            self.user_int[0] = int(values[20])
            self.user_int[1] = int(values[21])
            self.user_int[2] = int(values[22])
            self.user_int[3] = int(values[23])
            self.user_int[4] = int(values[24])
            self.user_int[5] = int(values[25])
            self.user_int[6] = int(values[26])
            self.user_int[7] = int(values[27])
            self.user_int[8] = int(values[28])
            self.user_int[9] = int(values[29])
            self.user_varchar[0] = str(values[30])
            self.user_varchar[1] = str(values[31])
            self.user_varchar[2] = str(values[32])
            self.user_varchar[3] = str(values[33])
            self.user_varchar[4] = str(values[34])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Hardware data model
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
                  current_ratio, max_rated_temperature, min_rated_temperature,
                  operating_current, operating_power, operating_voltage,
                  power_ratio, rated_current, rated_power, rated_voltage,
                  temperature_rise, voltage_ratio, add_adj_factor,
                  availability_logistics, availability_mission,
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

        _base_values = self._get_base_attributes()
        _stress_values = self._get_stress_attributes()
        _rel_values = self._get_reliability_attributes()
        _user_values = self._get_user_attributes()

        _values = _base_values + _stress_values + _rel_values + _user_values
        
        return _values

    def _get_base_attributes(self):
        """
        Method to retrieve the current values of the Hardware data model base
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
        Method to retrieve the current values of the Hardware data model stress
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
        Method to retrieves the current values of the Hardware data model
        reliability attributes.

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

    def _get_user_attributes(self):
        """
        Method to retrieve the current values of the Hardware data model user-defined
        attributes.

        :return: (user_float, user_int, user_varchar)
        :rtype: tuple
        """

        _values = (self.user_float, self.user_int, self.user_varchar)

        return _values

    def calculate(self, assembly):
        """
        Method to iterively calculate various hardware attributes.

        :param assembly: the :py:class:`rtk.hardware.Assembly.Model` data model
                         to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        
        assembly.hazard_rate_active = 0.0
        assembly.hazard_rate_dormant = 0.0
        assembly.hazard_rate_software = 0.0
        assembly.cost = 0.0
        assembly.total_part_quantity = 0
        assembly.total_power_dissipation = 0.0

        # First we calculate all the components that are direct children of the
        # current assembly.
        if assembly.part == 0:
            try:
                _components = assembly.dicComponents[assembly.hardware_id]
            except KeyError:
                _components = []
        elif assembly.part == 1:
            _components = [assembly]

        for _component in _components:
            if _component.hazard_rate_method == 1:      # Assessed
                try:
                    _component.calculate_part()
                except AttributeError:
                    # FIXME: Handle AttributeError in calculate.
                    print "Could not calculate {0:s}".format(_component.name)

            elif _component.hazard_rate_method == 2:    # Specified, h(t)
                _component.hazard_rate_active = assembly.hazard_rate_specified
            elif _component.hazard_rate_method == 3:    # Specified, MTBF
                _component.hazard_rate_active = 1.0 / _component.mtbf_specified

            # Calculate the dormant hazard rate.
            self._dormant_hazard_rate(_component)

            # Calculate component derived results.
            self._calculate_reliability(_component)
            self._calculate_costs(_component)

            # Update parent assembly hazard rates and costs.
            assembly.hazard_rate_active += _component.hazard_rate_active
            assembly.hazard_rate_dormant += _component.hazard_rate_dormant
            assembly.hazard_rate_software += _component.hazard_rate_software
            assembly.cost += _component.cost * _component.quantity
            assembly.total_part_quantity += _component.quantity
            assembly.total_power_dissipation += (_component.operating_power *
                                                 _component.quantity)

        # Then we calculate all the assemblies that are direct children of the
        # current assembly.
        try:
            _assemblies = assembly.dicAssemblies[assembly.hardware_id]
        except(KeyError, AttributeError):
            _assemblies = []

        for _assembly in _assemblies:
            if _assembly.hazard_rate_method == 1:       # Assessed
                self.calculate(_assembly)
            elif _assembly.hazard_rate_method == 2:     # Specified, h(t)
                _assembly.hazard_rate_active = _assembly.hazard_rate_specified
            elif _assembly.hazard_rate_method == 3:     # Specified, MTBF
                _assembly.hazard_rate_active = 1.0 / _assembly.mtbf_specified

            # Adjust the active hazard rate.
            _assembly.hazard_rate_active = (_assembly.hazard_rate_active +
                                            _assembly.add_adj_factor) * \
                                           (_assembly.duty_cycle / 100.0) * \
                                           _assembly.mult_adj_factor * \
                                           _assembly.quantity

            # Calculate assembly derived results.
            self._calculate_reliability(_assembly)
            self._calculate_costs(_assembly)

            # Update parent assembly hazard rates and costs.
            assembly.hazard_rate_active += _assembly.hazard_rate_active
            assembly.hazard_rate_dormant += _assembly.hazard_rate_dormant
            assembly.hazard_rate_software += _assembly.hazard_rate_software
            assembly.cost += _assembly.cost
            assembly.total_part_quantity += _assembly.total_part_quantity
            assembly.total_power_dissipation += _assembly.total_power_dissipation

        # Calculate parent assembly derived results.
        self._calculate_reliability(assembly)
        self._calculate_costs(assembly)

        return False

    def _calculate_reliability(self, hardware):     # pylint: disable=R0201
        """
        Method to calculate reliability metrics for a hardware item.

        :param :class: `rtk.hardware.Hardware` hardware: the rtk.Hardware()
                                                         data model to
                                                         calculate costs
                                                         metrics for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        # Calculate the logistics hazard rate.
        hardware.hazard_rate_logistics = hardware.hazard_rate_active + \
                                         hardware.hazard_rate_dormant + \
                                         hardware.hazard_rate_software

        try:
            hardware.mtbf_logistics = 1.0 / hardware.hazard_rate_logistics
        except ZeroDivisionError:
            hardware.mtbf_logistics = 0.0

        hardware.reliability_logistics = exp(-1.0 *
                                             hardware.hazard_rate_logistics *
                                             hardware.mission_time)

        # Calculate logistics hazard rate variances.
        # hardware.hr_active_variance = 1.0 / \
        #                               (hardware.hazard_rate_active**2.0)
        # hardware.hr_dormant_variance = 1.0 / \
        #                                (hardware.hazard_rate_dormant**2.0)
        # hardware.hr_specified_variance = 1.0 / \
        #                                  (hardware.hazard_rate_specified**2.0)

        # Calculate the mission hazard rate.
        # FIXME: Add attributes to allow mission (redundancy) calculations.
        hardware.hazard_rate_mission = hardware.hazard_rate_logistics
        hardware.reliability_mission = hardware.reliability_logistics

        return False

    def _calculate_costs(self, hardware):   # pylint: disable=R0201
        """
        Method to calculate cost metrics for a hardware item.

        :param `rtk.hardware.Hardware` hardware: the rtk.Hardware() data model
                                                 to calculate costs metrics
                                                 for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Calculate O & M cost metrics.
        try:
            hardware.cost_failure = hardware.cost / \
                (hardware.hazard_rate_logistics * hardware.mission_time)
        except ZeroDivisionError:
            # TODO: Handle errors.
            pass

        try:
            hardware.cost_hour = hardware.cost / hardware.mission_time
        except ZeroDivisionError:
            # TODO: Handle errors.
            pass

        return False

    def _dormant_hazard_rate(self, component):
        """
        Method to calculate the dormant hazard rate based on active
        environment, dormant environment, and component category.

        All conversion factors come from Reliability Toolkit: Commercial
        Practices Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below).

        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Component   |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
        | Category    |Active |Active  |Active  |Active |Active |Active |Active |
        |             |to     |to      |to      |to     |to     |to     |to     |
        |             |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
        |             |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
        +=============+=======+========+========+=======+=======+=======+=======+
        | Integrated  | 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
        | Circuits    |       |        |        |       |       |       |       |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Diodes      | 0.04  |  0.05  |  0.01  | 0.04  | 0.03  | 0.20  | 0.80  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Transistors | 0.05  |  0.06  |  0.02  | 0.05  | 0.03  | 0.20  | 1.00  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Capacitors  | 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Resistors   | 0.20  |  0.06  |  0.03  | 0.10  | 0.06  | 0.50  | 1.00  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Switches    | 0.40  |  0.20  |  0.10  | 0.40  | 0.20  | 0.80  | 1.00  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Relays      | 0.20  |  0.20  |  0.04  | 0.30  | 0.08  | 0.40  | 0.90  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Connectors  | 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Circuit     | 0.04  |  0.02  |  0.01  | 0.03  | 0.01  | 0.08  | 0.20  |
        | Boards      |       |        |        |       |       |       |       |
        +-------------+-------+--------+--------+-------+-------+-------+-------+
        | Transformers| 0.20  |  0.20  |  0.20  | 0.30  | 0.30  | 0.50  | 1.00  |
        +-------------+-------+--------+--------+-------+-------+-------+-------+

        :param :class: `rtk.hardware.Component` component: the rtk.Component() data
                                                           model to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        factor = [[0.08, 0.06, 0.04, 0.06, 0.05, 0.10, 0.30, 0.00],
                  [0.04, 0.05, 0.01, 0.04, 0.03, 0.20, 0.80, 0.00],
                  [0.05, 0.06, 0.02, 0.05, 0.03, 0.20, 1.00, 0.00],
                  [0.10, 0.10, 0.03, 0.10, 0.04, 0.20, 0.40, 0.00],
                  [0.20, 0.06, 0.03, 0.10, 0.06, 0.50, 1.00, 0.00],
                  [0.40, 0.20, 0.10, 0.40, 0.20, 0.80, 1.00, 0.00],
                  [0.20, 0.20, 0.04, 0.30, 0.08, 0.40, 0.90, 0.00],
                  [0.005, 0.005, 0.003, 0.008, 0.003, 0.02, 0.03, 0.00],
                  [0.04, 0.02, 0.01, 0.03, 0.01, 0.08, 0.20, 0.00],
                  [0.20, 0.20, 0.20, 0.30, 0.30, 0.50, 1.00, 0.00]]

        # First find the component category/subcategory index.
        if component.category_id == 1:                       # Capacitor
            c_index = 3
        elif component.category_id == 2:                     # Connection
            c_index = 7
        elif component.category_id == 3:                     # Inductive Device.
            if component.subcategory_id > 1:                 # Transformer
                c_index = 9
        elif component.category_id == 4:                     # Integrated Circuit
            c_index = 0
        elif component.category_id == 7:                     # Relay
            c_index = 6
        elif component.category_id == 8:                     # Resistor
            c_index = 4
        elif component.category_id == 9:                     # Semiconductor
            if component.subcategory_id > 0 and \
               component.subcategory_id < 7:                 # Diode
                c_index = 1
            elif component.subcategory_id > 6 and \
                 component.subcategory_id < 14:     # Transistor
                c_index = 2
        elif component.category_id == 10:           # Switching Device
            c_index = 5

        # Now find the appropriate active to passive environment index.
        if component.environment_active > 0 and \
           component.environment_active < 4:        # Ground
            if component.environment_dormant == 1:  # Ground
                e_index = 0
            else:
                e_index = 7
        elif component.environment_active > 3 and \
             component.environment_active < 6:      # Naval
            if component.environment_dormant == 1:  # Ground
                e_index = 4
            elif component.environment_dormant == 2:    # Naval
                e_index = 3
            else:
                e_index = 7
        elif component.environment_active > 5 and \
             component.environment_active < 11:     # Airborne
            if component.environment_dormant == 1:  # Ground
                e_index = 2
            elif component.environment_dormant == 3:    # Airborne
                e_index = 1
            else:
                e_index = 7
        elif component.environment_active == 11:    # Space
            if component.environment_dormant == 1:  # Ground
                e_index = 6
            elif component.environment_dormant == 4:    # Space
                e_index = 5
            else:
                e_index = 7

        try:
            component.hazard_rate_dormant = component.hazard_rate_active * \
                                            factor[c_index - 1][e_index]
            return False
        except IndexError:
            component.hazard_rate_dormant = 0.0
            return True
        except UnboundLocalError:
            component.hazard_rate_dormant = 0.0
            return True


class Hardware(object):
    """
    The Hardware data controller provides an interface between the Hardware
    data model and an RTK view model.  A single Hardware controller can manage
    one or more Hardware data models.  The Hardware data controller is
    currently unused.
    """

    def __init__(self):
        """
        Method to initialize a Hardware data controller instance.
        """

        pass
