# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKType.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKType Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKType(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent tramstk_type in the RAMSTK Common database."""

    __defaults__ = {
        'code': 'Type Code',
        'description': 'Type Description',
        'type_type': 'unknown'
    }
    __tablename__ = 'ramstk_type'
    __table_args__ = {'extend_existing': True}

    type_id = Column(
        'fld_type_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    code = Column('fld_code', String(256), default=__defaults__['code'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    type_type = Column('fld_type',
                       String(256),
                       default=__defaults__['type_type'])

    def get_attributes(self):
        """Retrieve the current values of the RAMSTKType data model attributes.

        :return: {type_id, description, type_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'type_id': self.type_id,
            'code': self.code,
            'description': self.description,
            'type_type': self.type_type,
        }

        return _attributes
