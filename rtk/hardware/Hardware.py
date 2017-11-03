#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.Hardware.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _get_component_index(category, subcategory):
    """
    Helper method to find the correct component index.

    """

    if category == 1:  # Capacitor
        _c_index = 3
    elif category == 2:  # Connection
        _c_index = 7
    elif category == 3:  # Inductive Device.
        if subcategory > 1:  # Transformer
            _c_index = 9
    elif category == 4:  # IC
        _c_index = 0
    elif category == 7:  # Relay
        _c_index = 6
    elif category == 8:  # Resistor
        _c_index = 4
    elif category == 9:  # Semiconductor
        if subcategory in [1, 2, 3, 4, 5, 6]:
            _c_index = 1
        elif subcategory in [7, 8, 9, 10, 11, 12, 13]:
            _c_index = 2
    elif category == 10:  # Switching Device
        _c_index = 5

    return _c_index


def _get_environment_index(active, dormant):
    """
    Helper method to find the correct environment index.

    """

    if active in [1, 2, 3]:  # Ground
        if dormant == 1:  # Ground
            _e_index = 0
        else:
            _e_index = 7
    elif active in [4, 5]:  # Naval
        if dormant == 1:  # Ground
            _e_index = 4
        elif dormant == 2:  # Naval
            _e_index = 3
        else:
            _e_index = 7
    elif active in [6, 7, 8, 9, 10]:  # Airborne
        if dormant == 1:  # Ground
            _e_index = 2
        elif dormant == 3:  # Airborne
            _e_index = 1
        else:
            _e_index = 7
    elif active == 11:  # Space
        if dormant == 1:  # Ground
            _e_index = 6
        elif dormant == 4:  # Space
            _e_index = 5
        else:
            _e_index = 7

    return _e_index


