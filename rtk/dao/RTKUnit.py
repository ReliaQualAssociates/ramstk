# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKUnit.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKUnit Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String        # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKUnit(RTK_BASE):
    """
    Class to represent the table rtk_unit in the RTK Common database.
    """

    __tablename__ = 'rtk_unit'
    __table_args__ = {'extend_existing': True}

    unit_id = Column('fld_unit_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)
    code = Column('fld_code', String(256), default='Unit Code')
    description = Column('fld_description', String(512),
                         default='Unit Description')
    unit_type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKUnit data model
        attributes.

        :return: (unit_id, code, description, unit_type)
        :rtype: tuple
        """

        _values = (self.unit_id, self.code, self.description, self.unit_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKUnit data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKUnit {0:d} attributes.". \
            format(self.unit_id)

        try:
            self.code = str(none_to_default(attributes[0], 'Unit Code'))
            self.description = str(none_to_default(attributes[2],
                                                   'Unit Description'))
            self.unit_type = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKUnit.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKUnit attributes."

        return _error_code, _msg
