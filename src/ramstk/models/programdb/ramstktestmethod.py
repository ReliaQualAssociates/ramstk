# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKTestMethod.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTestMethod Table."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKTestMethod(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_test_method in RAMSTK Program database.

    This table shared a Many-to-One relationship with ramstk_op_stress.
    """

    __defaults__ = {
        'description': '',
        'boundary_conditions': '',
        'remarks': ''
    }
    __tablename__ = 'ramstk_test_method'
    __table_args__ = (ForeignKeyConstraint(
        [
            'fld_revision_id', 'fld_hardware_id', 'fld_mode_id',
            'fld_mechanism_id', 'fld_load_id'
        ],
        [
            'ramstk_op_load.fld_revision_id', 'ramstk_op_load.fld_hardware_id',
            'ramstk_op_load.fld_mode_id', 'ramstk_op_load.fld_mechanism_id',
            'ramstk_op_load.fld_load_id'
        ],
    ), {
        'extend_existing': True
    })

    revision_id = Column('fld_revision_id',
                         Integer,
                         primary_key=True,
                         nullable=False)
    hardware_id = Column('fld_hardware_id',
                         Integer,
                         primary_key=True,
                         default=-1,
                         nullable=False)
    mode_id = Column('fld_mode_id', Integer, primary_key=True, nullable=False)
    mechanism_id = Column('fld_mechanism_id',
                          Integer,
                          primary_key=True,
                          nullable=False)
    load_id = Column('fld_load_id',
                     Integer,
                     primary_key=True,
                     nullable=False,
                     unique=True)
    test_id = Column('fld_test_id',
                     Integer,
                     primary_key=True,
                     autoincrement=True,
                     nullable=False)

    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    boundary_conditions = Column('fld_boundary_conditions',
                                 String(512),
                                 default=__defaults__['boundary_conditions'])
    remarks = Column('fld_remarks', String, default=__defaults__['remarks'])

    # Define the relationships to other tables in the RAMSTK Program database.
    op_load: relationship = relationship(
        'RAMSTKOpLoad',
        back_populates='test_method',
    )

    is_mode = False
    is_mechanism = False
    is_opload = False
    is_opstress = False
    is_testmethod = True

    def get_attributes(self):
        """Retrieve current values of RAMSTKTestMethod data model attributes.

        :return: {stress_id, test_id, description, boundary_conditions,
                  remarks} pairs
        :rtype: dict
        """
        _attributes = {
            'load_id': self.load_id,
            'test_id': self.test_id,
            'description': self.description,
            'boundary_conditions': self.boundary_conditions,
            'remarks': self.remarks
        }

        return _attributes
