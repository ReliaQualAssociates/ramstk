#!/usr/bin/env python
"""
############################
Hardware Package Data Module
############################
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
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf

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
    The Hardware data model contains the attributes and methods of a hardware
    item.  A :class:`rtk.revision.Revision` will consist of one or more
    Hardware items.  The attributes of a Hardware are:

    :ivar dicChildren: Dictionary of the Hardware data models that are children of this data model.  Key is the Hardware ID; value is a pointer to the Hardware data model instance.

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
        self.category_id = 0
        self.comp_ref_des = ''
        self.cost = 0.0
        self.cost_failure = 0.0
        self.cost_hour = 0.0
        self.cost_type = 0
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
        self.repairable = 0
        self.rpm = 0.0
        self.specification_number = ''
        self.subcategory_id = 0
        self.tagged_part = 0
        self.temperature_active = 30.0
        self.temperature_dormant = 30.0
        self.total_part_quantity = 0
        self.total_power_dissipation = 0.0
        self.vibration = 0.0
        self.year_of_manufacture = 2014

        # Stress attributes.
        self.current_ratio = 1.0
        self.junction_temperature = 30.0
        self.knee_temperature = 0.0
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
        self.thermal_resistance = 0.0
        self.tref = 0.0
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
        self.hazard_rate_model = ''
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

        (_code, _msg) = self._set_base_attributes(values[:44])
        (_code, _msg) = self._set_stress_attributes(values[44:60])
        (_code, _msg) = self._set_reliability_attributes(values[60:96])

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
            self.category_id = int(values[5])
            self.comp_ref_des = str(values[6])
            self.cost = float(values[7])
            self.cost_failure = float(values[8])
            self.cost_hour = float(values[9])
            self.cost_type = int(values[10])
            self.description = str(values[11])
            self.duty_cycle = float(values[12])
            self.environment_active = int(values[13])
            self.environment_dormant = int(values[14])
            self.figure_number = str(values[15])
            self.humidity = float(values[16])
            self.lcn = str(values[17])
            self.level = int(values[18])
            self.manufacturer = int(values[19])
            self.mission_time = float(values[20])
            self.name = str(values[21])
            self.nsn = str(values[22])
            self.overstress = int(values[23])
            self.page_number = str(values[24])
            self.parent_id = int(values[25])
            self.part = int(values[26])
            self.part_number = str(values[27])
            self.quantity = int(values[28])
            self.ref_des = str(values[29])
            self.reliability_goal = float(values[30])
            self.reliability_goal_measure = int(values[31])
            self.remarks = str(values[32])
            self.repairable = int(values[33])
            self.rpm = float(values[34])
            self.specification_number = str(values[35])
            self.subcategory_id = int(values[36])
            self.tagged_part = int(values[37])
            self.temperature_active = float(values[38])
            self.temperature_dormant = float(values[39])
            self.total_part_quantity = int(values[40])
            self.total_power_dissipation = float(values[41])
            self.vibration = float(values[42])
            self.year_of_manufacture = int(values[43])
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
            self.junction_temperature = float(values[1])
            self.knee_temperature = float(values[2])
            self.max_rated_temperature = float(values[3])
            self.min_rated_temperature = float(values[4])
            self.operating_current = float(values[5])
            self.operating_power = float(values[6])
            self.operating_voltage = float(values[7])
            self.power_ratio = float(values[8])
            self.rated_current = float(values[9])
            self.rated_power = float(values[10])
            self.rated_voltage = float(values[11])
            self.temperature_rise = float(values[12])
            self.thermal_resistance = float(values[13])
            self.tref = float(values[14])
            self.voltage_ratio = float(values[15])
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
                  cage_code, category_id, comp_ref_des, cost, cost_failure,
                  cost_hour, cost_type, description, duty_cycle,
                  environment_active, environment_dormant, figure_number,
                  humidity, lcn, level, manufacturer, mission_time, name, nsn,
                  overstress, page_number, parent_id, part, part_number,
                  quantity, ref_des, reliability_goal,
                  reliability_goal_measure, remarks, repairable, rpm,
                  specification_number, subcategory_id, tagged_part,
                  temperature_active, temperature_dormant, total_part_quantity,
                  total_power_dissipation, vibration, year_of_manufacture)
        :rtype: tuple
        """

        _values = (self.revision_id, self.hardware_id, self.alt_part_number,
                   self.attachments, self.cage_code, self.category_id,
                   self.comp_ref_des, self.cost, self.cost_failure,
                   self.cost_hour, self.cost_type, self.description,
                   self.duty_cycle, self.environment_active,
                   self.environment_dormant, self.figure_number, self.humidity,
                   self.lcn, self.level, self.manufacturer, self.mission_time,
                   self.name, self.nsn, self.overstress, self.page_number,
                   self.parent_id, self.part, self.part_number, self.quantity,
                   self.ref_des, self.reliability_goal,
                   self.reliability_goal_measure, self.remarks,
                   self.repairable, self.rpm, self.specification_number,
                   self.subcategory_id, self.tagged_part,
                   self.temperature_active, self.temperature_dormant,
                   self.total_part_quantity, self.total_power_dissipation,
                   self.vibration, self.year_of_manufacture)

        return _values

    def _get_stress_attributes(self):
        """
        Retrieves the current values of the Hardware data model stress
        attributes.

        :return: (current_ratio, junction_temperature, knee_temperature,
                  max_rated_temperature, min_rated_temperature,
                  operating_current, operating_power, operating_voltage,
                  power_ratio, rated_current, rated_power, rated_voltage,
                  temperature_rise, thermal_resistance, tref, voltage_ratio)
        :rtype: tuple
        """

        _values = (self.current_ratio, self.junction_temperature,
                   self.knee_temperature, self.max_rated_temperature,
                   self.min_rated_temperature, self.operating_current,
                   self.operating_power, self.operating_voltage,
                   self.power_ratio, self.rated_current, self.rated_power,
                   self.rated_voltage, self.temperature_rise,
                   self.thermal_resistance, self.tref, self.voltage_ratio)

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

        self.cost_failure = self.cost / \
                            (self.hazard_rate_logistics * self.mission_time)
        self.cost_hour = self.cost / self.mission_time

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
    one or more Hardware data models.  The attributes of an Hardware data
    controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
    Project database.
    :ivar _last_id: the last Requirement ID used.
    :ivar dicHardware: Dictionary of the Hardware data models managed.  Key is the Hardware ID; value is a pointer to the Hardware data model instance.
    """

    def __init__(self):
        """
        Initializes an Hardware data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicHardware = {}

    def request_hardware(self, dao, revision_id):
        """
        Reads the RTK Project database and loads all the Hardware associated
        with the selected Revision.  For each Hardware returned:

        #. Retrieve the Hardware from the RTK Project database.
        #. Create an Hardware data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Hardware being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the requirements for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('rtk_hardware')[0]

        # Select everything from the function table.
        _query = "SELECT t1.*, \
                         t2.fld_current_ratio, t2.fld_junction_temperature, \
                         t2.fld_knee_temperature, \
                         t2.fld_max_rated_temperature, \
                         t2.fld_min_rated_temperature, \
                         t2.fld_operating_current, t2.fld_operating_power, \
                         t2.fld_operating_voltage, t2.fld_power_ratio, \
                         t2.fld_rated_current, t2.fld_rated_power, \
                         t2.fld_rated_voltage, t2.fld_temperature_rise, \
                         t2.fld_thermal_resistance, t2.fld_tref, \
                         t2.fld_voltage_ratio, \
                         t3.fld_add_adj_factor, \
                         t3.fld_availability_logistics, \
                         t3.fld_availability_mission, \
                         t3.fld_avail_log_variance, \
                         t3.fld_avail_mis_variance, t3.fld_failure_dist, \
                         t3.fld_failure_parameter_1, \
                         t3.fld_failure_parameter_2, \
                         t3.fld_failure_parameter_3, \
                         t3.fld_hazard_rate_active, \
                         t3.fld_hazard_rate_dormant, \
                         t3.fld_hazard_rate_logistics, \
                         t3.fld_hazard_rate_method, \
                         t3.fld_hazard_rate_mission, \
                         t3.fld_hazard_rate_model, \
                         t3.fld_hazard_rate_percent, \
                         t3.fld_hazard_rate_software, \
                         t3.fld_hazard_rate_specified, \
                         t3.fld_hazard_rate_type, t3.fld_hr_active_variance, \
                         t3.fld_hr_dormant_variance, \
                         t3.fld_hr_logistics_variance, \
                         t3.fld_hr_mission_variance, \
                         t3.fld_hr_specified_variance, t3.fld_mtbf_logistics, \
                         t3.fld_mtbf_mission, t3.fld_mtbf_specified, \
                         t3.fld_mtbf_log_variance, t3.fld_mtbf_miss_variance, \
                         t3.fld_mtbf_spec_variance, t3.fld_mult_adj_factor, \
                         t3.fld_reliability_logistics, \
                         t3.fld_reliability_mission, t3.fld_rel_log_variance, \
                         t3.fld_rel_miss_variance, t3.fld_survival_analysis \
                  FROM rtk_hardware AS t1 \
                  INNER JOIN rtk_stress AS t2 \
                  ON t2.fld_hardware_id=t1.fld_hardware_id \
                  INNER JOIN rtk_reliability AS t3 \
                  ON t3.fld_hardware_id=t1.fld_hardware_id \
                  WHERE t1.fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_assemblies = len(_results)
        except TypeError as _err:
            _n_assemblies = 0

        for i in range(_n_assemblies):
            _hardware = Model()
            _hardware.set_attributes(_results[i])
            self.dicHardware[_hardware.hardware_id] = _hardware

        return(_results, _error_code)

    def add_hardware(self, revision_id, hardware_type, parent_id=None):
        """
        Adds a new Hardware item to the RTK Project for the selected Revision.

        :param int revision_id: the Revision ID to add the new Hardware
                                item(s).
        :param int hardware_type: the type of Hardware item to add.
                                  * 0 = Assembly
                                  * 1 = Component
        :keyword int parent_id: the Hardware ID of the parent requirement.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # By default we add the new Hardware item as an immediate child of the
        # top-level assembly.
        if parent_id is None:
            parent_id = 0

        _query = "INSERT INTO rtk_hardware \
                  (fld_revision_id, fld_parent_id, fld_part) \
                  VALUES({0:d}, {1:d}, {2:d})".format(revision_id, parent_id,
                                                      hardware_type)
        (_results, _error_code, _hardware_id) = self._dao.execute(_query,
                                                                  commit=True)

        # If the new hardware item was added successfully to the RTK Project
        # database, add a record to the stress table in the RTK Project
        # database.
        if _results:
            _query = "INSERT INTO rtk_stress \
                      (fld_hardware_id) \
                      VALUES({0:d})".format(_hardware_id)
        (_results, _error_code, _) = self._dao.execute(_query, commit=True)

        # If the record was successfully added to the stress table, add a
        # record to the reliability table.
        if _results:
            _query = "INSERT INTO rtk_reliability \
                      (fld_hardware_id) \
                      VALUES({0:d})".format(_hardware_id)
        (_results, _error_code, _) = self._dao.execute(_query, commit=True)

        # If the new hardware item was added successfully to all the tables in
        # the RTK Project database:
        #   1. Retrieve the ID of the newly inserted hardware item.
        #   2. Create a new Hardware model instance.
        #   3. Set the attributes of the new Hardware model instance.
        #   2. Add the new Hardware model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('rtk_hardware')[0]
            _hardware = Model()
            _hardware.set_attributes((revision_id, self._last_id, '', '', '',
                                      0, '', 0.0, 0.0, 0.0, 1.0, '', 100.0, 0,
                                      0, '', 50.0, '', 1, 0, 10.0, '', '', 0,
                                      '', parent_id, hardware_type, '', 1, '',
                                      1.0, 0, '', 0, 0.0, '', 0, 0, 30.0, 30.0,
                                      0, 0.0, 0.0, 2014, 1.0, 30.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                                      0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                                      0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                                      0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0,
                                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                      1.0, 1.0, 1.0, 0.0, 0.0, 0))
            self.dicHardware[_hardware.hardware_id] = _hardware

        return(_hardware, _error_code)

    def delete_hardware(self, hardware_id):
        """
        Deletes a Hardware item from the RTK Project.

        :param int hardware_id: the Hardware ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Delete all the child hardware, if any.
        _query = "DELETE FROM rtk_hardware \
                  WHERE fld_parent_id={0:d}".format(hardware_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Then delete the parent hardware.
        _query = "DELETE FROM rtk_hardware \
                  WHERE fld_hardware_id={0:d}".format(hardware_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self.dicHardware.pop(hardware_id)

        return(_results, _error_code)

    def save_hardware(self, hardware_id):
        """
        Saves the Hardware attributes to the RTK Project database.

        :param int hardware_id: the ID of the hardware to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _hardware = self.dicHardware[hardware_id]

        # Save the base attributes.
        _query = "UPDATE rtk_hardware \
                  SET fld_alt_part_number='{2:s}', fld_attachments='{3:s}', \
                      fld_cage_code='{4:s}', fld_category_id={5:d}, \
                      fld_comp_ref_des='{6:s}', fld_cost={7:f}, \
                      fld_cost_failure={8:f}, fld_cost_hour={9:f}, \
                      fld_cost_type={10:d}, fld_description='{11:s}', \
                      fld_duty_cycle={12:f}, fld_environment_active={13:d}, \
                      fld_environment_dormant={14:d}, \
                      fld_figure_number='{15:s}', fld_humidity={16:f}, \
                      fld_lcn='{17:s}', fld_level={18:d}, \
                      fld_manufacturer={19:d}, fld_mission_time={20:f}, \
                      fld_name='{21:s}', fld_nsn='{22:s}', \
                      fld_overstress={23:d}, fld_page_number='{24:s}', \
                      fld_parent_id={25:d}, fld_part={26:d}, \
                      fld_part_number='{27:s}', fld_quantity={28:d}, \
                      fld_ref_des='{29:s}', fld_reliability_goal={30:f}, \
                      fld_reliability_goal_measure={31:d}, \
                      fld_remarks='{32:s}', fld_repairable={33:d}, \
                      fld_rpm={34:f}, fld_specification_number='{35:s}', \
                      fld_subcategory_id={36:d}, fld_tagged_part={37:d}, \
                      fld_temperature_active={38:f}, \
                      fld_temperature_dormant={39:f}, \
                      fld_total_part_quantity={40:d}, \
                      fld_total_power_dissipation={41:f}, \
                      fld_vibration={42:f}, fld_year_of_manufacture={43:d} \
                  WHERE fld_revision_id={0:d} \
                  AND fld_hardware_id={1:d}".format(
                      _hardware.revision_id,
                      hardware_id, _hardware.alt_part_number,
                      _hardware.attachments, _hardware.cage_code,
                      _hardware.category_id, _hardware.comp_ref_des,
                      _hardware.cost, _hardware.cost_failure,
                      _hardware.cost_hour, _hardware.cost_type,
                      _hardware.description, _hardware.duty_cycle,
                      _hardware.environment_active,
                      _hardware.environment_dormant, _hardware.figure_number,
                      _hardware.humidity, _hardware.lcn, _hardware.level,
                      _hardware.manufacturer, _hardware.mission_time,
                      _hardware.name, _hardware.nsn, _hardware.overstress,
                      _hardware.page_number, _hardware.parent_id,
                      _hardware.part, _hardware.part_number,
                      _hardware.quantity, _hardware.ref_des,
                      _hardware.reliability_goal,
                      _hardware.reliability_goal_measure, _hardware.remarks,
                      _hardware.repairable, _hardware.rpm,
                      _hardware.specification_number, _hardware.subcategory_id,
                      _hardware.tagged_part, _hardware.temperature_active,
                      _hardware.temperature_dormant,
                      _hardware.total_part_quantity,
                      _hardware.total_power_dissipation, _hardware.vibration,
                      _hardware.year_of_manufacture)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Save the stress attributes.
        _query = "UPDATE rtk_stress \
                  SET fld_current_ratio={1:f}, \
                      fld_junction_temperature={2:f}, \
                      fld_knee_temperature={3:f}, \
                      fld_max_rated_temperature={4:f}, \
                      fld_min_rated_temperature={5:f}, \
                      fld_operating_current={6:f}, fld_operating_power={7:f}, \
                      fld_operating_voltage={8:f}, fld_power_ratio={9:f}, \
                      fld_rated_current={10:f}, fld_rated_power={11:f}, \
                      fld_rated_voltage={12:f}, fld_temperature_rise={13:f}, \
                      fld_thermal_resistance={14:f}, fld_tref={15:f}, \
                      fld_voltage_ratio={16:f} \
                  WHERE fld_hardware_id={0:d}".format(
                      hardware_id, _hardware.current_ratio,
                      _hardware.junction_temperature,
                      _hardware.knee_temperature,
                      _hardware.max_rated_temperature,
                      _hardware.min_rated_temperature,
                      _hardware.operating_current, _hardware.operating_power,
                      _hardware.operating_voltage, _hardware.power_ratio,
                      _hardware.rated_current, _hardware.rated_power,
                      _hardware.rated_voltage, _hardware.temperature_rise,
                      _hardware.thermal_resistance, _hardware.tref,
                      _hardware.voltage_ratio)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Save the reliability attributes.
        _query = "UPDATE rtk_reliability \
                  SET fld_add_adj_factor={1:f}, \
                      fld_availability_logistics={2:f}, \
                      fld_availability_mission={3:f}, \
                      fld_avail_log_variance={4:f}, \
                      fld_avail_mis_variance={5:f}, fld_failure_dist={6:d}, \
                      fld_failure_parameter_1={7:f}, \
                      fld_failure_parameter_2={8:f}, \
                      fld_failure_parameter_3={9:f}, \
                      fld_hazard_rate_active={10:f}, \
                      fld_hazard_rate_dormant={11:f}, \
                      fld_hazard_rate_logistics={12:f}, \
                      fld_hazard_rate_method={13:f}, \
                      fld_hazard_rate_mission={14:f}, \
                      fld_hazard_rate_model='{15:s}', \
                      fld_hazard_rate_percent={16:f}, \
                      fld_hazard_rate_software={17:f}, \
                      fld_hazard_rate_specified={18:f}, \
                      fld_hazard_rate_type={19:d}, \
                      fld_hr_active_variance={20:f}, \
                      fld_hr_dormant_variance={21:f}, \
                      fld_hr_logistics_variance={22:f}, \
                      fld_hr_mission_variance={23:f}, \
                      fld_hr_specified_variance={24:f}, \
                      fld_mtbf_logistics={25:f}, fld_mtbf_mission={26:f}, \
                      fld_mtbf_specified={27:f}, \
                      fld_mtbf_log_variance={28:f}, \
                      fld_mtbf_miss_variance={29:f}, \
                      fld_mtbf_spec_variance={30:f}, \
                      fld_mult_adj_factor={31:f}, \
                      fld_reliability_logistics={32:f}, \
                      fld_reliability_mission={33:f}, \
                      fld_rel_log_variance={34:f}, \
                      fld_rel_miss_variance={35:f}, \
                      fld_survival_analysis={36:d} \
                  WHERE fld_hardware_id={0:d}".format(
                      hardware_id, _hardware.add_adj_factor,
                      _hardware.availability_logistics,
                      _hardware.availability_mission,
                      _hardware.avail_log_variance,
                      _hardware.avail_mis_variance, _hardware.failure_dist,
                      _hardware.failure_parameter_1,
                      _hardware.failure_parameter_2,
                      _hardware.failure_parameter_3,
                      _hardware.hazard_rate_active,
                      _hardware.hazard_rate_dormant,
                      _hardware.hazard_rate_logistics,
                      _hardware.hazard_rate_method,
                      _hardware.hazard_rate_mission,
                      _hardware.hazard_rate_model,
                      _hardware.hazard_rate_percent,
                      _hardware.hazard_rate_software,
                      _hardware.hazard_rate_specified,
                      _hardware.hazard_rate_type,
                      _hardware.hr_active_variance,
                      _hardware.hr_dormant_variance,
                      _hardware.hr_logistics_variance,
                      _hardware.hr_mission_variance,
                      _hardware.hr_specified_variance,
                      _hardware.mtbf_logistics, _hardware.mtbf_mission,
                      _hardware.mtbf_specified, _hardware.mtbf_log_variance,
                      _hardware.mtbf_miss_variance,
                      _hardware.mtbf_spec_variance,
                      _hardware.mult_adj_factor,
                      _hardware.reliability_logistics,
                      _hardware.reliability_mission,
                      _hardware.rel_log_variance,
                      _hardware.rel_miss_variance, _hardware.survival_analysis)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)
# TODO: Handle errors.
        return (_results, _error_code)

    def save_all_hardware(self):
        """
        Saves all Hardware data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _hardware in self.dicHardware.values():
            (_results,
             _error_code) = self.save_hardware(_hardware.hardware_id)

        return False
