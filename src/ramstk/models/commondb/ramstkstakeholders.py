# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKStakeholders.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStakeholders Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKStakeholders(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_stakeholders in the RAMSTK Common database."""

    __defaults__ = {'stakeholder': 'Stakeholder'}
    __tablename__ = 'ramstk_stakeholders'
    __table_args__ = {'extend_existing': True}

    stakeholders_id = Column(
        'fld_stakeholders_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    stakeholder = Column('fld_stakeholder',
                         String(512),
                         default=__defaults__['stakeholder'])

    def get_attributes(self):
        """Retrieve current values of RAMSTKStakeholders data model attributes.

        :return: {stakeholders_id, stakeholder} pairs.
        :rtype: dict
        """
        _attributes = {
            'stakeholders_id': self.stakeholders_id,
            'stakeholder': self.stakeholder,
        }

        return _attributes
