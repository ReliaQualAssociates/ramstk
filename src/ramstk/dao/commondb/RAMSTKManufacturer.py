# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKManufacturer.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKManufacturer Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKManufacturer(RAMSTK_BASE):
    """Class to represent the table ramstk_manufacturer in the RAMSTK Common database."""

    __tablename__ = 'ramstk_manufacturer'
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
        Retrieve the current values of RAMSTKManufacturer data model attributes.

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
        Set the current values of the RAMSTKManufacturer data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKManufacturer {0:d} attributes.". \
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
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
