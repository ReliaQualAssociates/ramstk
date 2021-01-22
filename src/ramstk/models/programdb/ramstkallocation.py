# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.programdb.RAMSTKAllocation.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKAllocation Table."""

# Third Party Imports
# noinspection PyPackageRequirements
from sqlalchemy import Column, Float, ForeignKey, Integer
# noinspection PyPackageRequirements
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKAllocation(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_allocation table in RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        'availability_alloc': 0.0,
        'duty_cycle': 100.0,
        'env_factor': 1,
        'goal_measure_id': 1,
        'hazard_rate_alloc': 0.0,
        'hazard_rate_goal': 0.0,
        'included': 1,
        'int_factor': 1,
        'allocation_method_id': 1,
        'mission_time': 100.0,
        'mtbf_alloc': 0.0,
        'mtbf_goal': 0.0,
        'n_sub_systems': 1,
        'n_sub_elements': 1,
        'parent_id': 1,
        'percent_weight_factor': 0.0,
        'reliability_alloc': 1.0,
        'reliability_goal': 1.0,
        'op_time_factor': 1,
        'soa_factor': 1,
        'weight_factor': 1.0
    }
    __tablename__ = 'ramstk_allocation'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False,
    )

    availability_alloc = Column('fld_availability_alloc',
                                Float,
                                default=__defaults__['availability_alloc'])
    duty_cycle = Column('fld_duty_cycle',
                        Float,
                        default=__defaults__['duty_cycle'])
    env_factor = Column('fld_env_factor',
                        Integer,
                        default=__defaults__['env_factor'])
    goal_measure_id = Column('fld_goal_measure_id',
                             Integer,
                             default=__defaults__['goal_measure_id'])
    hazard_rate_alloc = Column('fld_hazard_rate_alloc',
                               Float,
                               default=__defaults__['hazard_rate_alloc'])
    hazard_rate_goal = Column('fld_hazard_rate_goal',
                              Float,
                              default=__defaults__['hazard_rate_goal'])
    included = Column('fld_included',
                      Integer,
                      default=__defaults__['included'])
    int_factor = Column('fld_int_factor',
                        Integer,
                        default=__defaults__['int_factor'])
    allocation_method_id = Column('fld_allocation_method_id',
                                  Integer,
                                  default=__defaults__['allocation_method_id'])
    mission_time = Column('fld_mission_time',
                          Float,
                          default=__defaults__['mission_time'])
    mtbf_alloc = Column('fld_mtbf_alloc',
                        Float,
                        default=__defaults__['mtbf_alloc'])
    mtbf_goal = Column('fld_mtbf_goal',
                       Float,
                       default=__defaults__['mtbf_goal'])
    n_sub_systems = Column('fld_n_sub_systems',
                           Integer,
                           default=__defaults__['n_sub_systems'])
    n_sub_elements = Column('fld_n_sub_elements',
                            Integer,
                            default=__defaults__['n_sub_elements'])
    parent_id = Column('fld_parent_id',
                       Integer,
                       default=__defaults__['parent_id'])
    percent_weight_factor = Column(
        'fld_percent_weight_factor',
        Float,
        default=__defaults__['percent_weight_factor'],
    )
    reliability_alloc = Column('fld_reliability_alloc',
                               Float,
                               default=__defaults__['reliability_alloc'])
    reliability_goal = Column('fld_reliability_goal',
                              Float,
                              default=__defaults__['reliability_goal'])
    op_time_factor = Column('fld_op_time_factor',
                            Integer,
                            default=__defaults__['op_time_factor'])
    soa_factor = Column('fld_soa_factor',
                        Integer,
                        default=__defaults__['soa_factor'])
    weight_factor = Column('fld_weight_factor',
                           Integer,
                           default=__defaults__['weight_factor'])

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship(  # type: ignore
        'RAMSTKHardware', back_populates='allocation')

    def get_attributes(self):
        """Retrieve current values of RAMSTKAllocation data model attributes.

        :return: {revision_id, hardware_id, availability_alloc, env_factor,
                  goal_measure_id, hazard_rate_alloc, hazard_rate_goal,
                  included, int_factor, method_id, mtbf_alloc, mtbf_goal,
                  n_sub_systems, n_sub_elements, parent_id, percent_wt_factor,
                  reliability_alloc, reliability_goal, op_time_factor,
                  soa_factor, weight_factor} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'hardware_id': self.hardware_id,
            'availability_alloc': self.availability_alloc,
            'duty_cycle': self.duty_cycle,
            'env_factor': self.env_factor,
            'goal_measure_id': self.goal_measure_id,
            'hazard_rate_alloc': self.hazard_rate_alloc,
            'hazard_rate_goal': self.hazard_rate_goal,
            'included': self.included,
            'int_factor': self.int_factor,
            'allocation_method_id': self.allocation_method_id,
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
            'weight_factor': self.weight_factor,
        }

        return _attributes
