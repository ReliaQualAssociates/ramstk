#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCategory.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
===============================================================================
The RTKCategory Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKCategory(RTK_BASE):
    """
    Class to represent the table rtk_category in the RTK Common database.

    Types of category are:
        # 1 = Hardware Component
        # 2 = Severity
    """

    __tablename__ = 'rtk_category'
    __table_args__ = {'extend_existing': True}

    category_id = Column('fld_category_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    name = Column('fld_name', String(256), default='Category Code')
    description = Column('fld_description', String(512),
                         default='Category Description')
    type = Column('fld_type', String(256), default='unknown')
    value = Column('fld_value', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    subcategory = relationship('RTKSubCategory', back_populates='category',
                               cascade='delete')
    mode = relationship('RTKFailureMode', back_populates='category',
                        cascade='delete')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKCategory data model
        attributes.

        :return: (category_id, name, description, type, value)
        :rtype: tuple
        """

        _values = (self.category_id, self.name, self.description, self.type,
                   self.value)

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
            self.name = str(attributes[0])
            self.description = str(attributes[1])
            self.type = str(attributes[2])
            self.value = int(attributes[3])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCategory.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCategory attributes."

        return _error_code, _msg
