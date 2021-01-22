# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKProgramStatus.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramStatus Table Module."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKProgramStatus(RAMSTK_BASE, RAMSTKBaseTable):
    """Class represent table ramstk_program_status in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {
        'cost_remaining': 0.0,
        'date_status': date.today(),
        'time_remaining': 0.0
    }
    __tablename__ = 'ramstk_program_status'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id',
                         Integer,
                         ForeignKey('ramstk_revision.fld_revision_id'),
                         nullable=False)
    status_id = Column('fld_status_id',
                       Integer,
                       primary_key=True,
                       autoincrement=True,
                       nullable=False)

    cost_remaining = Column('fld_cost_remaining', Float, default=0.0)
    date_status = Column('fld_date_status',
                         Date,
                         unique=True,
                         default=date.today())
    time_remaining = Column('fld_time_remaining', Float, default=0.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision: relationship = relationship(
        'RAMSTKRevision',
        back_populates='program_status',
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKProgramStatus model attributes.

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
