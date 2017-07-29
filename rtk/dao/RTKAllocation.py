#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKAllocation.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKAllocation Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKAllocation(RTK_BASE):
    """
    Class to represent the rtk_allocation table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_allocation'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

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
    percent_weight_factor = Column('fld_percent_weight_factor', Float,
                                   default=0.0)
    reliability_alloc = Column('fld_reliability_alloc', Float, default=0.0)
    reliability_goal = Column('fld_reliability_goal', Float, default=1.0)
    op_time_factor = Column('fld_op_time_factor', Integer, default=1)
    soa_factor = Column('fld_soa_factor', Integer, default=1)
    weight_factor = Column('fld_weight_factor', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='allocation')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKAllocation data model
        attributes.

        :return: (hardware_id, availability_alloc, env_factor, goal_measure_id,
                  hazard_rate_alloc, hazard_rate_goal, included, int_factor,
                  method_id, mtbf_alloc, mtbf_goal, n_sub_systems,
                  n_sub_elements, parent_id, percent_wt_factor,
                  reliability_alloc, reliability_goal, op_time_factor,
                  soa_factor, weight_factor)
        :rtype: tuple
        """

        _attributes = (self.hardware_id, self.availability_alloc,
                       self.env_factor, self.goal_measure_id,
                       self.hazard_rate_alloc, self.hazard_rate_goal,
                       self.included, self.int_factor, self.method_id,
                       self.mtbf_alloc, self.mtbf_goal, self.n_sub_systems,
                       self.n_sub_elements, self.parent_id,
                       self.percent_weight_factor, self.reliability_alloc,
                       self.reliability_goal, self.op_time_factor,
                       self.soa_factor, self.weight_factor)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKAllocation data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKAllocation {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.availability_alloc = float(attributes[0])
            self.env_factor = int(attributes[1])
            self.goal_measure_id = int(attributes[2])
            self.hazard_rate_alloc = float(attributes[3])
            self.hazard_rate_goal = float(attributes[4])
            self.included = int(attributes[5])
            self.int_factor = int(attributes[6])
            self.method_id = int(attributes[7])
            self.mtbf_alloc = float(attributes[8])
            self.mtbf_goal = float(attributes[9])
            self.n_sub_systems = int(attributes[10])
            self.n_sub_elements = int(attributes[11])
            self.parent_id = int(attributes[12])
            self.percent_weight_factor = float(attributes[13])
            self.reliability_alloc = float(attributes[14])
            self.reliability_goal = float(attributes[15])
            self.op_time_factor = int(attributes[16])
            self.soa_factor = int(attributes[17])
            self.weight_factor = float(attributes[18])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKAllocation.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKAllocation attributes."

        return _error_code, _msg
