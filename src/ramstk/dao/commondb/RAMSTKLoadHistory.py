# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKLoadHistory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKLoadHistory Table."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKLoadHistory(RAMSTK_BASE):
    """Class to represent the table ramstk_load_history."""

    __tablename__ = 'ramstk_load_history'
    __table_args__ = {'extend_existing': True}

    history_id = Column(
        'fld_load_history_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Load History Description')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKLoadHistory data model attributes.

        :return: {load_history_id, description} pairs
        :rtype: dict
        """
        _values = {
            'history_id': self.history_id,
            'description': self.description
        }

        return _values

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKLoadHistory data model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKLoadHistory {0:d} attributes.". \
            format(self.history_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Load History Description'))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKLoadHistory.set_attributes().".format(_err)

        return _error_code, _msg
