# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKProgramStatus.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramStatus Table Module."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKProgramStatus(RAMSTK_BASE):
    """
    Class to represent table ramstk_validation in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {
        'cost_remaining': 0,
        'date_status': date.today(),
        'time_remaining': 0.0
    }
    __tablename__ = 'ramstk_program_status'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    status_id = Column(
        'fld_status_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    cost_remaining = Column('fld_cost_remaining', Float, default=0.0)
    date_status = Column(
        'fld_date_status',
        Date,
        unique=True,
        default=date.today(),
    )
    time_remaining = Column('fld_time_remaining', Float, default=0.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='program_status')

    def get_attributes(self):
        """
        Retrieve current values of RAMSTKProgramStatus data model attributes.

        :return: {revision_id, cost_remaining, date_status, time_remaining}
            pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'status_id': self.status_id,
            'cost_remaining': self.cost_remaining,
            'date_status': self.date_status,
            'time_remaining': self.time_remaining,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKProgramInfo attributes.

        .. note:: you should pop the revision ID and status ID entries from the
            attributes dict before passing it to this method.

        :param dict attributes: dict of key:value pairs to assign to the
            instance attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
