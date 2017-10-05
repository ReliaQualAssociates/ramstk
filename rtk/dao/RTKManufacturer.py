# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKManufacturer.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKManufacturer Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String      # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKManufacturer(RTK_BASE):
    """
    Class to represent the table rtk_manufacturer in the RTK Common database.
    """

    __tablename__ = 'rtk_manufacturer'
    __table_args__ = {'extend_existing': True}

    manufacturer_id = Column('fld_manufacturer_id', Integer, primary_key=True,
                             autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Manufacturer Description')
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
            self.description = str(none_to_default(attributes[0],
                                                   'Manufacturer Description'))
            self.location = str(none_to_default(attributes[1], 'unknown'))
            self.cage_code = str(none_to_default(attributes[2], 'CAGE Code'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKManufacturer.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKManufacturer attributes."

        return _error_code, _msg
