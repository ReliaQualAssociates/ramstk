#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKManufacturer.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKManufacturer Package.
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


class RTKManufacturer(Base):
    """
    Class to represent the table rtk_manufacturer in the RTK Common database.
    """

    __tablename__ = 'rtk_manufacturer'
    __table_args__ = {'extend_existing': True}

    manufacturer_id = Column('fld_manufacturer_id', Integer, primary_key=True,
                             autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Distribution Description')
    location = Column('fld_location', String(512), default='unknown')
    cage_code = Column('fld_cage_code', String(512), default='CAGE Code')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKManufacturer data model
        attributes.

        :return: (manufacturer_id, description, location, cage_code)
        :rtype: tuple
        """

        _values = (self.manufacturer_id, self.description, self.location,
                   self.cage_code)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKManufacturer data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKManufacturer {0:d} attributes.". \
            format(self.manufacturer_id)

        try:
            self.description = str(attributes[0])
            self.location = str(attributes[1])
            self.cage_code = str(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKManufacturer.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKManufacturer attributes."

        return _error_code, _msg
