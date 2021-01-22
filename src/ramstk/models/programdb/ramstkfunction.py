# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKFunction.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKFunction Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKFunction(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_function table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-Many relationship with ramstk_mode.
    """

    __defaults__ = {
        'availability_logistics': 1.0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'function_code': 'Function Code',
        'hazard_rate_logistics': 0.0,
        'hazard_rate_mission': 0.0,
        'level': 0,
        'mmt': 0.0,
        'mcmt': 0.0,
        'mpmt': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.0,
        'name': 'Function Name',
        'parent_id': 0,
        'remarks': '',
        'safety_critical': 0,
        'total_mode_count': 0,
        'total_part_count': 0,
        'type_id': 0
    }
    __tablename__ = 'ramstk_function'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    function_id = Column(
        'fld_function_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

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
    cost = Column('fld_cost', Float, default=__defaults__['cost'])
    function_code = Column(
        'fld_function_code',
        String(16),
        default=__defaults__['function_code'],
    )
    hazard_rate_logistics = Column(
        'fld_hazard_rate_logistics',
        Float,
        default=__defaults__['hazard_rate_logistics'],
    )
    hazard_rate_mission = Column('fld_hazard_rate_mission',
                                 Float,
                                 default=__defaults__['hazard_rate_mission'])
    level = Column('fld_level', Integer, default=__defaults__['level'])
    mmt = Column('fld_mmt', Float, default=__defaults__['mmt'])
    mcmt = Column('fld_mcmt', Float, default=__defaults__['mcmt'])
    mpmt = Column('fld_mpmt', Float, default=__defaults__['mpmt'])
    mtbf_logistics = Column('fld_mtbf_logistics',
                            Float,
                            default=__defaults__['mtbf_logistics'])
    mtbf_mission = Column('fld_mtbf_mission',
                          Float,
                          default=__defaults__['mtbf_mission'])
    mttr = Column('fld_mttr', Float, default=__defaults__['mttr'])
    name = Column('fld_name', String(256), default=__defaults__['name'])
    parent_id = Column('fld_parent_id',
                       Integer,
                       default=__defaults__['parent_id'])
    remarks = Column('fld_remarks', String, default=__defaults__['remarks'])
    safety_critical = Column('fld_safety_critical',
                             Integer,
                             default=__defaults__['safety_critical'])
    total_mode_count = Column('fld_total_mode_count',
                              Integer,
                              default=__defaults__['total_mode_count'])
    total_part_count = Column('fld_total_part_count',
                              Integer,
                              default=__defaults__['total_part_count'])
    type_id = Column('fld_type_id', Integer, default=__defaults__['type_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship(  # type: ignore
        'RAMSTKRevision', back_populates='function')
    hazard = relationship(  # type: ignore
        'RAMSTKHazardAnalysis',
        back_populates='function',
        cascade='all,delete')

    def get_attributes(self):
        """Retrieve current values of the RAMSTKFunction data model attributes.

        :return: {revision_id, function_id, availability_logistics,
                  availability_mission, cost, function_code,
                  hazard_rate_logistics, hazard_rate_mission, level, mmt, mcmt,
                  mpmt, mtbf_logistics, mtbf_mission, mttr, name, parent_id,
                  remarks, safety_critical, total_mode_count, total_part_count,
                  type_id} pairs.
        :rtype: tuple
        """
        _values = {
            'revision_id': self.revision_id,
            'function_id': self.function_id,
            'availability_logistics': self.availability_logistics,
            'availability_mission': self.availability_mission,
            'cost': self.cost,
            'function_code': self.function_code,
            'hazard_rate_logistics': self.hazard_rate_logistics,
            'hazard_rate_mission': self.hazard_rate_mission,
            'level': self.level,
            'mmt': self.mmt,
            'mcmt': self.mcmt,
            'mpmt': self.mpmt,
            'mtbf_logistics': self.mtbf_logistics,
            'mtbf_mission': self.mtbf_mission,
            'mttr': self.mttr,
            'name': self.name,
            'parent_id': self.parent_id,
            'remarks': self.remarks,
            'safety_critical': self.safety_critical,
            'total_mode_count': self.total_mode_count,
            'total_part_count': self.total_part_count,
            'type_id': self.type_id,
        }

        return _values
