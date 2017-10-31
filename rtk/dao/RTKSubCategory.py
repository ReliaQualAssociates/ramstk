# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSubCategory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKSubCategory Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKSubCategory(RTK_BASE):
    """
    Class to represent the table rtk_subcategory in the RTK Common database.
    """

    __tablename__ = 'rtk_subcategory'
    __table_args__ = {'extend_existing': True}

    category_id = Column('fld_category_id', Integer,
                         ForeignKey('rtk_category.fld_category_id'),
                         nullable=False)
    subcategory_id = Column('fld_subcategory_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Type Description')

    # Define the relationships to other tables in the RTK Program database.
    category = relationship('RTKCategory', back_populates='subcategory')
    mode = relationship('RTKFailureMode', back_populates='subcategory',
                        cascade='delete')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSubCategory data model
        attributes.

        :return: (category_id, subcategory, description)
        :rtype: tuple
        """

        _values = (self.category_id, self.subcategory_id, self.description)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKSubCategory data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSubCategory {0:d} attributes.". \
            format(self.subcategory_id)

        try:
            self.category_id = int(none_to_default(attributes[0], -1))
            self.description = str(none_to_default(attributes[1], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSubCategory.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSubCategory attributes."

        return _error_code, _msg
