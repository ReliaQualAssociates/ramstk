#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSubCategory.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKSubCategory Table
==============================
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKSubCategory(Base):
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
            self.category_id = int(attributes[0])
            self.description = str(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSubCategory.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSubCategory attributes."

        return _error_code, _msg
