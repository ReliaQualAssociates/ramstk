# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKLoadHistory.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKLoadHistory Table."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKLoadHistory(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent the table ramstk_load_history."""

    __defaults__ = {'description': 'Load History Description'}
    __tablename__ = 'ramstk_load_history'
    __table_args__ = {'extend_existing': True}

    history_id = Column('fld_history_id',
                        Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])

    def get_attributes(self):
        """Retrieve current values of RAMSTKLoadHistory data model attributes.

        :return: {load_history_id, description} pairs
        :rtype: dict
        """
        _values = {
            'history_id': self.history_id,
            'description': self.description,
        }

        return _values
