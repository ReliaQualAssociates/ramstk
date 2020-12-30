# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKGroup.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKGroup Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKGroup(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent the table ramstk_group in the RAMSTK Common database.

    This table shares a Many-to-One relationship with ramstk_user.
    """

    __defaults__ = {'description': 'Group Description', 'group_type': ''}
    __tablename__ = 'ramstk_group'
    __table_args__ = {'extend_existing': True}

    group_id = Column(
        'fld_group_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    group_type = Column('fld_group_type',
                        String(256),
                        default=__defaults__['group_type'])

    def get_attributes(self):
        """Retrieve current values of the RAMSTKGroup data model attributes.

        :return: {workgroup_id, description, group_type} pairs
        :rtype: dict
        """
        _attributes = {
            'group_id': self.group_id,
            'description': self.description,
            'group_type': self.group_type,
        }

        return _attributes
