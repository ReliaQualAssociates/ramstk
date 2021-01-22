# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.ramstkcontrol.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKControl Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKControl(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_control in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_cause.
    """

    __defaults__ = {'description': '', 'type_id': ''}
    __tablename__ = 'ramstk_control'
    __table_args__ = (ForeignKeyConstraint(
        [
            'fld_revision_id', 'fld_hardware_id', 'fld_mode_id',
            'fld_mechanism_id', 'fld_cause_id'
        ],
        [
            'ramstk_cause.fld_revision_id', 'ramstk_cause.fld_hardware_id',
            'ramstk_cause.fld_mode_id', 'ramstk_cause.fld_mechanism_id',
            'ramstk_cause.fld_cause_id'
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
    cause_id = Column('fld_cause_id',
                      Integer,
                      primary_key=True,
                      nullable=False,
                      unique=True)
    control_id = Column('fld_control_id',
                        Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)

    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    type_id = Column('fld_type_id',
                     String(512),
                     default=__defaults__['type_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    cause = relationship(  # type: ignore
        'RAMSTKCause', back_populates='control')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = True
    is_action = False

    def get_attributes(self):
        """Retrieve current values of the RAMSTKControl data model attributes.

        :return: {cause_id, control_id, description, type_id} pairs.
        :rtype: dict
        """
        _attributes = {
            'cause_id': self.cause_id,
            'control_id': self.control_id,
            'description': self.description,
            'type_id': self.type_id,
        }

        return _attributes