class Model(object):  # pylint: disable=R0902
    """
    The Hardware data model contains the attributes and methods of a Hardware
    item.  The Hardware class is a meta-class for the Assembly and Component
    classes.  A :py:class:`rtk.hardware.BoM.BoM` will consist of one or more
    Hardware items.

    The class attributes of a Hardware item are:
    :cvar str _qry_get_general: the SQL query used to retrieve general Hardware
                                information from the RTK Program database.
    :cvar str _qry_get_stress: the SQL query used to retrieve operating stree
                               information from the RTK Program database.
    :cvar str _qry_get_reliability: the SQL query used to retrieve the
                                    reliability information from the RTK
                                    Program database.
    :cvar str _qry_add_stress: the SQL query used to add a new record to the
                               table rk_stress in the RTK Program database.
    :cvar str _qry_add_reliability: the SQL query used to add a new record to
                                    the table rtk_reliability in the RTK
                                    Program database.
    :cvar str _qry_save_general: the SQL query used to save the Hardware item's
                                 general attributes to the RTK Program
                                 database.
    :cvar str _qry_save_stress: the SQL query used to save the Hardware item's
                                stress attributes to the RTK Program database.
    :cvar str _qry_save_reliability: the SQL query used to save the Hardware
                                     item's reliability attributes to the RTK
                                     Program database.

    The instance attributes of a Hardware item are:
    :ivar dao: the `rtk.DAO.DAO` providing the connection to the RTK Program
               database.
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
    :ivar int cost_type_id: the type of cost analysis to perform.  Options are:
                            * 1 = Assessed
                            * 2 = Specified
    :ivar str description: the noun description of the Hardware item.
    :ivar float duty_cycle: the duty cycle.
    :ivar str figure_number: the figure number in the applicable specification.
    :ivar str lcn: the Logistics Control Number of the Hardware item.
    :ivar int level: the indenture level of the Hardware item.
    :ivar int manufacturer_id: the index of the manufacturer.
    :ivar float mission_time: the mission time of the Hardware item.
    :ivar str name: the noun name of the Hardware item.
    :ivar str nsn: the National Stock Number of the Hardware item.
    :ivar str page_number: the page number in the applicable specification.
    :ivar int parent_id: the Hardware ID of the parent Hardware item.
    :ivar int part: indicates whether the Hardware item is an Assembly (0) or
                    a Component (1).
    :ivar str part_number: the part number of the Hardware item.
    :ivar int quantity: the quantity of the Hardware item in the design.
    :ivar str ref_des: the reference designator of the Hardware item.
    :ivar str remarks: any associated user remarks.
    :ivar str specification_number: the applicable specification.
    :ivar int tagged_part: indicator for user-defined use.
    :ivar int year_of_manufacture: the year the Hardware item was manufactured.

    :ivar int environment_active_id: the index of the active ambient
                                     environment.
    :ivar int environment_dormant_id: the index of the dormant ambient
                                      evironment.
    :ivar int overstress: indicates whether the Hardware item is overstressed.
    :ivar str reason: the reason(s) the Hardware item is overstressed.
    :ivar float temperature_active: the active operating ambient temperature.
    :ivar float temperature_dormant: the dormant ambient temperature.

    :ivar float add_adj_factor: the hazard rate additive adjustment factor.
    :ivar float availability_logistics: the logistics availability.
    :ivar float availability_mission: the mission availability.
    :ivar float avail_log_variance: the variance of the logistics availability.
    :ivar float avail_mis_variance: the variance of the mission availability.
    :ivar int failure_distribution_id: the index of the statistical
                                       distribution for the hazard rate.
    :ivar float failure_parameter_1: the hazard rate distribution scale
                                     parameter.
    :ivar float failure_parameter_2: the hazard rate distribution shape
                                     parameter.
    :ivar float failure_parameter_3: the hazard rate distribution location
                                     parameter.
    :ivar float hazard_rate_active: the active hazard rate.
    :ivar float hazard_rate_dormant: the dormant hazard rate.
    :ivar float hazard_rate_logistics: the logistics hazard rate.
    :ivar int hazard_rate_method_id: the method of assessing the hazard rate.
                                     Values are:
                                     * 1 = Assessed
                                     * 2 = Specified, Hazard Rate
                                     * 3 = Specified, MTBF
                                     * 4 = Specified, Distribution
    :ivar float hazard_rate_mission: the mission hazard rate.
    :ivar int hazard_rate_model: the statistical hazard rate model.
    :ivar float hazard_rate_percent: the percent of the system hazard rate
                                     coming from the Hardware item.
    :ivar float hazard_rate_software: the hazard rate of any software
                                      associated with the Hardware.
    :ivar float hazard_rate_specified: the specified hazard rate.
    :ivar int hazard_rate_type_id: the type of hazard rate assessment.  Values
                                   are:
                                   * 1 = MIL-HDBK-217FN2, Parts Count
                                   * 2 = MIL-HDBK-217FN2, Part Stress
                                   * 3 = NSWC-11
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
    :ivar float reliability_goal: the reliability goal for the Hardware item.
    :ivar int reliability_goal_measure_id: the measurement method of the
                                           reliability goal.
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

    _qry_get_general_attributes = "SELECT * FROM rtk_hardware \
                                   WHERE fld_hardware_id={0:d}"

    _qry_get_stress_attributes = "SELECT fld_environment_active_id, \
                                         fld_environment_dormant_id, \
                                         fld_overstress, \
                                         fld_reason, \
                                         fld_temperature_active, \
                                         fld_temperature_dormant \
                                  FROM rtk_stress \
                                  WHERE fld_hardware_id={0:d}"

    _qry_get_reliability_attributes = "SELECT fld_add_adj_factor, \
                                              fld_availability_logistics, \
                                              fld_availability_mission, \
                                              fld_avail_log_variance, \
                                              fld_avail_mis_variance, \
                                              fld_failure_distribution_id, \
                                              fld_scale_parameter, \
                                              fld_shape_parameter, \
                                              fld_location_parameter, \
                                              fld_hazard_rate_active, \
                                              fld_hazard_rate_dormant, \
                                              fld_hazard_rate_logistics, \
                                              fld_hazard_rate_method_id, \
                                              fld_hazard_rate_mission, \
                                              fld_hazard_rate_percent, \
                                              fld_hazard_rate_software, \
                                              fld_hazard_rate_specified, \
                                              fld_hazard_rate_type_id, \
                                              fld_hr_active_variance, \
                                              fld_hr_dormant_variance, \
                                              fld_hr_logistics_variance, \
                                              fld_hr_mission_variance, \
                                              fld_hr_specified_variance, \
                                              fld_mtbf_logistics, \
                                              fld_mtbf_mission, \
                                              fld_mtbf_specified, \
                                              fld_mtbf_log_variance, \
                                              fld_mtbf_miss_variance, \
                                              fld_mtbf_spec_variance, \
                                              fld_mult_adj_factor, \
                                              fld_quality_id, \
                                              fld_reliability_goal, \
                                              fld_reliability_goal_measure_id, \
                                              fld_reliability_logistics, \
                                              fld_reliability_mission, \
                                              fld_rel_log_variance, \
                                              fld_rel_miss_variance, \
                                              fld_survival_analysis_id, \
                                              fld_lambda_b \
                                       FROM rtk_reliability \
                                       WHERE fld_hardware_id={0:d}"

    _qry_add_stress = "INSERT INTO rtk_stress (fld_hardware_id) \
                       VALUES({0:d})"

    _qry_add_reliability = "INSERT INTO rtk_reliability (fld_hardware_id) \
                            VALUES({0:d})"

    _qry_save_general = "UPDATE rtk_hardware \
                         SET fld_alt_part_number='{0:s}', \
                             fld_attachments='{1:s}', fld_cage_code='{2:s}', \
                             fld_comp_ref_des='{3:s}', fld_cost={4:f}, \
                             fld_cost_failure={5:f}, fld_cost_hour={6:f}, \
                             fld_cost_type_id={7:d}, fld_description='{8:s}', \
                             fld_duty_cycle={9:f}, \
                             fld_figure_number='{10:s}', \
                             fld_lcn='{11:s}', fld_level={12:d}, \
                             fld_manufacturer_id={13:d}, \
                             fld_mission_time={14:f}, fld_name='{15:s}', \
                             fld_nsn='{16:s}', fld_page_number='{17:s}', \
                             fld_parent_id={18:d}, fld_part={19:d}, \
                             fld_part_number='{20:s}', fld_quantity={21:d}, \
                             fld_ref_des='{22:s}', fld_remarks='{23:s}', \
                             fld_repairable={24:d}, \
                             fld_specification_number='{25:s}', \
                             fld_tagged_part={26:d}, \
                             fld_total_part_count={27:d}, \
                             fld_total_power_dissipation={28:f}, \
                             fld_year_of_manufacture={29:d} \
                         WHERE fld_hardware_id={30:d}"

    _qry_save_stress = "UPDATE rtk_stress \
                        SET fld_environment_active_id={0:d}, \
                            fld_environment_dormant_id={1:d}, \
                            fld_overstress={2:d}, fld_reason='{3:s}', \
                            fld_temperature_active={4:f}, \
                            fld_temperature_dormant={5:f} \
                        WHERE fld_hardware_id={6:d}"

    _qry_save_reliability = "UPDATE rtk_reliability \
                             SET fld_add_adj_factor={0:f}, \
                                 fld_availability_logistics={1:f}, \
                                 fld_availability_mission={2:f}, \
                                 fld_avail_log_variance={3:f}, \
                                 fld_avail_mis_variance={4:f}, \
                                 fld_failure_distribution_id={5:d}, \
                                 fld_scale_parameter={6:f}, \
                                 fld_shape_parameter={7:f}, \
                                 fld_location_parameter={8:f}, \
                                 fld_hazard_rate_active={9:f}, \
                                 fld_hazard_rate_dormant={10:f}, \
                                 fld_hazard_rate_logistics={11:f}, \
                                 fld_hazard_rate_method_id={12:d}, \
                                 fld_hazard_rate_mission={13:f}, \
                                 fld_hazard_rate_percent={14:f}, \
                                 fld_hazard_rate_software={15:f}, \
                                 fld_hazard_rate_specified={16:f}, \
                                 fld_hazard_rate_type_id={17:d}, \
                                 fld_hr_active_variance={18:f}, \
                                 fld_hr_dormant_variance={19:f}, \
                                 fld_hr_logistics_variance={20:f}, \
                                 fld_hr_mission_variance={21:f}, \
                                 fld_hr_specified_variance={22:f}, \
                                 fld_mtbf_logistics={23:f}, \
                                 fld_mtbf_mission={24:f}, \
                                 fld_mtbf_specified={25:f}, \
                                 fld_mtbf_log_variance={26:f}, \
                                 fld_mtbf_miss_variance={27:f}, \
                                 fld_mtbf_spec_variance={28:f}, \
                                 fld_mult_adj_factor={29:f}, \
                                 fld_quality_id={30:d}, \
                                 fld_reliability_goal={31:f}, \
                                 fld_reliability_goal_measure_id={32:d}, \
                                 fld_reliability_logistics={33:f}, \
                                 fld_reliability_mission={34:f}, \
                                 fld_rel_log_variance={35:f}, \
                                 fld_rel_miss_variance={36:f}, \
                                 fld_survival_analysis_id={37:d}, \
                                 fld_lambda_b={38:f} \
                             WHERE fld_hardware_id={39:d}"

    def __init__(self, dao=None):
        """
        Method to initialize a Hardware data model instance.

        :param dao: the `rtk.DAO.DAO` object connected to the RTK Program
                    database.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.hazard_rate_model = {}

        # Define public list attributes.
        self.user_float = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.user_int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.user_varchar = ['', '', '', '', '']

        # Define public scalar attributes.
        self.dao = dao

        # General attributes.
        self.revision_id = None
        self.hardware_id = None
        self.alt_part_number = ''
        self.attachments = ''
        self.cage_code = ''
        self.comp_ref_des = ''
        self.cost = 0.0
        self.cost_failure = 0.0
        self.cost_hour = 0.0
        self.cost_type_id = 0
        self.description = ''
        self.duty_cycle = 100.0
        self.figure_number = ''
        self.lcn = ''
        self.level = 0
        self.manufacturer_id = 0
        self.mission_time = 100.0
        self.name = ''
        self.nsn = ''
        self.page_number = ''
        self.parent_id = None
        self.part = 0
        self.part_number = ''
        self.quantity = 1
        self.ref_des = ''
        self.remarks = ''
        self.repairable = 0
        self.specification_number = ''
        self.tagged_part = 0
        self.total_part_count = 0
        self.total_power_dissipation = 0.0
        self.year_of_manufacture = 2017

        # Stress attributes.
        self.environment_active_id = 0
        self.environment_dormant_id = 0
        self.overstress = 0
        self.reason = ''
        self.temperature_active = 30.0
        self.temperature_dormant = 25.0

        # Reliability attributes.
        self.add_adj_factor = 0.0
        self.availability_logistics = 1.0
        self.availability_mission = 1.0
        self.avail_log_variance = 0.0
        self.avail_mis_variance = 0.0
        self.failure_distribution_id = 0
        self.scale_parameter = 0.0
        self.shape_parameter = 0.0
        self.location_parameter = 0.0
        self.hazard_rate_active = 0.0
        self.hazard_rate_dormant = 0.0
        self.hazard_rate_logistics = 0.0
        self.hazard_rate_method_id = 0
        self.hazard_rate_mission = 0.0
        self.hazard_rate_percent = 0.0
        self.hazard_rate_software = 0.0
        self.hazard_rate_specified = 0.0
        self.hazard_rate_type_id = 0
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
        self.quality_id = 0
        self.reliability_goal = 1.0
        self.reliability_goal_measure_id = 0
        self.reliability_logistics = 1.0
        self.reliability_mission = 1.0
        self.rel_log_variance = 0.0
        self.rel_miss_variance = 0.0
        self.survival_analysis_id = 0
        self.lambda_b = 0.0

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

    def _get_general_attributes(self):
        """
        Method to retrieve the general attributes from the RTK Program database.

        :return: _records
        :rtype: tuple
        """

        _query = self._qry_get_general_attributes.format(self.hardware_id)

        (_records, _error_code, __) = self.dao.execute(_query, commit=False)

        try:
            _records = _records[0]
        except IndexError:
            _records = (self.revision_id, self.hardware_id, u'', u'', u'', 0,
                        u'', 0.0, 0.0, 0.0, 2, u'', 100.0, u'', u'', 1, 0,
                        10.0, u'Name', u'', u'', 1, 0, u'', 1, u'Ref Des', 1.0,
                        0, u'None', 0, u'Specification', 0, 0, 0, 0.0, 2014)

        return _records

    def _get_stress_attributes(self):
        """
        Method to retrieve the stress attributes from the RTK Program database.

        :return: _records; the stress attributes for the selected Hardware.
        :rtype: tuple
        """

        _query = self._qry_get_stress_attributes.format(self.hardware_id)

        (_records, _error_code, __) = self.dao.execute(_query, commit=False)

        # We don't need to return the hardware_id (first) field.
        try:
            _records = _records[0]
        except IndexError:
            _records = (0, 0, 0, u'Reason', 30.0, 25.0)

        return _records

    def set_attributes(self, attributes):
        """
        Method to set the Hardware data model attributes.

        :param tuple attributes: tuple of attribute values to assign to the
                                 instance attributes.
        :return: (_code, _msg); the error codes and error messages.
        :rtype: (list, list)
        """

        _code = [0, 0, 0, 0]
        _msg = ['', '', '', '']

        # Set the general attributes for the Hardware item.
        (_code[0], _msg[0]) = self._set_general_attributes(attributes[:34])

        # If that was successful, set the stress-specific attributes
        # for the Hardware item.
        if _code[0] == 0:
            (_code[1], _msg[1]) = self._set_stress_attributes(
                attributes[34:40])

        # If that was successful, set the reliability-specific
        # attributes for the Hardware item.
        if _code[1] == 0:
            (_code[2],
             _msg[2]) = self._set_reliability_attributes(attributes[40:])

        # If that was successful, set the maintainability-specific
        # attributes for the Hardware item.
        # if _code[2] == 0:
        #     (_code[3],
        #      _msg[3]) = self._set_maintainability_attributes(attributes[79:])

        return _code, _msg

    def _set_stress_attributes(self, attributes):
        """
        Method to set the stress-specific Hardware attributes.

        :param tuple attributes: tuple of attribute values to assign to the
                                 instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.environment_active_id = int(attributes[0])
            self.environment_dormant_id = int(attributes[1])
            self.overstress = int(attributes[2])
            self.reason = str(attributes[3])
            self.temperature_active = float(attributes[4])
            self.temperature_dormant = float(attributes[5])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = _(u"ERROR: Hardware._set_stress_attributes: "
                     u"Insufficient stress input values.  Require six, only "
                     u"{0:d} were passed.").format(len(attributes))
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = _(u"ERROR: Hardware._set_stress_attributes: Converting one "
                     u"or more stress inputs to the correct data type.")

        return _code, _msg

    def _set_user_attributes(self, values):
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

        return _code, _msg

    def save_attributes(self):
        """
        Method to save the attributes for a Hardware object to the RTK
        Program database.

        :return: _error_codes; list of error codes from each save
                               method.
        :rtype: list
        """

        _error_codes = [0, 0, 0, 0]

        _error_codes[0] = self.save_general_attributes()
        _error_codes[1] = self.save_stress_attributes()
        _error_codes[2] = self.save_reliability_attributes()
        # _error_codes[3] = self.save_maintainability_attributes()

        return _error_codes

    def save_general_attributes(self):
        """
        Method to save the general attributes for a Hardware object to the RTK
        Program database.

        :return: _error_code;
        :rtype: int
        """

        _query = self._qry_save_general.format(self.alt_part_number,
                                               self.attachments,
                                               self.cage_code,
                                               self.comp_ref_des,
                                               self.cost,
                                               self.cost_failure,
                                               self.cost_hour,
                                               self.cost_type_id,
                                               self.description,
                                               self.duty_cycle,
                                               self.figure_number,
                                               self.lcn,
                                               self.level,
                                               self.manufacturer_id,
                                               self.mission_time,
                                               self.name,
                                               self.nsn,
                                               self.page_number,
                                               self.parent_id,
                                               self.part,
                                               self.part_number,
                                               self.quantity,
                                               self.ref_des,
                                               self.remarks,
                                               self.repairable,
                                               self.specification_number,
                                               self.tagged_part,
                                               self.total_part_count,
                                               self.total_power_dissipation,
                                               self.year_of_manufacture,
                                               self.hardware_id)

        (_result, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def save_stress_attributes(self):
        """
        Method to save the stress attributes for a Hardware object to the RTK
        Program database.

        :return: _error_code;
        :rtype: int
        """
        _query = self._qry_save_stress.format(self.environment_active_id,
                                              self.environment_dormant_id,
                                              self.overstress, self.reason,
                                              self.temperature_active,
                                              self.temperature_dormant,
                                              self.hardware_id)

        (_result, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def save_reliability_attributes(self):
        """
        Method to save the reliability attributes for a Hardware object to the
        RTK Program database.

        :return: _error_code;
        :rtype: int
        """

        _query = self._qry_save_reliability.format(self.add_adj_factor,
                                                   self.availability_logistics,
                                                   self.availability_mission,
                                                   self.avail_log_variance,
                                                   self.avail_mis_variance,
                                                   self.failure_distribution_id,
                                                   self.scale_parameter,
                                                   self.shape_parameter,
                                                   self.location_parameter,
                                                   self.hazard_rate_active,
                                                   self.hazard_rate_dormant,
                                                   self.hazard_rate_logistics,
                                                   self.hazard_rate_method_id,
                                                   self.hazard_rate_mission,
                                                   self.hazard_rate_percent,
                                                   self.hazard_rate_software,
                                                   self.hazard_rate_specified,
                                                   self.hazard_rate_type_id,
                                                   self.hr_active_variance,
                                                   self.hr_dormant_variance,
                                                   self.hr_logistics_variance,
                                                   self.hr_mission_variance,
                                                   self.hr_specified_variance,
                                                   self.mtbf_logistics,
                                                   self.mtbf_mission,
                                                   self.mtbf_specified,
                                                   self.mtbf_log_variance,
                                                   self.mtbf_miss_variance,
                                                   self.mtbf_spec_variance,
                                                   self.mult_adj_factor,
                                                   self.quality_id,
                                                   self.reliability_goal,
                                                   self.reliability_goal_measure_id,
                                                   self.reliability_logistics,
                                                   self.reliability_mission,
                                                   self.rel_log_variance,
                                                   self.rel_miss_variance,
                                                   self.survival_analysis_id,
                                                   self.lambda_b,
                                                   self.hardware_id)

        (_result, _error_code, __) = self.dao.execute(_query, commit=True)

        return _error_code

    def calculate(self):
        """
        Method to calculate various Hardware attributes.

        :return: (_code, _msg); lists of error codes and error messages.
        :rtype: (list, list)
        """

        _code = [0, 0, 0]
        _msg = ['', '', '']

        (_code[0], _msg[0]) = self.calculate_reliability()
        # (_code[1], _msg[1]) = self.calculate_maintainability()
        (_code[2], _msg[2]) = self.calculate_costs()

        return _code, _msg

    def calculate_reliability(self):
        """
        Method to calculate reliability metrics for a Hardware item.

        :return: (_code, _msg); the error code and error message.
        :rtype: (int, str)
        """

        from math import exp

        _code = 0
        _msg = ''

        # Calculate the logistics hazard rate.
        self.hazard_rate_logistics = self.hazard_rate_active + \
            self.hazard_rate_dormant + self.hazard_rate_software

        try:
            self.mtbf_logistics = 1.0 / self.hazard_rate_logistics
        except ZeroDivisionError:
            self.mtbf_logistics = 0.0
            _code = 10
            _msg = _(u"ERROR: Hardware._calculate_reliability(): Zero "
                     u"division error when calculating logistics MTBF.  "
                     u"Active hazard rate = {0:f}, dormant hazard rate = "
                     u"{1:f}, software hazard rate = "
                     u"{2:f}.").format(self.hazard_rate_active,
                                       self.hazard_rate_dormant,
                                       self.hazard_rate_software)

        self.reliability_logistics = exp(-1.0 *
                                         self.hazard_rate_logistics *
                                         self.mission_time)

        # Calculate logistics hazard rate variances if using handbook methods.
        if self.hazard_rate_method_id == 1:
            self.hr_active_variance = self.hazard_rate_active ** 2.0
            self.hr_dormant_variance = self.hazard_rate_dormant ** 2.0
            # self.hr_specified_variance = 1.0 / \
            #                              (self.hazard_rate_specified**2.0)

        # Calculate the mission hazard rate.
        # FIXME: Add attributes to allow mission (redundancy) calculations.
        self.hazard_rate_mission = self.hazard_rate_logistics
        self.reliability_mission = self.reliability_logistics

        return _code, _msg

    def calculate_costs(self):
        """
        Method to calculate cost metrics for a hardware item.

        :return: (_code, _msg); the error code and error message.
        :rtype: (int, str)
        """

        _code = 0
        _msg = ''

        # Calculate O & M cost metrics.
        try:
            self.cost_failure = self.cost / \
                                (self.hazard_rate_logistics *
                                 self.mission_time)
        except ZeroDivisionError:
            self.cost_failure = 0.0
            _code = 10
            _msg = _(u"ERROR: Hardware._calculate_cost(): Zero division error "
                     u"when calculating cost per failure.  Logistics hazard "
                     u"rate = {0:f}, mission "
                     u"time = {1:f}.").format(self.hazard_rate_logistics,
                                              self.mission_time)

        try:
            self.cost_hour = self.cost / self.mission_time
        except ZeroDivisionError:
            self.cost_hour = 0.0
            _code = 10
            _msg = _(u"ERROR: Hardware._calculate_cost(): Zero division error "
                     u"when calculating cost per hour.  Mission "
                     u"time = {0:f}.").format(self.mission_time)

        return _code, _msg

    def _dormant_hazard_rate(self, component):
        """
        Method to calculate the dormant hazard rate based on active
        environment, dormant environment, and component category.

        All conversion factors come from Reliability Toolkit: Commercial
        Practices Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below).

        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Component |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
        | Category  |Active |Active  |Active  |Active |Active |Active |Active |
        |           |to     |to      |to      |to     |to     |to     |to     |
        |           |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
        |           |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
        +===========+=======+========+========+=======+=======+=======+=======+
        | Integrated| 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
        | Circuits  |       |        |        |       |       |       |       |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Diodes    | 0.04  |  0.05  |  0.01  | 0.04  | 0.03  | 0.20  | 0.80  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Transistor| 0.05  |  0.06  |  0.02  | 0.05  | 0.03  | 0.20  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Capacitors| 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Resistors | 0.20  |  0.06  |  0.03  | 0.10  | 0.06  | 0.50  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Switches  | 0.40  |  0.20  |  0.10  | 0.40  | 0.20  | 0.80  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Relays    | 0.20  |  0.20  |  0.04  | 0.30  | 0.08  | 0.40  | 0.90  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Connectors| 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Circuit   | 0.04  |  0.02  |  0.01  | 0.03  | 0.01  | 0.08  | 0.20  |
        | Boards    |       |        |        |       |       |       |       |
        +-----------+-------+--------+--------+-------+-------+-------+-------+
        | Xformers  | 0.20  |  0.20  |  0.20  | 0.30  | 0.30  | 0.50  | 1.00  |
        +-----------+-------+--------+--------+-------+-------+-------+-------+

        :param :class: `rtk.hardware.Component` component: the rtk.Component()
                                                           data model to
                                                           calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Move to each component type model.
        _status = False

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
        c_index = _get_component_index(component.category_id,
                                       component.subcategory_id)

        # Now find the appropriate active to passive environment index.
        e_index = _get_environment_index(component.environment_active,
                                         component.environment_dormant)

        try:
            component.hazard_rate_dormant = component.hazard_rate_active * \
                                            factor[c_index - 1][e_index]
        except IndexError:
            component.hazard_rate_dormant = 0.0
            _status = True
        except UnboundLocalError:
            component.hazard_rate_dormant = 0.0
            _status = True

        return _status

    @classmethod
    def add_hardware(cls, revision_id, dao, parent_id=0, part=0):
        """
        Method to add a Hardware record to the RTK Program database.

        :param int revision_id: the ID of the Revision to associate the
                                Hardware item with.
        :param dao: the `rtk.DAO.DAO` object connected to the RTK Program
                    database.
        :param int parent_id: the ID of the parent item of the new node.  By
                              default the new node is added to the top level
                              item.
        :param int part: variable indicating whether to add a new assembly
                         (part=0, default) or component (part=1).
        :return: (_error_code, _msg, _item_id); a tuple containing the code
                 and message for the error that occured, if any, and the ID of
                 the newly added item.  Error codes are:
                     * 0 = success
                     * 100 = failed to add new record to the
                             rtk_hardware table.
                     * 200 = failed to add new record to the
                             rtk_stress table.
                     * 300 = failed to add new record to the
                             rtk_reliability table.
                 These values are added to the error code returned from the
                 `rtk.DAO.DAO` object executing the query.
        :rtype: (int, str, int)
        """

        _msg = _(u"SUCCESS: Hardware.add_hardware: Succesfully added a "
                 u"Hardware record to the RTK Program database.")

        _lst_add_item_query = ["INSERT INTO rtk_hardware \
                                (fld_revision_id, fld_parent_id, fld_part) \
                                VALUES({0:d}, {1:d}, {2:d})",
                               "INSERT INTO rtk_stress \
                                (fld_hardware_id) \
                                VALUES({0:d})",
                               "INSERT INTO rtk_reliability \
                                (fld_hardware_id) \
                                VALUES({0:d})"]

        # Add a new record to the rtk_hardware table.
        _query = _lst_add_item_query[0].format(revision_id, parent_id, part)
        (_results,
         _error_code,
         _item_id) = dao.execute(_query, commit=True)

        # If record was successfully added to rtk_hardware, add a new
        # record to the rtk_stress table.  If not, set the error
        # message.
        if _results:
            _query = _lst_add_item_query[1].format(_item_id)
            (_results,
             _error_code,
             __) = dao.execute(_query, commit=True)
        else:
            _msg = _(u"ERROR: Hardware.add_hardware(): Failed to add new "
                     u"record to table rtk_hardware.  Database returned error "
                     u"code: {0:d}").format(_error_code)

        # If record was successfully added to rtk_stress, add a new record to
        # the rtk_reliability table.  If not, set the error message.
        if _results:
            _query = _lst_add_item_query[2].format(_item_id)
            (_results,
             _error_code,
             __) = dao.execute(_query, commit=True)

            # If record was unsuccessfully added to rtk_reliability, set the
            # error message.
            if not _results:
                _msg = _(u"ERROR: Hardware.add_hardware(): Failed to add new "
                         u"record to table rtk_reliability.  Database "
                         u"returned error code: {0:d}").format(_error_code)
        else:
            _msg = _(u"ERROR: Hardware.add_hardware(): Failed to add new "
                     u"record to table rtk_stress.  Database returned error "
                     u"code: {0:d}").format(_error_code)

        return _error_code, _msg, _item_id

    @classmethod
    def remove_hardware(cls, hardware_id, dao, children=True):
        """
        Method to remove a hardware item from the RTK Program database.

        :param int hardware_id: the ID of the Hardware item to remove.
        :param dao: the `rtk.DAO.DAO` object connected to the RTK Program
                    database.
        :param bool children: variable indicating whether (default) or not to
                              remove the children records too.
        :return: (_error_code, _msg); a tuple containing the error
                                      code and error message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = _(u"SUCCESS: Hardware.remove_hardware(): Succesfully removed "
                 u"record hardware_id={0:d} and all child records from the "
                 u"RTK Program database.").format(hardware_id)

        _lst_remove_item_query = ["DELETE FROM rtk_hardware \
                                   WHERE fld_parent_id={0:d}",
                                  "DELETE FROM rtk_hardware \
                                   WHERE fld_hardware_id={0:d}"]

        # Remove all the children of the Hardware item to remove.
        if children:
            (_results,
             _error_code,
             __) = dao.execute(_lst_remove_item_query[0].format(hardware_id),
                               commit=True)

            # If all children were successfully removed from rtk_hardware,
            # remove the Hardware item whose hardware ID was passed from
            # rtk_hardware.  Otherwise set the error message.
            if _results:
                (_results, _error_code, __) = dao.execute(
                    _lst_remove_item_query[1].format(hardware_id), commit=True)

                # If the Hardware item whose hardware ID was passed was
                # not removed from rtk_hardware, set the error message.
                if not _results:
                    _msg = _(u"ERROR: Hardware.remove_hardware(): Failed to "
                             u"remove record whose hardware_id={0:d} from "
                             u"table rtk_hardware.  Database returned error "
                             u"code: {1:d}").format(hardware_id, _error_code)
            else:
                _msg = _(u"ERROR: Hardware.remove_hardware(): Failed to "
                         u"remove one or more child records whose parent "
                         u"record is hardware_id={0:d} from table "
                         u"rtk_hardware.  Database returned error "
                         u"code: {1:d}").format(hardware_id, _error_code)

        return _error_code, _msg

    def old_calculate(self, assembly):
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
            if _component.hazard_rate_method == 1:  # Assessed
                try:
                    _component.calculate_part()
                except AttributeError:
                    # FIXME: Handle AttributeError in calculate.
                    print "Could not calculate {0:s}".format(_component.name)

            elif _component.hazard_rate_method == 2:  # Specified, h(t)
                _component.hazard_rate_active = assembly.hazard_rate_specified
            elif _component.hazard_rate_method == 3:  # Specified, MTBF
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
            if _assembly.hazard_rate_method == 1:  # Assessed
                self.calculate(_assembly)
            elif _assembly.hazard_rate_method == 2:  # Specified, h(t)
                _assembly.hazard_rate_active = _assembly.hazard_rate_specified
            elif _assembly.hazard_rate_method == 3:  # Specified, MTBF
                _assembly.hazard_rate_active = 1.0 / _assembly.mtbf_specified

            # Adjust the active hazard rate.
            _assembly.hazard_rate_active = (_assembly.hazard_rate_active +
                                            _assembly.add_adj_factor) * \
                                           (_assembly.duty_cycle / 100.0) * \
                                           _assembly.mult_adj_factor * _assembly.quantity

            # Calculate assembly derived results.
            self._calculate_reliability(_assembly)
            self._calculate_costs(_assembly)

            # Update parent assembly hazard rates and costs.
            assembly.hazard_rate_active += _assembly.hazard_rate_active
            assembly.hazard_rate_dormant += _assembly.hazard_rate_dormant
            assembly.hazard_rate_software += _assembly.hazard_rate_software
            assembly.cost += _assembly.cost
            assembly.total_part_quantity += _assembly.total_part_quantity
            assembly.total_power_dissipation += \
                _assembly.total_power_dissipation

        # Calculate parent assembly derived results.
        self._calculate_reliability(assembly)
        self._calculate_costs(assembly)

        return False

    def _old_calculate_reliability(self, hardware):  # pylint: disable=R0201
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
                                         hardware.hazard_rate_dormant + hardware.hazard_rate_software

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
