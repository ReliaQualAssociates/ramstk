#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKControl.py is part of The RTK Project
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
The RTKControl Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKControl(RTK_BASE):
    """
    Class to represent the table rtk_control in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_control'
    __table_args__ = {'extend_existing': True}

    mode_id = Column('fld_mode_id', Integer,
                     ForeignKey('rtk_mode.fld_mode_id'), nullable=False)
    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    control_id = Column('fld_control_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    cause = relationship('RTKCause', back_populates='control')
    mode = relationship('RTKMode', back_populates='control')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKControl data model
        attributes.

        :return: (mode_id, cause_id, control_id, description, type_id)
        :rtype: tuple
        """

        _attributes = (self.mode_id, self.cause_id, self.control_id,
                       self.description, self.type_id)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKControl data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKControl {0:d} attributes.". \
               format(self.control_id)

        try:
            self.description = str(none_to_default(attributes[0], ''))
            self.type_id = int(none_to_default(attributes[1], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKControl.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKControl attributes."

        return _error_code, _msg
