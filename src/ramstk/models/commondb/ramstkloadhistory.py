# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKLoadHistory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKLoadHistory Table."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKLoadHistory(RAMSTK_BASE):
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
        """
        Retrieve current values of the RAMSTKLoadHistory data model attributes.

        :return: {load_history_id, description} pairs
        :rtype: dict
        """
        _values = {
            'history_id': self.history_id,
            'description': self.description,
        }

        return _values

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKLoadHistory attributes.

        .. note:: you should pop the history ID entries from the attributes
            dict before passing it to this method.

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
