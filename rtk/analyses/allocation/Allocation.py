#!/usr/bin/env python
"""
##############################
Allocation Package Data Module
##############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.allocation.Allocation.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf

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


class Model(object):
    """
    The Allocation data model contains the attributes and methods of an
    allocation.  The attributes of an Allocation are:

    :ivar hardware_id: default value: None
    :ivar reliability_goal: default value: 1.0
    :ivar hazard_rate_goal: default value: 0.0
    :ivar mtbf_goal: default value: 0.0
    :ivar included: default value: 1
    :ivar n_sub_systems: default value: 1
    :ivar n_sub_elements: default value: 1
    :ivar weight_factor: default value: 1.0
    :ivar percent_wt_factor: default value: 1.0
    :ivar int_factor: default value: 1
    :ivar soa_factor: default value: 1
    :ivar op_time_factor: default value: 1
    :ivar env_factor: default value: 1
    :ivar availability_alloc: default value: 0.0
    :ivar reliability_alloc: default value: 0.0
    :ivar hazard_rate_alloc: default value: 0.0
    :ivar mtbf_alloc: default value: 0.0
    :ivar parent_id: default value: -1
    """

    def __init__(self):
        """
        Initializes an Allocation data model instance.
        """

        # Initialize private scalar attributes.  These are set as a convenience
        # for performing allocations.
        self._duty_cycle = 100.0
        self._hazard_rate = 0.0
        self._mission_time = 10.0

        # Initialize public scalar attributes.
        self.hardware_id = None
        self.reliability_goal = 1.0
        self.hazard_rate_goal = 0.0
        self.mtbf_goal = 0.0
        self.included = 1
        self.n_sub_systems = 1
        self.n_sub_elements = 1
        self.weight_factor = 1.0
        self.percent_wt_factor = 1.0
        self.int_factor = 1
        self.soa_factor = 1
        self.op_time_factor = 1
        self.env_factor = 1
        self.availability_alloc = 0.0
        self.reliability_alloc = 0.0
        self.hazard_rate_alloc = 0.0
        self.mtbf_alloc = 0.0
        self.parent_id = -1
        self.method = 0
        self.goal_measure = 0

    def set_attributes(self, values):
        """
        Sets the Allocation data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.hardware_id = int(values[0])
            self.reliability_goal = float(values[1])
            self.hazard_rate_goal = float(values[2])
            self.mtbf_goal = float(values[3])
            self.included = int(values[4])
            self.n_sub_systems = int(values[5])
            self.n_sub_elements = int(values[6])
            self.weight_factor = float(values[7])
            self.percent_wt_factor = float(values[8])
            self.int_factor = int(values[9])
            self.soa_factor = int(values[10])
            self.op_time_factor = int(values[11])
            self.env_factor = int(values[12])
            self.availability_alloc = float(values[13])
            self.reliability_alloc = float(values[14])
            self.hazard_rate_alloc = float(values[15])
            self.mtbf_alloc = float(values[16])
            self.parent_id = int(values[17])
            self.method = int(values[18])
            self.goal_measure = int(values[19])
            self._duty_cycle = float(values[20])
            self._hazard_rate = float(values[21])
            self._mission_time = float(values[22])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Allocation data model attributes.

        :return: (hardware_id, reliability_goal, hazard_rate_goal, mtbf_goal,
                  included, n_sub_systems, n_sub_elements, weight_factor,
                  percent_wt_factor, int_factor, soa_factor, op_time_factor,
                  env_factor, availability_alloc, reliability_alloc,
                  failure_rate_alloc, mtbf_alloc, parent_id, method, goal)
        :rtype: tuple
        """

        _values = (self.hardware_id, self.reliability_goal,
                   self.hazard_rate_goal, self.mtbf_goal, self.included,
                   self.n_sub_systems, self.n_sub_elements, self.weight_factor,
                   self.percent_wt_factor, self.int_factor, self.soa_factor,
                   self.op_time_factor, self.env_factor,
                   self.availability_alloc, self.reliability_alloc,
                   self.hazard_rate_alloc, self.mtbf_alloc, self.parent_id,
                   self.method, self.goal_measure)

        return _values

    def equal_apportionment(self, n_children, parent_goal):
        """
        Performs an equal apportionment of the reliability goal.

        :param int n_children: the number of immediate children comprising the
                               parent hardware item.
        :param float parent_goal: the reliability goal of the parent hardware
                                  item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import log

        try:
            _weight_i = 1.0 / float(n_children)
        except ZeroDivisionError:
            return True

        self.reliability_alloc = parent_goal ** _weight_i

        try:
            self.hazard_rate_alloc = -1.0 * log(self.reliability_alloc) / \
                                     self._mission_time
            self.mtbf_alloc = 1.0 / self.hazard_rate_alloc
        except(ZeroDivisionError, ValueError):
            return True

        return False

    def agree_apportionment(self, n_children, parent_goal):
        """
        Performs an AGREE apportionment of a reliability requirement.

        :param int n_children: the number of immediate children comprising the
                               parent hardware item.
        :param float parent_goal: the reliability goal of the parent hardware
                                  item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp, log

        _time_i = self._mission_time * self._duty_cycle / 100.0

        try:
            self.mtbf_alloc = (n_children * self.weight_factor * _time_i) / \
                              (-1.0 * self.n_sub_elements * log(parent_goal))
        except(ValueError, ZeroDivisionError):
            return True

        try:
            self.hazard_rate_alloc = 1.0 / self.mtbf_alloc
        except ZeroDivisionError:
            return True

        self.reliability_alloc = exp(-1.0 * self.hazard_rate_alloc * \
                                     self._mission_time)

        return False

    def arinc_apportionment(self, system_hr, parent_goal):
        """
        Performs an ARINC apportionment of the reliability requirement.

        :param float system_hr: the current system hazard rate.
        :param float parent_goal: the goal hazard rate of the parent hardware
                                  item.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        from math import exp

        try:
            self.weight_factor = self._hazard_rate / system_hr
        except ZeroDivisionError:
            return True

        self.hazard_rate_alloc = self.weight_factor * parent_goal

        try:
            self.mtbf_alloc = 1.0 / self.hazard_rate_alloc
        except ZeroDivisionError:
            return True

        self.reliability_alloc = exp(-1.0 * self.hazard_rate_alloc * \
                                     self._mission_time)

        return False

    def foo_apportionment(self, cum_weight, parent_goal):
        """
        Performs a feasibility of objectives (FOO) apportionment of the
        reliability requirement.

        :param int cum_weight: the cumulative weight factor for all subordinate
                               assemblies.
        :param float parent_goal: the failure rate requirement to allocate.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        from math import exp
# TODO: Add range check on input factors.
        # First calculate the system failure rate and weighting factor for each
        # sub-system.
        self.weight_factor = self.int_factor * self.soa_factor * \
                             self.op_time_factor * self.env_factor

        self.percent_wt_factor = float(self.weight_factor) / float(cum_weight)

        self.hazard_rate_alloc = self.percent_wt_factor * parent_goal

        try:
            self.mtbf_alloc = 1.0 / self.hazard_rate_alloc
        except ZeroDivisionError:
            return True

        self.reliability_alloc = exp(-1.0 * self.hazard_rate_alloc * \
                                     self._mission_time)

        return False

    def calculate_goals(self):
        """
        Calculates the other two reliability metrics from the Allocation goal
        provided.

        :return: False if successful or True if an error is encountered
        :rtype: bool
        """

        from math import exp, log

        if self.goal_measure == 1:          # Reliability goal
            try:
                self.mtbf_goal = -1.0 * self._mission_time / \
                                 log(self.reliability_goal)
            except(ValueError, ZeroDivisionError):
                return True

            self.hazard_rate_goal = 1.0 / self.mtbf_goal

        elif self.goal_measure == 2:        # Hazard rate goal
            try:
                self.mtbf_goal = 1.0 / self.hazard_rate_goal
            except ZeroDivisionError:
                return True

            self.reliability_goal = exp(-1.0 * self._mission_time / \
                                        self.mtbf_goal)

        elif self.goal_measure == 3:        # MTBF goal
            try:
                self.hazard_rate_goal = 1.0 / self.mtbf_goal
            except ZeroDivisionError:
                return True

            self.reliability_goal = exp(-1.0 * self._mission_time / \
                                        self.mtbf_goal)

        return False


class Allocation(object):
    """
    The Allocation data controller provides an interface between the Allocation
    data model and an RTK view model.  A single Allocation controller can
    manage one or more Allocation data models.  The attributes of an Allocation
    data controller are:

    :ivar _dao: the Data Access Object to use when communicating with the RTK
                Project database.
    :ivar dicAllocation: Dictionary of the Allocation data models managed.  Key is the Hardware ID; value is a pointer to the Allocation data model instance.
    """

    def __init__(self):
        """
        Initializes an Allocation data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None

        # Initialize public dictionary attributes.
        self.dicAllocation = {}

    def request_allocation(self, dao):
        """
        Reads the RTK Project database and loads all the Allocation.  For each
        Allocation returned:

        #. Retrieve the Allocation from the RTK Project database.
        #. Create an Allocation data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Hardware being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        _query = "SELECT t1.fld_hardware_id, t1.fld_reliability_goal, \
                         t1.fld_hazard_rate_goal, t1.fld_mtbf_goal, \
                         t1.fld_included, t1.fld_n_sub_systems, \
                         t1.fld_n_sub_elements, t1.fld_weight_factor, \
                         t1.fld_percent_wt_factor, t1.fld_int_factor, \
                         t1.fld_soa_factor, t1.fld_op_time_factor, \
                         t1.fld_env_factor, t1.fld_availability_alloc, \
                         t1.fld_reliability_alloc, t1.fld_hazard_rate_alloc, \
                         t1.fld_mtbf_alloc, t1.fld_parent_id, \
                         t1.fld_method, t1.fld_goal_measure, \
                         t2.fld_duty_cycle, t3.fld_hazard_rate_logistics, \
                         t2.fld_mission_time, t2.fld_name, \
                         t3.fld_availability_logistics, \
                         t3.fld_reliability_logistics, \
                         t3.fld_mtbf_logistics \
                  FROM rtk_allocation AS t1 \
                  INNER JOIN rtk_hardware AS t2 \
                  ON t2.fld_hardware_id=t1.fld_hardware_id \
                  INNER JOIN rtk_reliability AS t3 \
                  ON t3.fld_hardware_id=t1.fld_hardware_id"
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_allocations = len(_results)
        except TypeError as _err:
            _n_allocations = 0

        for i in range(_n_allocations):
            _allocation = Model()
            _allocation.set_attributes(_results[i][0:23])
            self.dicAllocation[_allocation.hardware_id] = _allocation

        return(_results, _error_code)

    def add_allocation(self):
        """
        Adds a new Allocation data model to the dictionary of models controlled
        by an instance of the Allocation data controller.

        :param int hardware_id: the hardware ID of the new Allocation.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_allocation(self._dao)

        return False

    def delete_allocation(self, hardware_id):
        """
        Deletes an Allocation data model instance from the dictionary of models
        controlled by an instance of the Allocation data controller.

        :param int hardware_id: the hardware ID of the Allocation to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.dicAllocation.pop(hardware_id)

        return False

    def allocate(self, hardware_id):
        """
        Performs the allocation.

        :return: False if successful or True if an error is encountered
        :rtype: bool
        """

        _allocation = self.dicAllocation[hardware_id]

        _parent_goal = _allocation.reliability_goal
        _parent_hr = _allocation._hazard_rate

        _children = [_a for _a in self.dicAllocation.values()
                     if _a.parent_id == hardware_id]
        _allocation.weight_factor = sum([_a.int_factor * _a.soa_factor * \
                                         _a.op_time_factor * _a.env_factor \
                                         for _a in _children])
        _n_children = len(_children)
        for _child in _children:
            if _allocation.method == 1:
                _child.equal_apportionment(_n_children, _parent_goal)
            elif _allocation.method == 2:
                _child.agree_apportionment(_n_children, _parent_goal)
            elif _allocation.method == 3:
                _parent_goal = _allocation.hazard_rate_goal
                _child.arinc_apportionment(_parent_hr, _parent_goal)
            elif _allocation.method == 4:
                _parent_goal = _allocation.hazard_rate_goal
                _child.foo_apportionment(_allocation.weight_factor,
                                         _parent_goal)

        return False

    def save_allocation(self, hardware_id):
        """
        Saves the Allocation for the selected Hardware.

        :param int hardware_id: the ID of the hardware whose Allocation is to
                                be saved.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _allocation = self.dicAllocation[hardware_id]

        _query = "UPDATE rtk_allocation \
                  SET fld_reliability_goal={0:f}, fld_hazard_rate_goal={1:f}, \
                      fld_mtbf_goal={2:f}, fld_included={3:d}, \
                      fld_n_sub_systems={4:d}, fld_n_sub_elements={5:d}, \
                      fld_weight_factor={6:f}, fld_percent_wt_factor={7:f}, \
                      fld_int_factor={8:d}, fld_soa_factor={9:d}, \
                      fld_op_time_factor={10:d}, fld_env_factor={11:d}, \
                      fld_availability_alloc={12:f}, \
                      fld_reliability_alloc={13:f}, \
                      fld_hazard_rate_alloc={14:f}, fld_mtbf_alloc={15:f}, \
                      fld_parent_id={16:d}, fld_method={17:d}, \
                      fld_goal_measure={18:d} \
                  WHERE fld_hardware_id={19:d}".format(
                      _allocation.reliability_goal,
                      _allocation.hazard_rate_goal, _allocation.mtbf_goal,
                      _allocation.included, _allocation.n_sub_systems,
                      _allocation.n_sub_elements, _allocation.weight_factor,
                      _allocation.percent_wt_factor, _allocation.int_factor,
                      _allocation.soa_factor, _allocation.op_time_factor,
                      _allocation.env_factor, _allocation.availability_alloc,
                      _allocation.reliability_alloc,
                      _allocation.hazard_rate_alloc, _allocation.mtbf_alloc,
                      _allocation.parent_id, _allocation.method,
                      _allocation.goal_measure, hardware_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)
        # TODO: Handle errors.
        return (_results, _error_code)

    def save_all_allocation(self):
        """
        Saves all Allocation data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _allocation in self.dicAllocation.values():
            (_results,
             _error_code) = self.save_allocation(_allocation.hardware_id)

        return False

    def trickle_down(self, hardware_id):
        """
        Sets the next indenture level hardware items' goal to the allocated
        values calculated at the parent level.

        :param int hardware_id: the Hardware ID to trickle down.
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """

        _children = [_a for _a in self.dicAllocation.values()
                     if _a.parent_id == hardware_id]
        for _child in _children:
            _child.reliability_goal = _child.reliability_alloc

        return False
