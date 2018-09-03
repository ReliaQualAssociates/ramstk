# -*- coding: utf-8 -*-
#
#       rtk.dao.RAMSTKReliability.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTKReliability Table Module."""  # pragma: no cover

from sqlalchemy import Column, Float, ForeignKey, Integer, String  # pragma: no cover
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from rtk.Utilities import none_to_default

from rtk.dao.RAMSTKCommonDB import RAMSTK_BASE  # pragma: no cover


class RAMSTKReliability(RAMSTK_BASE):
    """
    Class to represent the rtk_reliability table in the RAMSTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_reliability'
    __table_args__ = {'extend_existing': True}  # pragma: no cover

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    add_adj_factor = Column('fld_add_adj_factor', Float, default=0.0)
    availability_logistics = Column(
        'fld_availability_logistics', Float, default=1.0)
    availability_mission = Column(
        'fld_availability_mission', Float, default=1.0)
    avail_log_variance = Column('fld_avail_log_variance', Float, default=0.0)
    avail_mis_variance = Column('fld_avail_mis_variance', Float, default=0.0)
    failure_distribution_id = Column(
        'fld_failure_distribution_id', Integer, default=0)
    hazard_rate_active = Column('fld_hazard_rate_active', Float, default=0.0)
    hazard_rate_dormant = Column('fld_hazard_rate_dormant', Float, default=0.0)
    hazard_rate_logistics = Column(
        'fld_hazard_rate_logistics', Float, default=0.0)
    hazard_rate_method_id = Column(
        'fld_hazard_rate_method_id', Integer, default=0)
    hazard_rate_mission = Column('fld_hazard_rate_mission', Float, default=0.0)
    hazard_rate_model = Column(
        'fld_hazard_rate_model', String(512), default='')
    hazard_rate_percent = Column('fld_hazard_rate_percent', Float, default=0.0)
    hazard_rate_software = Column(
        'fld_hazard_rate_software', Float, default=0.0)
    hazard_rate_specified = Column(
        'fld_hazard_rate_specified', Float, default=0.0)
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
    reliability_goal_measure_id = Column(
        'fld_reliability_goal_measure_id', Integer, default=0)
    reliability_logistics = Column(
        'fld_reliability_logistics', Float, default=1.0)
    reliability_mission = Column('fld_reliability_mission', Float, default=1.0)
    reliability_log_variance = Column(
        'fld_reliability_log_variance', Float, default=0.0)
    reliability_miss_variance = Column(
        'fld_reliability_mis_variance', Float, default=0.0)
    scale_parameter = Column('fld_scale_parameter', Float, default=0.0)
    shape_parameter = Column('fld_shape_parameter', Float, default=0.0)
    survival_analysis_id = Column(
        'fld_survival_analysis_id', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship(
        'RAMSTKHardware', back_populates='reliability')  # pragma: no cover

    def get_attributes(self):
        """
        Retrieve the RAMSTKReliability attributes from the RAMSTK Program database.

        :return: {hardware_id, add_adj_factor, availability_logistics,
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
                  lambda_b} pairs.
        :rtype: dict
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'add_adj_factor': self.add_adj_factor,
            'availability_logistics': self.availability_logistics,
            'availability_mission': self.availability_mission,
            'avail_log_variance': self.avail_log_variance,
            'avail_mis_variance': self.avail_mis_variance,
            'failure_distribution_id': self.failure_distribution_id,
            'hazard_rate_active': self.hazard_rate_active,
            'hazard_rate_dormant': self.hazard_rate_dormant,
            'hazard_rate_logistics': self.hazard_rate_logistics,
            'hazard_rate_method_id': self.hazard_rate_method_id,
            'hazard_rate_mission': self.hazard_rate_mission,
            'hazard_rate_model': self.hazard_rate_model,
            'hazard_rate_percent': self.hazard_rate_percent,
            'hazard_rate_software': self.hazard_rate_software,
            'hazard_rate_specified': self.hazard_rate_specified,
            'hazard_rate_type_id': self.hazard_rate_type_id,
            'hr_active_variance': self.hr_active_variance,
            'hr_dormant_variance': self.hr_dormant_variance,
            'hr_logistics_variance': self.hr_logistics_variance,
            'hr_mission_variance': self.hr_mission_variance,
            'hr_specified_variance': self.hr_specified_variance,
            'location_parameter': self.location_parameter,
            'mtbf_logistics': self.mtbf_logistics,
            'mtbf_mission': self.mtbf_mission,
            'mtbf_specified': self.mtbf_specified,
            'mtbf_log_variance': self.mtbf_log_variance,
            'mtbf_miss_variance': self.mtbf_miss_variance,
            'mtbf_spec_variance': self.mtbf_spec_variance,
            'mult_adj_factor': self.mult_adj_factor,
            'quality_id': self.quality_id,
            'reliability_goal': self.reliability_goal,
            'reliability_goal_measure_id': self.reliability_goal_measure_id,
            'reliability_logistics': self.reliability_logistics,
            'reliability_mission': self.reliability_mission,
            'reliability_log_variance': self.reliability_log_variance,
            'reliability_miss_variance': self.reliability_miss_variance,
            'scale_parameter': self.scale_parameter,
            'shape_parameter': self.shape_parameter,
            'survival_analysis_id': self.survival_analysis_id,
            'lambda_b': self.lambda_b
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKReliability attributes.

        :param dict attributes: dict of attribute values to assign to the
                                instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKReliability {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.add_adj_factor = float(
                none_to_default(attributes['add_adj_factor'], 0.0))
            self.availability_logistics = float(
                none_to_default(attributes['availability_logistics'], 1.0))
            self.availability_mission = float(
                none_to_default(attributes['availability_mission'], 1.0))
            self.avail_log_variance = float(
                none_to_default(attributes['avail_log_variance'], 0.0))
            self.avail_mis_variance = float(
                none_to_default(attributes['avail_mis_variance'], 0.0))
            self.failure_distribution_id = int(
                none_to_default(attributes['failure_distribution_id'], 0))
            self.hazard_rate_active = float(
                none_to_default(attributes['hazard_rate_active'], 0.0))
            self.hazard_rate_dormant = float(
                none_to_default(attributes['hazard_rate_dormant'], 0.0))
            self.hazard_rate_logistics = float(
                none_to_default(attributes['hazard_rate_logistics'], 0.0))
            self.hazard_rate_method_id = int(
                none_to_default(attributes['hazard_rate_method_id'], 0))
            self.hazard_rate_mission = float(
                none_to_default(attributes['hazard_rate_mission'], 0.0))
            self.hazard_rate_model = str(
                none_to_default(attributes['hazard_rate_model'], ''))
            self.hazard_rate_percent = float(
                none_to_default(attributes['hazard_rate_percent'], 0.0))
            self.hazard_rate_software = float(
                none_to_default(attributes['hazard_rate_software'], 0.0))
            self.hazard_rate_specified = float(
                none_to_default(attributes['hazard_rate_specified'], 0.0))
            self.hazard_rate_type_id = int(
                none_to_default(attributes['hazard_rate_type_id'], 0))
            self.hr_active_variance = float(
                none_to_default(attributes['hr_active_variance'], 0.0))
            self.hr_dormant_variance = float(
                none_to_default(attributes['hr_dormant_variance'], 0.0))
            self.hr_logistics_variance = float(
                none_to_default(attributes['hr_logistics_variance'], 0.0))
            self.hr_mission_variance = float(
                none_to_default(attributes['hr_mission_variance'], 0.0))
            self.hr_specified_variance = float(
                none_to_default(attributes['hr_specified_variance'], 0.0))
            self.location_parameter = float(
                none_to_default(attributes['location_parameter'], 0.0))
            self.mtbf_logistics = float(
                none_to_default(attributes['mtbf_logistics'], 0.0))
            self.mtbf_mission = float(
                none_to_default(attributes['mtbf_mission'], 0.0))
            self.mtbf_specified = float(
                none_to_default(attributes['mtbf_specified'], 0.0))
            self.mtbf_log_variance = float(
                none_to_default(attributes['mtbf_log_variance'], 0.0))
            self.mtbf_miss_variance = float(
                none_to_default(attributes['mtbf_miss_variance'], 0.0))
            self.mtbf_spec_variance = float(
                none_to_default(attributes['mtbf_spec_variance'], 0.0))
            self.mult_adj_factor = float(
                none_to_default(attributes['mult_adj_factor'], 1.0))
            self.quality_id = int(none_to_default(attributes['quality_id'], 0))
            self.reliability_goal = float(
                none_to_default(attributes['reliability_goal'], 0.0))
            self.reliability_goal_measure_id = int(
                none_to_default(attributes['reliability_goal_measure_id'], 0))
            self.reliability_logistics = float(
                none_to_default(attributes['reliability_logistics'], 1.0))
            self.reliability_mission = float(
                none_to_default(attributes['reliability_mission'], 1.0))
            self.reliability_log_variance = float(
                none_to_default(attributes['reliability_log_variance'], 0.0))
            self.reliability_miss_variance = float(
                none_to_default(attributes['reliability_miss_variance'], 0.0))
            self.scale_parameter = float(
                none_to_default(attributes['scale_parameter'], 0.0))
            self.shape_parameter = float(
                none_to_default(attributes['shape_parameter'], 0.0))
            self.survival_analysis_id = int(
                none_to_default(attributes['survival_analysis_id'], 0.0))
            self.lambda_b = float(none_to_default(attributes['lambda_b'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKReliability.set_attributes().".format(_err)

        return _error_code, _msg
