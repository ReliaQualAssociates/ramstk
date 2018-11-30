# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKAllocation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKAllocation Table."""

from math import exp, log

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKAllocation(RAMSTK_BASE):
    """
    Class to represent the ramstk_allocation table in the RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __tablename__ = 'ramstk_allocation'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    availability_alloc = Column('fld_availability_alloc', Float, default=0.0)
    duty_cycle = Column('fld_duty_cycle', Float, default=100.0)
    env_factor = Column('fld_env_factor', Integer, default=1)
    goal_measure_id = Column('fld_goal_measure_id', Integer, default=1)
    hazard_rate_alloc = Column('fld_hazard_rate_alloc', Float, default=0.0)
    hazard_rate_goal = Column('fld_hazard_rate_goal', Float, default=0.0)
    included = Column('fld_included', Integer, default=1)
    int_factor = Column('fld_int_factor', Integer, default=1)
    method_id = Column('fld_method_id', Integer, default=1)
    mission_time = Column('fld_mission_time', Float, default=100.0)
    mtbf_alloc = Column('fld_mtbf_alloc', Float, default=0.0)
    mtbf_goal = Column('fld_mtbf_goal', Float, default=0.0)
    n_sub_systems = Column('fld_n_sub_systems', Integer, default=1)
    n_sub_elements = Column('fld_n_sub_elements', Integer, default=1)
    parent_id = Column('fld_parent_id', Integer, default=1)
    percent_weight_factor = Column(
        'fld_percent_weight_factor', Float, default=0.0)
    reliability_alloc = Column('fld_reliability_alloc', Float, default=0.0)
    reliability_goal = Column('fld_reliability_goal', Float, default=1.0)
    op_time_factor = Column('fld_op_time_factor', Integer, default=1)
    soa_factor = Column('fld_soa_factor', Integer, default=1)
    weight_factor = Column('fld_weight_factor', Integer, default=1)

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship('RAMSTKHardware', back_populates='allocation')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKAllocation data model attributes.

        :return: {hardware_id, availability_alloc, env_factor, goal_measure_id,
                  hazard_rate_alloc, hazard_rate_goal, included, int_factor,
                  method_id, mtbf_alloc, mtbf_goal, n_sub_systems,
                  n_sub_elements, parent_id, percent_wt_factor,
                  reliability_alloc, reliability_goal, op_time_factor,
                  soa_factor, weight_factor} pairs.
        :rtype: dict
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'availability_alloc': self.availability_alloc,
            'duty_cycle': self.duty_cycle,
            'env_factor': self.env_factor,
            'goal_measure_id': self.goal_measure_id,
            'hazard_rate_alloc': self.hazard_rate_alloc,
            'hazard_rate_goal': self.hazard_rate_goal,
            'included': self.included,
            'int_factor': self.int_factor,
            'method_id': self.method_id,
            'mission_time': self.mission_time,
            'mtbf_alloc': self.mtbf_alloc,
            'mtbf_goal': self.mtbf_goal,
            'n_sub_systems': self.n_sub_systems,
            'n_sub_elements': self.n_sub_elements,
            'parent_id': self.parent_id,
            'percent_weight_factor': self.percent_weight_factor,
            'reliability_alloc': self.reliability_alloc,
            'reliability_goal': self.reliability_goal,
            'op_time_factor': self.op_time_factor,
            'soa_factor': self.soa_factor,
            'weight_factor': self.weight_factor
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the RAMSTKAllocation data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKAllocation {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.availability_alloc = float(
                none_to_default(attributes['availability_alloc'], 0.0))
            self.duty_cycle = float(
                none_to_default(attributes['duty_cycle'], 100.0))
            self.env_factor = int(none_to_default(attributes['env_factor'], 1))
            self.goal_measure_id = int(
                none_to_default(attributes['goal_measure_id'], 0))
            self.hazard_rate_alloc = float(
                none_to_default(attributes['hazard_rate_alloc'], 0.0))
            self.hazard_rate_goal = float(
                none_to_default(attributes['hazard_rate_goal'], 0.0))
            self.included = int(none_to_default(attributes['included'], 1))
            self.int_factor = int(none_to_default(attributes['int_factor'], 1))
            self.method_id = int(none_to_default(attributes['method_id'], 1))
            self.mission_time = float(
                none_to_default(attributes['mission_time'], 100.0))
            self.mtbf_alloc = float(
                none_to_default(attributes['mtbf_alloc'], 0.0))
            self.mtbf_goal = float(
                none_to_default(attributes['mtbf_goal'], 0.0))
            self.n_sub_systems = int(
                none_to_default(attributes['n_sub_systems'], 1))
            self.n_sub_elements = int(
                none_to_default(attributes['n_sub_elements'], 1))
            self.parent_id = int(none_to_default(attributes['parent_id'], 1))
            self.percent_weight_factor = float(
                none_to_default(attributes['percent_weight_factor'], 0.0))
            self.reliability_alloc = float(
                none_to_default(attributes['reliability_alloc'], 0.0))
            self.reliability_goal = float(
                none_to_default(attributes['reliability_goal'], 1.0))
            self.op_time_factor = int(
                none_to_default(attributes['op_time_factor'], 1))
            self.soa_factor = int(none_to_default(attributes['soa_factor'], 1))
            self.weight_factor = float(
                none_to_default(attributes['weight_factor'], 1))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKAllocation.set_attributes().".format(str(_err))

        return _error_code, _msg

    def equal_apportionment(self, n_children, parent_goal):
        """
        Perform an equal apportionment of the reliability goal.

        :param int n_children: the number of immediate children comprising the
                               parent hardware item.
        :param float parent_goal: the reliability goal of the parent hardware
                                  item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        try:
            _weight_i = 1.0 / float(n_children)
            self.reliability_alloc = parent_goal**_weight_i
            self.hazard_rate_alloc = (
                -1.0 * log(self.reliability_alloc) / self.mission_time)
            self.mtbf_alloc = 1.0 / self.hazard_rate_alloc
        except (UnboundLocalError, ValueError, ZeroDivisionError):
            self.reliability_alloc = 0.0
            self.hazard_rate_alloc = 0.0
            self.mtbf_alloc = 0.0
            _return = True

        return _return

    def agree_apportionment(self, n_children, parent_goal):
        """
        Perform an AGREE apportionment of a reliability requirement.

        :param int n_children: the number of immediate children comprising the
                               parent hardware item.
        :param float parent_goal: the reliability goal of the parent hardware
                                  item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _time_i = self.mission_time * self.duty_cycle / 100.0

        try:
            self.mtbf_alloc = ((n_children * self.weight_factor * _time_i) /
                               (-1.0 * self.n_sub_elements * log(parent_goal)))
            self.hazard_rate_alloc = 1.0 / self.mtbf_alloc
            self.reliability_alloc = exp(
                -1.0 * self.hazard_rate_alloc * self.mission_time)
        except (ValueError, ZeroDivisionError):
            self.reliability_alloc = 0.0
            self.hazard_rate_alloc = 0.0
            self.mtbf_alloc = 0.0
            _return = True

        return _return

    def arinc_apportionment(self, system_hr, parent_goal, hazard_rate):
        """
        Perform an ARINC apportionment of the reliability requirement.

        :param float system_hr: the current system hazard rate.
        :param float parent_goal: the goal hazard rate of the parent hardware
                                  item.
        :param float hazard_rate: the current (historic) hazard rate of this
                                  hardware item.
        :param float mission_time: the mission time of the system.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        try:
            self.weight_factor = hazard_rate / system_hr
            self.hazard_rate_alloc = self.weight_factor * parent_goal
            self.mtbf_alloc = 1.0 / self.hazard_rate_alloc
            self.reliability_alloc = exp(
                -1.0 * self.hazard_rate_alloc * self.mission_time)
        except ZeroDivisionError:
            self.weight_factor = 0.0
            self.reliability_alloc = 0.0
            self.hazard_rate_alloc = 0.0
            self.mtbf_alloc = 0.0
            _return = True

        return _return

    def foo_apportionment(self, cum_weight, parent_goal):
        """
        Perform a feasibility of objectives (FOO) apportionment.

        :param int cum_weight: the cumulative weight factor for all subordinate
                               assemblies.
        :param float parent_goal: the failure rate requirement to allocate.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
        _return = False

        # FIXME: Add range check on input factors (1 - 10) in RAMSTKAllocation.foo_apportionment().
        self.weight_factor = (self.int_factor * self.soa_factor *
                              self.op_time_factor * self.env_factor)

        try:
            self.percent_weight_factor = (
                float(self.weight_factor) / float(cum_weight))
            self.hazard_rate_alloc = self.percent_weight_factor * parent_goal
            self.mtbf_alloc = 1.0 / self.hazard_rate_alloc
            self.reliability_alloc = exp(
                -1.0 * self.hazard_rate_alloc * self.mission_time)
        except ZeroDivisionError:
            self.percent_weight_factor = 0.0
            self.reliability_alloc = 0.0
            self.hazard_rate_alloc = 0.0
            self.mtbf_alloc = 0.0
            _return = True

        return _return

    def calculate_goals(self):
        """
        Calculate the other two reliability metrics from the third.

        :return: False if successful or True if an error is encountered
        :rtype: bool
        """
        _return = False

        if self.goal_measure_id == 1:  # Reliability goal
            try:
                self.mtbf_goal = (
                    -1.0 * self.mission_time / log(self.reliability_goal))
                self.hazard_rate_goal = 1.0 / self.mtbf_goal
            except (ValueError, ZeroDivisionError):
                self.hazard_rate_goal = 0.0
                self.mtbf_goal = 0.0
                _return = True

        elif self.goal_measure_id == 2:  # Hazard rate goal
            try:
                self.mtbf_goal = 1.0 / self.hazard_rate_goal
                self.reliability_goal = exp(
                    -1.0 * self.mission_time / self.mtbf_goal)
            except ZeroDivisionError:
                self.mtbf_goal = 0.0
                self.reliability_goal = 0.0
                _return = True

        elif self.goal_measure_id == 3:  # MTBF goal
            try:
                self.hazard_rate_goal = 1.0 / self.mtbf_goal
                self.reliability_goal = exp(
                    -1.0 * self.mission_time / self.mtbf_goal)
            except ZeroDivisionError:
                self.hazard_rate_goal = 0.0
                self.reliability_goal = 0.0
                _return = True

        return _return
