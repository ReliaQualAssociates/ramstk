#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKOpStress.py is part of The RTK Project
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
The RTKOpStress Table
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


class RTKOpStress(RTK_BASE):
    """
    Class to represent the table rtk_op_stress in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_op_load.
    """

    __tablename__ = 'rtk_op_stress'
    __table_args__ = {'extend_existing': True}

    load_id = Column('fld_load_id', Integer,
                     ForeignKey('rtk_op_load.fld_load_id'), nullable=False)
    stress_id = Column('fld_stress_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    load_history = Column('fld_load_history', Integer, default=0)
    measurable_parameter = Column('fld_measurable_parameter', Integer,
                                  default=0)
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_load = relationship('RTKOpLoad', back_populates='op_stress')
    test_method = relationship('RTKTestMethod', back_populates='op_stress')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mode data model
        attributes.

        :return: (load_id, stress_id, description, load_history,
                  measurable_parameter, remarks)
        :rtype: tuple
        """

        _attributes = (self.load_id, self.stress_id, self.description,
                       self.load_history, self.measurable_parameter,
                       self.remarks)

        return _attributes

    def set_attributes(self, values):
        """
        Method to set the Stress data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKOpStress {0:d} attributes.". \
               format(self.stress_id)

        try:
            self.description = str(values[0])
            self.load_history = int(values[1])
            self.measurable_parameter = int(values[2])
            self.remarks = str(values[3])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKOpStress.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKOpStress attributes."

        return _error_code, _msg
