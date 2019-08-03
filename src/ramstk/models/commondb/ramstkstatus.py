# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKStatus.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStatus Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKStatus(RAMSTK_BASE):
    """Class to represent ramstk_status in the RAMSTK Common database."""

    __defaults__ = {
        'name': 'Status Name',
        'description': 'Status Decription',
        'status_type': ''
    }
    __tablename__ = 'ramstk_status'
    __table_args__ = {'extend_existing': True}

    status_id = Column(
        'fld_status_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column('fld_name', String(256), default=__defaults__['name'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    status_type = Column('fld_status_type',
                         String(256),
                         default=__defaults__['status_type'])

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKStatus data model attributes.

        :return: {status_id, name, description, status_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'status_id': self.status_id,
            'name': self.name,
            'description': self.description,
            'status_type': self.status_type,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKStatus attributes.

        .. note:: you should pop the status ID entries from the attributes dict
            before passing it to this method.

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
