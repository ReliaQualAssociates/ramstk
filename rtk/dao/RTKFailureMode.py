#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKFailureMode.py is part of The RTK Project
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
The RTKFailureMode Table
===============================================================================
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKFailureMode(RTK_BASE):
    """
    Class to represent the table rtk_failuremode in the RTK Common database.
    """

    __tablename__ = 'rtk_failure_mode'
    __table_args__ = {'extend_existing': True}

    category_id = Column('fld_category_id', Integer,
                         ForeignKey('rtk_category.fld_category_id'),
                         nullable=False)
    subcategory_id = Column('fld_subcategory_id', Integer,
                            ForeignKey('rtk_subcategory.fld_subcategory_id'),
                            nullable=False)
    mode_id = Column('fld_failuremode_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Failure Mode Decription')
    mode_ratio = Column('fld_mode_ratio', Float, default=1.0)
    source = Column('fld_source', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    category = relationship('RTKCategory', back_populates='mode')
    subcategory = relationship('RTKSubCategory', back_populates='mode')

    def get_attributes(self):
        """
        FailureMode to retrieve the current values of the RTKFailureMode data
        model attributes.

        :return: (failuremode_id, description, type)
        :rtype: tuple
        """

        _values = (self.category_id, self.subcategory_id, self.mode_id,
                   self.description, self.mode_ratio, self.source)

        return _values

    def set_attributes(self, attributes):
        """
        FailureMode to set the current values of the RTKFailureMode data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKFailureMode {0:d} attributes.". \
            format(self.mode_id)

        try:
            self.description = str(attributes[0])
            self.mode_ratio = float(attributes[1])
            self.source = int(attributes[2])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKFailureMode.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKFailureMode attributes."

        return _error_code, _msg
