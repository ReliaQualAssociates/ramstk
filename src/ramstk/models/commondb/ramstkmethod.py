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
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKMethod(RAMSTK_BASE):
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
        """
        Retrieve the current values of the RAMSTKMethod data model attributes.

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

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKMethod attributes.

        .. note:: you should pop the method ID entries from the attributes dict
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
