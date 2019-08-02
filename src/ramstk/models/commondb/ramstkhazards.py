# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKHazards.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHazard Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKHazards(RAMSTK_BASE):
    """Class to represent the table ramstk_hazard in the RAMSTK Common database."""

    __defaults__ = {
        'hazard_category': 'Hazard Category',
        'hazard_subcategory': 'Hazard Subcategory'
    }
    __tablename__ = 'ramstk_hazards'
    __table_args__ = {'extend_existing': True}

    hazard_id = Column(
        'fld_hazard_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    hazard_category = Column('fld_hazard_category',
                             String(512),
                             default='Hazard Category')
    hazard_subcategory = Column('fld_hazard_subcategory',
                                String(512),
                                default='Hazard Subcategory')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKHazard data model attributes.

        :return: {hazard_id, category, subcategory} pairs
        :rtype: tuple
        """
        _attributes = {
            'hazard_id': self.hazard_id,
            'hazard_category': self.hazard_category,
            'hazard_subcategory': self.hazard_subcategory,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKHazards attributes.

        .. note:: you should pop the hazard ID entries from the attributes dict
            before passing it to this method.

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
