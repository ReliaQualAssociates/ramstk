# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMethod.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKMethod Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKMethod(RTK_BASE):
    """
    Class to represent the table rtk_method in the RTK Common database.
    """

    __tablename__ = 'rtk_method'
    __table_args__ = {'extend_existing': True}

    method_id = Column(
        'fld_method_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(256), default='Method Name')
    description = Column(
        'fld_description', String(512), default='Method Description')
    method_type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKMethod data model
        attributes.

        :return: (method_id, name, description, method_type)
        :rtype: tuple
        """

        _values = (self.method_id, self.name, self.description,
                   self.method_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKMethod data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMethod {0:d} attributes.". \
            format(self.method_id)

        try:
            self.name = str(none_to_default(attributes[0], 'Method Name'))
            self.description = str(
                none_to_default(attributes[1], 'Method Description'))
            self.method_type = str(none_to_default(attributes[2], 'unknown'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMethod.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMethod attributes."

        return _error_code, _msg
