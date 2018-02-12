# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKStatus.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKStatus Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKStatus(RTK_BASE):
    """
    Class to represent the table rtk_status in the RTK Common database.
    """

    __tablename__ = 'rtk_status'
    __table_args__ = {'extend_existing': True}

    status_id = Column(
        'fld_status_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(256), default='Status Name')
    description = Column(
        'fld_description', String(512), default='Status Decription')
    status_type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Status to retrieve the current values of the RTKStatus data model
        attributes.

        :return: (status_id, name, description, status_type)
        :rtype: tuple
        """

        _values = (self.status_id, self.name, self.description,
                   self.status_type)

        return _values

    def set_attributes(self, attributes):
        """
        Status to set the current values of the RTKStatus data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKStatus {0:d} attributes.". \
            format(self.status_id)

        try:
            self.name = str(none_to_default(attributes[0], 'Status Name'))
            self.description = str(
                none_to_default(attributes[1], 'Status Description'))
            self.status_type = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKStatus.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKStatus attributes."

        return _error_code, _msg
