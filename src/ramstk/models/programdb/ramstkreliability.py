# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.RAMSTKReliability.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKReliability Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKReliability(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_reliability table in RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        'add_adj_factor': 0.0,
        'availability_logistics': 1.0,
        'availability_mission': 1.0,
        'avail_log_variance': 0.0,
        'avail_mis_variance': 0.0,
        'failure_distribution_id': 0,
        'hazard_rate_active': 0.0,
        'hazard_rate_dormant': 0.0,
        'hazard_rate_logistics': 0.0,
        'hazard_rate_method_id': 0,
        'hazard_rate_mission': 0.0,
        'hazard_rate_model': '',
        'hazard_rate_percent': 0.0,
        'hazard_rate_software': 0.0,
        'hazard_rate_specified': 0.0,
        'hazard_rate_type_id': 0,
        'hr_active_variance': 0.0,
        'hr_dormant_variance': 0.0,
        'hr_logistics_variance': 0.0,
        'hr_mission_variance': 0.0,
        'hr_specified_variance': 0.0,
        'lambda_b': 0.0,
        'location_parameter': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mtbf_specified': 0.0,
        'mtbf_logistics_variance': 0.0,
        'mtbf_mission_variance': 0.0,
        'mtbf_specified_variance': 0.0,
        'mult_adj_factor': 1.0,
        'quality_id': 0,
        'reliability_goal': 0.0,
        'reliability_goal_measure_id': 0,
        'reliability_logistics': 1.0,
        'reliability_mission': 1.0,
        'reliability_log_variance': 0.0,
        'reliability_miss_variance': 0.0,
        'scale_parameter': 0.0,
        'shape_parameter': 0.0,
        'survival_analysis_id': 0
    }
    __tablename__ = 'ramstk_reliability'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False,
    )

    add_adj_factor = Column('fld_add_adj_factor',
                            Float,
                            default=__defaults__['add_adj_factor'])
    availability_logistics = Column(
        'fld_availability_logistics',
        Float,
        default=__defaults__['availability_logistics'],
    )
    availability_mission = Column(
        'fld_availability_mission',
        Float,
        default=__defaults__['availability_mission'],
    )
    avail_log_variance = Column('fld_avail_log_variance',
                                Float,
                                default=__defaults__['avail_log_variance'])
    avail_mis_variance = Column('fld_avail_mis_variance',
                                Float,
                                default=__defaults__['avail_mis_variance'])
    failure_distribution_id = Column(
        'fld_failure_distribution_id',
        Integer,
        default=__defaults__['failure_distribution_id'],
    )
    hazard_rate_active = Column('fld_hazard_rate_active',
                                Float,
                                default=__defaults__['hazard_rate_active'])
    hazard_rate_dormant = Column('fld_hazard_rate_dormant',
                                 Float,
                                 default=__defaults__['hazard_rate_dormant'])
    hazard_rate_logistics = Column(
        'fld_hazard_rate_logistics',
        Float,
        default=__defaults__['hazard_rate_logistics'],
    )
    hazard_rate_method_id = Column(
        'fld_hazard_rate_method_id',
        Integer,
        default=__defaults__['hazard_rate_method_id'],
    )
    hazard_rate_mission = Column('fld_hazard_rate_mission',
                                 Float,
                                 default=__defaults__['hazard_rate_mission'])
    hazard_rate_model = Column(
        'fld_hazard_rate_model',
        String(512),
        default=__defaults__['hazard_rate_model'],
    )
    hazard_rate_percent = Column('fld_hazard_rate_percent',
                                 Float,
                                 default=__defaults__['hazard_rate_percent'])
    hazard_rate_software = Column(
        'fld_hazard_rate_software',
        Float,
        default=__defaults__['hazard_rate_software'],
    )
    hazard_rate_specified = Column(
        'fld_hazard_rate_specified',
        Float,
        default=__defaults__['hazard_rate_specified'])
    hazard_rate_type_id = Column('fld_hazard_rate_type_id',
                                 Integer,
                                 default=__defaults__['hazard_rate_type_id'])
    hr_active_variance = Column('fld_hr_active_variance',
                                Float,
                                default=__defaults__['hr_active_variance'])
    hr_dormant_variance = Column('fld_hr_dormant_variance',
                                 Float,
                                 default=__defaults__['hr_dormant_variance'])
    hr_logistics_variance = Column(
        'fld_hr_log_variance',
        Float,
        default=__defaults__['hr_logistics_variance'])
    hr_mission_variance = Column('fld_hr_mis_variance',
                                 Float,
                                 default=__defaults__['hr_mission_variance'])
    hr_specified_variance = Column(
        'fld_hr_spec_variance',
        Float,
        default=__defaults__['hr_specified_variance'])
    lambda_b = Column('fld_lambda_b', Float, default=__defaults__['lambda_b'])
    location_parameter = Column('fld_location_parameter',
                                Float,
                                default=__defaults__['location_parameter'])
    mtbf_logistics = Column('fld_mtbf_logistics',
                            Float,
                            default=__defaults__['mtbf_logistics'])
    mtbf_mission = Column('fld_mtbf_mission',
                          Float,
                          default=__defaults__['mtbf_mission'])
    mtbf_specified = Column('fld_mtbf_specified',
                            Float,
                            default=__defaults__['mtbf_specified'])
    mtbf_logistics_variance = Column(
        'fld_mtbf_log_variance',
        Float,
        default=__defaults__['mtbf_logistics_variance'])
    mtbf_mission_variance = Column(
        'fld_mtbf_mis_variance',
        Float,
        default=__defaults__['mtbf_mission_variance'])
    mtbf_specified_variance = Column(
        'fld_mtbf_spec_variance',
        Float,
        default=__defaults__['mtbf_specified_variance'])
    mult_adj_factor = Column('fld_mult_adj_factor',
                             Float,
                             default=__defaults__['mult_adj_factor'])
    quality_id = Column('fld_quality_id',
                        Integer,
                        default=__defaults__['quality_id'])
    reliability_goal = Column('fld_reliability_goal',
                              Float,
                              default=__defaults__['reliability_goal'])
    reliability_goal_measure_id = Column(
        'fld_reliability_goal_measure_id',
        Integer,
        default=__defaults__['reliability_goal_measure_id'],
    )
    reliability_logistics = Column(
        'fld_reliability_logistics',
        Float,
        default=__defaults__['reliability_logistics'],
    )
    reliability_mission = Column('fld_reliability_mission',
                                 Float,
                                 default=__defaults__['reliability_mission'])
    reliability_log_variance = Column(
        'fld_reliability_log_variance',
        Float,
        default=__defaults__['reliability_log_variance'])
    reliability_miss_variance = Column(
        'fld_reliability_mis_variance',
        Float,
        default=__defaults__['reliability_miss_variance'])
    scale_parameter = Column('fld_scale_parameter',
                             Float,
                             default=__defaults__['scale_parameter'])
    shape_parameter = Column('fld_shape_parameter',
                             Float,
                             default=__defaults__['shape_parameter'])
    survival_analysis_id = Column('fld_survival_analysis_id',
                                  Integer,
                                  default=__defaults__['survival_analysis_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware: relationship = relationship(
        'RAMSTKHardware',
        back_populates='reliability',
    )

    def get_attributes(self):
        """Retrieve RAMSTKReliability attributes from RAMSTK Program database.

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
            'lambda_b': self.lambda_b,
            'location_parameter': self.location_parameter,
            'mtbf_logistics': self.mtbf_logistics,
            'mtbf_mission': self.mtbf_mission,
            'mtbf_specified': self.mtbf_specified,
            'mtbf_logistics_variance': self.mtbf_logistics_variance,
            'mtbf_mission_variance': self.mtbf_mission_variance,
            'mtbf_specified_variance': self.mtbf_specified_variance,
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
            'survival_analysis_id': self.survival_analysis_id
        }

        return _attributes
