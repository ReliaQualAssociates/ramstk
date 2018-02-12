# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKLoadHistory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKLoadHistory Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKLoadHistory(RTK_BASE):
    """
    Class to represent the table rtk_load_history in the RTK Common database.
    """

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
        LoadHistory to retrieve the current values of the RTKLoadHistory data
        model attributes.

        :return: (load_history_id, description)
        :rtype: tuple
        """

        _values = (self.history_id, self.description)

        return _values

    def set_attributes(self, attributes):
        """
        LoadHistory to set the current values of the RTKLoadHistory data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKLoadHistory {0:d} attributes.". \
            format(self.history_id)

        try:
            self.description = str(
                none_to_default(attributes[0], 'Load History Description'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKLoadHistory.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKLoadHistory attributes."

        return _error_code, _msg
