# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKLoadHistory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKLoadHistory Table."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKLoadHistory(RTK_BASE):
    """Class to represent the table rtk_load_history."""

    __tablename__ = 'rtk_load_history'
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
        Retrieve current values of the RTKLoadHistory data model attributes.

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
        Set the current values of the RTKLoadHistory data model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKLoadHistory {0:d} attributes.". \
            format(self.history_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Load History Description'))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKLoadHistory.set_attributes().".format(_err)

        return _error_code, _msg
