#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKReliability.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKReliability Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
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
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKReliability(Base):
    """
    Class to represent the rtk_reliability table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_reliability'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    add_adj_factor = Column('fld_add_adj_factor', Float, default=0.0)
    availability_logistics = Column('fld_availability_logistics', Float,
                                    default=1.0)
    availability_mission = Column('fld_availability_mission', Float,
                                  default=1.0)
    avail_log_variance = Column('fld_avail_log_variance', Float, default=0.0)
    avail_mis_variance = Column('fld_avail_mis_variance', Float, default=0.0)
    failure_distribution_id = Column('fld_failure_distribution_id', Integer,
                                     default=0)
    hazard_rate_active = Column('fld_hazard_rate_active', Float, default=0.0)
    hazard_rate_dormant = Column('fld_hazard_rate_dormant', Float, default=0.0)
    hazard_rate_logistics = Column('fld_hazard_rate_logistics', Float,
                                   default=0.0)
    hazard_rate_method_id = Column('fld_hazard_rate_method_id', Integer,
                                   default=0)
    hazard_rate_mission = Column('fld_hazard_rate_mission', Float, default=0.0)
    hazard_rate_model = Column('fld_hazard_rate_model', String(512),
                               default='')
    hazard_rate_percent = Column('fld_hazard_rate_percent', Float, default=0.0)
    hazard_rate_software = Column('fld_hazard_rate_software', Float,
                                  default=0.0)
    hazard_rate_specified = Column('fld_hazard_rate_specified', Float,
                                   default=0.0)
    hazard_rate_type_id = Column('fld_hazard_rate_type_id', Integer, default=0)
    hr_active_variance = Column('fld_hr_active_variance', Float, default=0.0)
    hr_dormant_variance = Column('fld_hr_dormant_variance', Float, default=0.0)
    hr_logistics_variance = Column('fld_hr_log_variance', Float, default=0.0)
    hr_mission_variance = Column('fld_hr_mis_variance', Float, default=0.0)
    hr_specified_variance = Column('fld_hr_spec_variance', Float, default=0.0)
    lambda_b = Column('fld_lambda_b', Float, default=0.0)
    location_parameter = Column('fld_location_parameter', Float, default=0.0)
    mtbf_logistics = Column('fld_mtbf_logistics', Float, default=0.0)
    mtbf_mission = Column('fld_mtbf_mission', Float, default=0.0)
    mtbf_specified = Column('fld_mtbf_specified', Float, default=0.0)
    mtbf_log_variance = Column('fld_mtbf_log_variance', Float, default=0.0)
    mtbf_miss_variance = Column('fld_mtbf_mis_variance', Float, default=0.0)
    mtbf_spec_variance = Column('fld_mtbf_spec_variance', Float, default=0.0)
    mult_adj_factor = Column('fld_mult_adj_factor', Float, default=0.0)
    quality_id = Column('fld_quality_id', Integer, default=0)
    reliability_goal = Column('fld_reliability_goal', Float, default=0.0)
    reliability_goal_measure_id = Column('fld_reliability_goal_measure_id',
                                         Integer, default=0)
    reliability_logistics = Column('fld_reliability_logistics', Float,
                                   default=0.0)
    reliability_mission = Column('fld_reliability_mission', Float, default=0.0)
    reliability_log_variance = Column('fld_reliability_log_variance', Float,
                                      default=0.0)
    reliability_miss_variance = Column('fld_reliability_mis_variance', Float,
                                       default=0.0)
    scale_parameter = Column('fld_scale_parameter', Float, default=0.0)
    shape_parameter = Column('fld_shape_parameter', Float, default=0.0)
    survival_analysis_id = Column('fld_survival_analysis_id', Integer,
                                  default=0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='reliability')

    def get_attributes(self):
        """
        Method to retrieve the RTKReliability attributes from the RTK Program
        database.

        :return: (hardware_id, add_adj_factor, availability_logistics,
                  availability_mission, avail_log_variance, avail_mis_variance,
                  failure_distribution_id, hazard_rate_active,
                  hazard_rate_dormant, hazard_rate_logistics,
                  hazard_rate_method_id, hazard_rate_mission,
                  hazard_rate_model, hazard_rate_percent, hazard_rate_software,
                  hazard_rate_specified, hazard_rate_type_id,
                  hr_active_variance, hr_dormant_variance,
                  hr_logistics_variance, hr_mission_variance,
                  hr_specified_variance, location_parameter, mtbf_logistics,
                  mtbf_mission, mtbf_specified, mtbf_log_variance,
                  mtbf_miss_variance, mtbf_spec_variance, mult_adj_factor,
                  quality_id, reliability_goal, reliability_goal_measure_id,
                  reliability_logistics, reliability_mission,
                  reliability_log_variance, reliability_miss_variance,
                  scale_parameter, shape_parameter, survival_analysis_id,
                  lambda_b)
        :rtype: tuple
        """

        _attributes = (self.hardware_id, self.add_adj_factor,
                       self.availability_logistics, self.availability_mission,
                       self.avail_log_variance, self.avail_mis_variance,
                       self.failure_distribution_id, self.hazard_rate_active,
                       self.hazard_rate_dormant, self.hazard_rate_logistics,
                       self.hazard_rate_method_id, self.hazard_rate_mission,
                       self.hazard_rate_model, self.hazard_rate_percent,
                       self.hazard_rate_software, self.hazard_rate_specified,
                       self.hazard_rate_type_id, self.hr_active_variance,
                       self.hr_dormant_variance, self.hr_logistics_variance,
                       self.hr_mission_variance, self.hr_specified_variance,
                       self.location_parameter, self.mtbf_logistics,
                       self.mtbf_mission, self.mtbf_specified,
                       self.mtbf_log_variance, self.mtbf_miss_variance,
                       self.mtbf_spec_variance, self.mult_adj_factor,
                       self.quality_id, self.reliability_goal,
                       self.reliability_goal_measure_id,
                       self.reliability_logistics, self.reliability_mission,
                       self.reliability_log_variance,
                       self.reliability_miss_variance, self.scale_parameter,
                       self.shape_parameter, self.survival_analysis_id,
                       self.lambda_b)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the reliability-specific Hardware attributes.

        :param tuple attributes: tuple of attribute values to assign to the
                                 instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKReliability {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.add_adj_factor = float(attributes[0])
            self.availability_logistics = float(attributes[1])
            self.availability_mission = float(attributes[2])
            self.avail_log_variance = float(attributes[3])
            self.avail_mis_variance = float(attributes[4])
            self.failure_distribution_id = int(attributes[5])
            self.hazard_rate_active = float(attributes[6])
            self.hazard_rate_dormant = float(attributes[7])
            self.hazard_rate_logistics = float(attributes[8])
            self.hazard_rate_method_id = int(attributes[9])
            self.hazard_rate_mission = float(attributes[10])
            self.hazard_rate_model = str(attributes[11])
            self.hazard_rate_percent = float(attributes[12])
            self.hazard_rate_software = float(attributes[13])
            self.hazard_rate_specified = float(attributes[14])
            self.hazard_rate_type_id = int(attributes[15])
            self.hr_active_variance = float(attributes[16])
            self.hr_dormant_variance = float(attributes[17])
            self.hr_logistics_variance = float(attributes[18])
            self.hr_mission_variance = float(attributes[19])
            self.hr_specified_variance = float(attributes[20])
            self.location_parameter = float(attributes[21])
            self.mtbf_logistics = float(attributes[22])
            self.mtbf_mission = float(attributes[23])
            self.mtbf_specified = float(attributes[24])
            self.mtbf_log_variance = float(attributes[25])
            self.mtbf_miss_variance = float(attributes[26])
            self.mtbf_spec_variance = float(attributes[27])
            self.mult_adj_factor = float(attributes[28])
            self.quality_id = int(attributes[29])
            self.reliability_goal = float(attributes[30])
            self.reliability_goal_measure_id = int(attributes[31])
            self.reliability_logistics = float(attributes[32])
            self.reliability_mission = float(attributes[33])
            self.reliability_log_variance = float(attributes[34])
            self.reliability_miss_variance = float(attributes[35])
            self.scale_parameter = float(attributes[36])
            self.shape_parameter = float(attributes[37])
            self.survival_analysis_id = int(attributes[38])
            self.lambda_b = float(attributes[39])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKReliability.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKReliability attributes."

        return _error_code, _msg
