#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMethod.py is part of The RTK Project
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
The RTKMethod Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKMethod(RTK_BASE):
    """
    Class to represent the table rtk_method in the RTK Common database.
    """

    __tablename__ = 'rtk_method'
    __table_args__ = {'extend_existing': True}

    method_id = Column('fld_method_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    name = Column('fld_name', String(256), default='Method Name')
    description = Column('fld_description', String(512),
                         default='Method Description')
    type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKMethod data model
        attributes.

        :return: (method_id, name, description, type)
        :rtype: tuple
        """

        _values = (self.method_id, self.name, self.description, self.type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKMethod data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMethod {0:d} attributes.". \
            format(self.method_id)

        try:
            self.name = str(attributes[0])
            self.description = str(attributes[1])
            self.type = str(attributes[2])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMethod.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMethod attributes."

        return _error_code, _msg
