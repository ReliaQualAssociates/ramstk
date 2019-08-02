# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKRPN.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKRPN Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKRPN(RAMSTK_BASE):
    """Class to represent table ramstk_rpn in the RAMSTK Common database."""

    __defaults__ = {
        'name': 'RPN Name',
        'description': 'RPN Description',
        'rpn_type': '',
        'value': 0
    }
    __tablename__ = 'ramstk_rpn'
    __table_args__ = {'extend_existing': True}

    rpn_id = Column(
        'fld_rpn_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column('fld_name', String(512), default=__defaults__['name'])
    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    rpn_type = Column('fld_rpn_type',
                      String(256),
                      default=__defaults__['rpn_type'])
    value = Column('fld_value', Integer, default=__defaults__['value'])

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKRPN data model attributes.

        :return: {}rpn_id, name, description, rpn_type, value} key:value pairs
        :rtype: dict
        """
        _values = {
            'rpn_id': self.rpn_id,
            'name': self.name,
            'description': self.description,
            'rpn_type': self.rpn_type,
            'value': self.value,
        }

        return _values

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKSiteInfo attributes.

        .. note:: you should pop the site ID entries from the attributes dict
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
