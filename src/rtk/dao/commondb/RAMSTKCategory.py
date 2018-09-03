# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RAMSTKCategory.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTKCategory Table Module."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKCategory(RAMSTK_BASE):
    """
    Class to represent the table rtk_category in the RAMSTK Common database.

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

    # Define the relationships to other tables in the RAMSTK Program database.
    subcategory = relationship(
        'RAMSTKSubCategory', back_populates='category', cascade='delete')
    mode = relationship(
        'RAMSTKFailureMode', back_populates='category', cascade='delete')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKCategory data model attributes.

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
        Set the current values of the RAMSTKCategory data model attributes.

        :param dict attributes: dict containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKCategory {0:d} attributes.". \
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
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKCategory.set_attributes().".format(_err)

        return _error_code, _msg
