# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKAllocation.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKAllocation Table."""

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKAllocation(RTK_BASE):
    """
    Class to represent the rtk_allocation table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_allocation'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    availability_alloc = Column('fld_availability_alloc', Float, default=0.0)
    env_factor = Column('fld_env_factor', Integer, default=1)
    goal_measure_id = Column('fld_goal_measure_id', Integer, default=1)
    hazard_rate_alloc = Column('fld_hazard_rate_alloc', Float, default=0.0)
    hazard_rate_goal = Column('fld_hazard_rate_goal', Float, default=0.0)
    included = Column('fld_included', Integer, default=1)
    int_factor = Column('fld_int_factor', Integer, default=1)
    method_id = Column('fld_method_id', Integer, default=1)
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

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='allocation')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKAllocation data model attributes.

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
            'env_factor': self.env_factor,
            'goal_measure_id': self.goal_measure_id,
            'hazard_rate_alloc': self.hazard_rate_alloc,
            'hazard_rate_goal': self.hazard_rate_goal,
            'included': self.included,
            'int_factor': self.int_factor,
            'method_id': self.method_id,
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
        Set the RTKAllocation data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKAllocation {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.availability_alloc = float(
                none_to_default(attributes['availability_alloc'], 0.0))
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
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKAllocation.set_attributes().".format(_err)

        return _error_code, _msg
