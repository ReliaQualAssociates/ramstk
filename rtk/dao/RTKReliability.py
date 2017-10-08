# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKReliability.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKReliability Table
===============================================================================
"""

from sqlalchemy import Column, Float, ForeignKey, \
                       Integer, String              # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKReliability(RTK_BASE):
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
    mult_adj_factor = Column('fld_mult_adj_factor', Float, default=1.0)
    quality_id = Column('fld_quality_id', Integer, default=0)
    reliability_goal = Column('fld_reliability_goal', Float, default=0.0)
    reliability_goal_measure_id = Column('fld_reliability_goal_measure_id',
                                         Integer, default=0)
    reliability_logistics = Column('fld_reliability_logistics', Float,
                                   default=1.0)
    reliability_mission = Column('fld_reliability_mission', Float, default=1.0)
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
        print _attributes
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
            self.add_adj_factor = float(none_to_default(attributes[0], 0.0))
            self.availability_logistics = float(none_to_default(attributes[1],
                                                                1.0))
            self.availability_mission = float(none_to_default(attributes[2],
                                                              1.0))
            self.avail_log_variance = float(none_to_default(attributes[3],
                                                            0.0))
            self.avail_mis_variance = float(none_to_default(attributes[4],
                                                            0.0))
            self.failure_distribution_id = int(none_to_default(attributes[5],
                                                               0))
            self.hazard_rate_active = float(none_to_default(attributes[6],
                                                            0.0))
            self.hazard_rate_dormant = float(none_to_default(attributes[7],
                                                             0.0))
            self.hazard_rate_logistics = float(none_to_default(attributes[8],
                                                               0.0))
            self.hazard_rate_method_id = int(none_to_default(attributes[9], 0))
            self.hazard_rate_mission = float(none_to_default(attributes[10],
                                                             0.0))
            self.hazard_rate_model = str(none_to_default(attributes[11], ''))
            self.hazard_rate_percent = float(none_to_default(attributes[12],
                                                             0.0))
            self.hazard_rate_software = float(none_to_default(attributes[13],
                                                              0.0))
            self.hazard_rate_specified = float(none_to_default(attributes[14],
                                                               0.0))
            self.hazard_rate_type_id = int(none_to_default(attributes[15], 0))
            self.hr_active_variance = float(none_to_default(attributes[16],
                                                            0.0))
            self.hr_dormant_variance = float(none_to_default(attributes[17],
                                                             0.0))
            self.hr_logistics_variance = float(none_to_default(attributes[18],
                                                               0.0))
            self.hr_mission_variance = float(none_to_default(attributes[19],
                                                             0.0))
            self.hr_specified_variance = float(none_to_default(attributes[20],
                                                               0.0))
            self.location_parameter = float(none_to_default(attributes[21],
                                                            0.0))
            self.mtbf_logistics = float(none_to_default(attributes[22], 0.0))
            self.mtbf_mission = float(none_to_default(attributes[23], 0.0))
            self.mtbf_specified = float(none_to_default(attributes[24], 0.0))
            self.mtbf_log_variance = float(none_to_default(attributes[25],
                                                           0.0))
            self.mtbf_miss_variance = float(none_to_default(attributes[26],
                                                            0.0))
            self.mtbf_spec_variance = float(none_to_default(attributes[27],
                                                            0.0))
            self.mult_adj_factor = float(none_to_default(attributes[28], 1.0))
            self.quality_id = int(none_to_default(attributes[29], 0))
            self.reliability_goal = float(none_to_default(attributes[30], 0.0))
            self.reliability_goal_measure_id = int(
                none_to_default(attributes[31], 0))
            self.reliability_logistics = float(none_to_default(attributes[32],
                                                               1.0))
            self.reliability_mission = float(none_to_default(attributes[33],
                                                             1.0))
            self.reliability_log_variance = float(
                none_to_default(attributes[34], 0.0))
            self.reliability_miss_variance = float(
                none_to_default(attributes[35], 0.0))
            self.scale_parameter = float(none_to_default(attributes[36], 0.0))
            self.shape_parameter = float(none_to_default(attributes[37], 0.0))
            self.survival_analysis_id = int(none_to_default(attributes[38],
                                                            0.0))
            self.lambda_b = float(none_to_default(attributes[39], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKReliability.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKReliability attributes."

        return _error_code, _msg
