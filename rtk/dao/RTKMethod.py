#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMethod.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKMethod Package.
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


class RTKMethod(Base):
    """
    Class to represent the table rtk_method in the RTK Common database.
    """

    __tablename__ = 'rtk_method'

    method_id = Column('fld_method_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    name = Column('fld_name', String(256), default='Method Name')
    description = Column('fld_description', String(512),
                         default='Method Description')
    type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKMethod data model
        attributes.

        :return: (method_id, name, description, type)
        :rtype: tuple
        """

        _values = (self.method_id, self.name, self.description, self.type)

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
            self.name = str(attributes[0])
            self.description = str(attributes[1])
            self.type = str(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMethod.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMethod attributes."

        return _error_code, _msg
