# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKCategory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKCategory Table Module."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKCategory(RTK_BASE):
    """
    Class to represent the table rtk_category in the RTK Common database.

    Types of category are:
        # 1 = Hardware Component
        # 2 = Severity
    """

    __tablename__ = 'rtk_category'
    __table_args__ = {'extend_existing': True}

    category_id = Column(
        'fld_category_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(256), default='Category Name')
    description = Column(
        'fld_description', String(512), default='Category Description')
    cat_type = Column('fld_type', String(256), default='unknown')
    value = Column('fld_value', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    subcategory = relationship(
        'RTKSubCategory', back_populates='category', cascade='delete')
    mode = relationship(
        'RTKFailureMode', back_populates='category', cascade='delete')

    def get_attributes(self):
        """
        Retrieve current values of the RTKCategory data model attributes.

        :return: {category_id, name, description, cat_type, value} pairs
        :rtype: dict
        """
        _attributes = {
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'category_type': self.cat_type,
            'value': self.value
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKCategory data model attributes.

        :param dict attributes: dict containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCategory {0:d} attributes.". \
            format(self.category_id)

        try:
            self.name = str(
                none_to_default(attributes['name'], 'Category Name'))
            self.description = str(
                none_to_default(attributes['description'],
                                'Category Description'))
            self.cat_type = str(
                none_to_default(attributes['category_type'], 'unknown'))
            self.value = int(none_to_default(attributes['value'], 1))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKCategory.set_attributes().".format(_err)

        return _error_code, _msg
