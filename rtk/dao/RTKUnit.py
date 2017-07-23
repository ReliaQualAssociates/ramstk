#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKUnit.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKUnit Table
==============================
"""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
try:
    import Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKUnit(Base):
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
    type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKUnit data model
        attributes.

        :return: (unit_id, code, description, type)
        :rtype: tuple
        """

        _values = (self.unit_id, self.code, self.description, self.type)

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
            self.code = str(attributes[0])
            self.description = str(attributes[2])
            self.type = str(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKUnit.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKUnit attributes."

        return _error_code, _msg
