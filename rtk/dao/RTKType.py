# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKType.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKType Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKType(RTK_BASE):
    """
    Class to represent the table rtk_type in the RTK Common database.
    """

    __tablename__ = 'rtk_type'
    __table_args__ = {'extend_existing': True}

    type_id = Column(
        'fld_model_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    code = Column('fld_code', String(256), default='Type Code')
    description = Column(
        'fld_description', String(512), default='Type Description')
    type_type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKType data model
        attributes.

        :return: (type_id, description, type_type)
        :rtype: tuple
        """

        _values = (self.type_id, self.code, self.description, self.type_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKType data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKType {0:d} attributes.". \
            format(self.type_id)

        try:
            self.code = str(none_to_default(attributes[0], ''))
            self.description = str(none_to_default(attributes[1], ''))
            self.type_type = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKType.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKType attributes."

        return _error_code, _msg
