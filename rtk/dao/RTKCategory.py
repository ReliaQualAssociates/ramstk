# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCategory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKCategory Table."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default
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
        Method to retrieve the current values of the RTKCategory data model
        attributes.

        :return: (category_id, name, description, cat_type, value)
        :rtype: tuple
        """

        _values = (self.category_id, self.name, self.description,
                   self.cat_type, self.value)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKCategory data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCategory {0:d} attributes.". \
            format(self.category_id)

        try:
            self.name = str(none_to_default(attributes[0], 'Category Name'))
            self.description = str(
                none_to_default(attributes[1], 'Category Description'))
            self.cat_type = str(none_to_default(attributes[2], 'unknown'))
            self.value = int(none_to_default(attributes[3], 1))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCategory.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCategory attributes."

        return _error_code, _msg
