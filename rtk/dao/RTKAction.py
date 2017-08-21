#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKAction.py is part of The RTK Project
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
The RTKAction Table
===============================================================================
"""

from datetime import date, timedelta

# Import the database models.
from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKAction(RTK_BASE):
    """
    Class to represent the table rtk_action in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_action'
    __table_args__ = {'extend_existing': True}

    mode_id = Column('fld_mode_id', Integer,
                     ForeignKey('rtk_mode.fld_mode_id'), nullable=False)
    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    action_id = Column('fld_action_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    action_recommended = Column('fld_action_recommended', BLOB, default='')
    action_category = Column('fld_action_category', Integer, default=0)
    action_owner = Column('fld_action_owner', Integer, default=0)
    action_due_date = Column('fld_action_due_date', Date,
                             default=date.today() + timedelta(days=30))
    action_status_id = Column('fld_action_status', Integer, default=0)
    action_taken = Column('fld_action_taken', BLOB, default='')
    action_approved = Column('fld_action_approved', Integer, default=0)
    action_approve_date = Column('fld_action_approve_date', Date,
                                 default=date.today() + timedelta(days=30))
    action_closed = Column('fld_action_closed', Integer, default=0)
    action_close_date = Column('fld_action_close_date', Date,
                               default=date.today() + timedelta(days=30))

    # Define the relationships to other tables in the RTK Program database.
    # The first relationship is for functional FMEAs and the second is for
    # hardware FMEAs.
    mode = relationship('RTKMode', back_populates='action')
    cause = relationship('RTKCause', back_populates='action')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKAction data model
        attributes.

        :return: (mode_id, cause_id, action_id, action_recommended,
                  action_category, action_owner, action_due_date,
                  action_status, action_taken, action_approved,
                  action_approved_date, action_closed, action_closed_date)
        :rtype: tuple
        """

        _values = (self.mode_id, self.cause_id, self.action_id,
                   self.action_recommended, self.action_category,
                   self.action_owner, self.action_due_date,
                   self.action_status_id, self.action_taken,
                   self.action_approved, self.action_approve_date,
                   self.action_closed, self.action_close_date)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the RTKAction data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKAction {0:d} attributes.".\
            format(self.action_id)
        _date = date.today() + timedelta(days=30)

        try:
            self.action_recommended = str(none_to_default(attributes[0], ''))
            self.action_category = int(none_to_default(attributes[1], 0))
            self.action_owner = int(none_to_default(attributes[2], 0))
            self.action_due_date = none_to_default(attributes[3], _date)
            self.action_status_id = int(none_to_default(attributes[4], 0))
            self.action_taken = str(none_to_default(attributes[5], ''))
            self.action_approved = int(none_to_default(attributes[6], 0))
            self.action_approve_date = none_to_default(attributes[7], _date)
            self.action_closed = int(none_to_default(attributes[8], 0))
            self.action_close_date = none_to_default(attributes[9], _date)
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKAction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKAction attributes."

        return _error_code, _msg
