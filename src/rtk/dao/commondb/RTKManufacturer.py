# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKManufacturer.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKManufacturer Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKManufacturer(RTK_BASE):
    """Class to represent the table rtk_manufacturer in the RTK Common database."""

    __tablename__ = 'rtk_manufacturer'
    __table_args__ = {'extend_existing': True}

    manufacturer_id = Column(
        'fld_manufacturer_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Manufacturer Description')
    location = Column('fld_location', String(512), default='unknown')
    cage_code = Column('fld_cage_code', String(512), default='CAGE Code')

    def get_attributes(self):
        """
        Retrieve the current values of RTKManufacturer data model attributes.

        :return: {manufacturer_id, description, location, cage_code} pairs
        :rtype: dict
        """
        _attributes = {
            'manufacturer_id': self.manufacturer_id,
            'description': self.description,
            'location': self.location,
            'cage_code': self.cage_code
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKManufacturer data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKManufacturer {0:d} attributes.". \
            format(self.manufacturer_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Manufacturer Description'))
            self.location = str(
                none_to_default(attributes['location'], 'unknown'))
            self.cage_code = str(
                none_to_default(attributes['cage_code'], 'CAGE Code'))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
