#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKTestMethod.py is part of The RTK Project
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
The RTKTestMethod Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKTestMethod(RTK_BASE):
    """
    Class to represent the table rtk_test_method in the RTK Program database.

    This table shared a Many-to-One relationship with rtk_op_stress.
    """

    __tablename__ = 'rtk_test_method'
    __table_args__ = {'extend_existing': True}

    stress_id = Column('fld_stress_id', Integer,
                       ForeignKey('rtk_op_stress.fld_stress_id'),
                       nullable=False)
    test_id = Column('fld_test_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    boundary_conditions = Column('fld_boundary_conditions', String(512),
                                 default='')
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_stress = relationship('RTKOpStress', back_populates='test_method')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKTestMethod data model
        attributes.

        :return: (stress_id, test_id, description, boundary_conditions,
                  remarks)
        :rtype: tuple
        """

        _attributes = (self.stress_id, self.test_id, self.description,
                       self.boundary_conditions, self.remarks)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKTestMethod data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKTestMethod {0:d} attributes.". \
               format(self.test_id)

        try:
            self.description = str(attributes[0])
            self.boundary_conditions = str(attributes[1])
            self.remarks = str(attributes[2])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKTestMethod.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKTestMethod attributes."

        return _error_code, _msg
