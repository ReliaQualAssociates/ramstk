# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKOpLoad.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKOpLoad Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKOpLoad(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_op_load in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mechanism.
    This table shares a One-to-Many relationship with ramstk_op_stress.
    This table shares a One-to-Many relationship with
    ramstk_test_method.
    """

    __defaults__ = {'description': '', 'damage_model': '', 'priority_id': 0}
    __tablename__ = 'ramstk_op_load'
    __table_args__ = (ForeignKeyConstraint(
        [
            'fld_revision_id', 'fld_hardware_id', 'fld_mode_id',
            'fld_mechanism_id'
        ],
        [
            'ramstk_mechanism.fld_revision_id',
            'ramstk_mechanism.fld_hardware_id', 'ramstk_mechanism.fld_mode_id',
            'ramstk_mechanism.fld_mechanism_id'
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
                     autoincrement=True,
                     nullable=False)

    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    damage_model = Column('fld_damage_model',
                          String(512),
                          default=__defaults__['damage_model'])
    priority_id = Column('fld_priority_id',
                         Integer,
                         default=__defaults__['priority_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    mechanism = relationship(  # type: ignore
        'RAMSTKMechanism',
        back_populates='op_load',
    )
    op_stress = relationship(  # type: ignore
        'RAMSTKOpStress',
        back_populates='op_load',
        cascade='all,delete',
    )
    test_method = relationship(  # type: ignore
        'RAMSTKTestMethod',
        back_populates='op_load',
        cascade='all,delete',
    )

    is_mode = False
    is_mechanism = False
    is_opload = True
    is_opstress = False
    is_testmethod = False

    def get_attributes(self):
        """Retrieve current values of the RAMSTKOpLoad data model attributes.

        :return: {mechanism_id, load_id, description, damage_model,
                  priority_id} pairs
        :rtype: dict
        """
        _attributes = {
            'mechanism_id': self.mechanism_id,
            'load_id': self.load_id,
            'description': self.description,
            'damage_model': self.damage_model,
            'priority_id': self.priority_id
        }

        return _attributes
