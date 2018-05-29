# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKSubCategory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKSubCategory Table Module."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKSubCategory(RTK_BASE):
    """Class to represent the table rtk_subcategory in the RTK Common database."""

    __tablename__ = 'rtk_subcategory'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        ForeignKey('rtk_category.fld_category_id'),
        nullable=False)
    subcategory_id = Column(
        'fld_subcategory_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Type Description')

    # Define the relationships to other tables in the RTK Program database.
    category = relationship('RTKCategory', back_populates='subcategory')
    mode = relationship(
        'RTKFailureMode', back_populates='subcategory', cascade='delete')

    def get_attributes(self):
        """
        Retrieve current values of the RTKSubCategory data model attributes.

        :return: {category_id, subcategory, description} pairs.
        :rtype: dict
        """
        _attributes = {
            'category_id': self.category_id,
            'subcategory_id': self.subcategory_id,
            'description': self.description
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKSubCategory data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSubCategory {0:d} attributes.". \
            format(self.subcategory_id)

        try:
            self.category_id = int(
                none_to_default(attributes['category_id'], -1))
            self.description = str(
                none_to_default(attributes['description'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
