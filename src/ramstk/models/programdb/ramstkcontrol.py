# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.ramstkcontrol.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKControl Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKControl(RAMSTK_BASE, RAMSTKBaseTable):
    """
    Class to represent the table ramstk_control in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_cause.
    """

    __defaults__ = {'description': '', 'type_id': ''}
    __tablename__ = 'ramstk_control'
    __table_args__ = {'extend_existing': True}

    cause_id = Column(
        'fld_cause_id',
        Integer,
        ForeignKey('ramstk_cause.fld_cause_id'),
        primary_key=True,
        nullable=False,
    )
    control_id = Column(
        'fld_control_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    type_id = Column('fld_type_id',
                     String(512),
                     default=__defaults__['type_id'])

    # Define the relationships to other tables in the RAMSTK Program database.
    cause = relationship('RAMSTKCause', back_populates='control')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = True
    is_action = False

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKControl data model attributes.

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
