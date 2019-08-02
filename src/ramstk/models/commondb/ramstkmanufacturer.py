# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.RAMSTKManufacturer.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKManufacturer Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKManufacturer(RAMSTK_BASE):
    """Class to represent ramstk_manufacturer in the RAMSTK Common database."""

    __defaults__ = {
        'description': 'Manufacturer Description',
        'location': 'unknown',
        'cage_code': 'CAGE Code'
    }
    __tablename__ = 'ramstk_manufacturer'
    __table_args__ = {'extend_existing': True}

    manufacturer_id = Column(
        'fld_manufacturer_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column('fld_description', String(512), default=__defaults__['description'])
    location = Column('fld_location', String(512), default=__defaults__['location'])
    cage_code = Column('fld_cage_code', String(512), default=__defaults__['cage_code'])

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
            'cage_code': self.cage_code,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKManufacturer attributes.

        .. note:: you should pop the manufacturer ID entries from the
            attributes dict before passing it to this method.

        :param dict attributes: dict of key:value pairs to assign to the
            instance attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
