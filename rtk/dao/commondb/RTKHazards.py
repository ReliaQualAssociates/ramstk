# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKHazards.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKHazard Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKHazards(RTK_BASE):
    """Class to represent the table rtk_hazard in the RTK Common database."""

    __tablename__ = 'rtk_hazards'
    __table_args__ = {'extend_existing': True}

    hazard_id = Column(
        'fld_hazard_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    category = Column('fld_category', String(512), default='Hazard Category')
    subcategory = Column(
        'fld_subcategory', String(512), default='Hazard Subcategory')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKHazard data model attributes.

        :return: {hazard_id, category, subcategory} pairs
        :rtype: tuple
        """
        _attributes = {
            'hazard_id': self.hazard_id,
            'category': self.category,
            'subcategory': self.subcategory
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKHazard data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKHazard {0:d} attributes.". \
            format(self.hazard_id)

        try:
            self.category = str(
                none_to_default(attributes['category'], 'Hazard Category'))
            self.subcategory = str(
                none_to_default(attributes['subcategory'],
                                'Hazard Subcategory'))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
