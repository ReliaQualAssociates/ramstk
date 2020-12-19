# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKMethod.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMethod Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKMethod(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to representramstk_method in the RAMSTK Common database."""

    __defaults__ = {
        'description': 'Method Description',
        'method_type': 'unknown',
        'name': 'Method Name'
    }
    __tablename__ = 'ramstk_method'
    __table_args__ = {'extend_existing': True}

    method_id = Column(
        'fld_method_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column('fld_name', String(256), default=__defaults__['name'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    method_type = Column('fld_method_type',
                         String(256),
                         default=__defaults__['method_type'])

    def get_attributes(self):
        """Retrieve current values of the RAMSTKMethod data model attributes.

        :return: {method_id, name, description, method_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'method_id': self.method_id,
            'name': self.name,
            'description': self.description,
            'method_type': self.method_type,
        }

        return _attributes
