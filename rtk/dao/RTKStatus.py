#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKStatus.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKStatus Table
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


class RTKStatus(Base):
    """
    Class to represent the table rtk_status in the RTK Common database.
    """

    __tablename__ = 'rtk_status'
    __table_args__ = {'extend_existing': True}

    status_id = Column('fld_status_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    name = Column('fld_name', String(256), default='Status Name')
    description = Column('fld_description', String(512),
                         default='Status Decription')
    type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Status to retrieve the current values of the RTKStatus data model
        attributes.

        :return: (status_id, name, description, type)
        :rtype: tuple
        """

        _values = (self.status_id, self.name, self.description, self.type)

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
            self.name = str(attributes[0])
            self.description = str(attributes[1])
            self.type = str(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKStatus.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKStatus attributes."

        return _error_code, _msg
