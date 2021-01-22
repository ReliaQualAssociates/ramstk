# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKProgramImfo.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramInfo Table Module."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from sqlalchemy import Column, Date, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKProgramInfo(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_program_info in RAMSTK Program database.

    This table has a one-to-one relationship with RAMSTKProgramStatus.
    """

    __defaults__ = {
        'function_active': 1,
        'requirement_active': 1,
        'hardware_active': 1,
        'software_active': 0,
        'rcm_active': 0,
        'testing_active': 0,
        'incident_active': 0,
        'survival_active': 0,
        'vandv_active': 1,
        'hazard_active': 1,
        'stakeholder_active': 1,
        'allocation_active': 1,
        'similar_item_active': 1,
        'fmea_active': 1,
        'pof_active': 1,
        'rbd_active': 0,
        'fta_active': 0,
        'created_on': date.today(),
        'created_by': '',
        'last_saved': date.today(),
        'last_saved_by': ''
    }
    __tablename__ = 'ramstk_program_info'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id',
                         Integer,
                         primary_key=True,
                         autoincrement=True,
                         nullable=False)
    function_active = Column('fld_function_active',
                             Integer,
                             default=__defaults__['function_active'])
    requirement_active = Column('fld_requirement_active',
                                Integer,
                                default=__defaults__['requirement_active'])
    hardware_active = Column('fld_hardware_active',
                             Integer,
                             default=__defaults__['hardware_active'])
    software_active = Column('fld_software_active',
                             Integer,
                             default=__defaults__['software_active'])
    rcm_active = Column('fld_rcm_active',
                        Integer,
                        default=__defaults__['rcm_active'])
    testing_active = Column('fld_testing_active',
                            Integer,
                            default=__defaults__['testing_active'])
    incident_active = Column('fld_incident_active',
                             Integer,
                             default=__defaults__['incident_active'])
    survival_active = Column('fld_survival_active',
                             Integer,
                             default=__defaults__['survival_active'])
    vandv_active = Column('fld_vandv_active',
                          Integer,
                          default=__defaults__['vandv_active'])
    hazard_active = Column('fld_hazard_active',
                           Integer,
                           default=__defaults__['hazard_active'])
    stakeholder_active = Column('fld_stakeholder_active',
                                Integer,
                                default=__defaults__['stakeholder_active'])
    allocation_active = Column('fld_allocation_active',
                               Integer,
                               default=__defaults__['allocation_active'])
    similar_item_active = Column('fld_similar_item_active',
                                 Integer,
                                 default=__defaults__['similar_item_active'])
    fmea_active = Column('fld_fmea_active',
                         Integer,
                         default=__defaults__['fmea_active'])
    pof_active = Column('fld_pof_active',
                        Integer,
                        default=__defaults__['pof_active'])
    rbd_active = Column('fld_rbd_active',
                        Integer,
                        default=__defaults__['rbd_active'])
    fta_active = Column('fld_fta_active',
                        Integer,
                        default=__defaults__['fta_active'])
    created_on = Column('fld_created_on',
                        Date,
                        default=__defaults__['created_on'])
    created_by = Column('fld_created_by',
                        String(512),
                        default=__defaults__['created_by'])
    last_saved = Column('fld_last_saved_on',
                        Date,
                        default=__defaults__['last_saved'])
    last_saved_by = Column('fld_last_saved_by',
                           String(512),
                           default=__defaults__['last_saved_by'])

    def get_attributes(self):
        """Retrieve current values of RAMSTKProgramInfo data model attributes.

        :return: {revision_id, function_active, requirement_active,
                  hardware_active, software_active, vandv_active,
                  testing_active, fraca_active, survival_active, rcm_active,
                  rbd_active, fta_active, created_on, created_by, last_saved,
                  last_saved_by, method} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'function_active': self.function_active,
            'requirement_active': self.requirement_active,
            'hardware_active': self.hardware_active,
            'software_active': self.software_active,
            'rcm_active': self.rcm_active,
            'testing_active': self.testing_active,
            'incident_active': self.incident_active,
            'survival_active': self.survival_active,
            'vandv_active': self.vandv_active,
            'fmea_active': self.fmea_active,
            'pof_active': self.pof_active,
            'hazard_active': self.hazard_active,
            'stakeholder_active': self.stakeholder_active,
            'allocation_active': self.allocation_active,
            'similar_item_active': self.similar_item_active,
            'rbd_active': self.rbd_active,
            'fta_active': self.fta_active,
            'created_on': self.created_on,
            'created_by': self.created_by,
            'last_saved': self.last_saved,
            'last_saved_by': self.last_saved_by,
        }

        return _attributes
