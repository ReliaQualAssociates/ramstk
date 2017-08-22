#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKUser.py is part of The RTK Project
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
The RTKUser Table
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


class RTKUser(RTK_BASE):
    """
    Class to represent the table rtk_user in the RTK Common database.

    This table shares a One-to-Many relationship with rtk_workgroup.
    """

    __tablename__ = 'rtk_user'
    __table_args__ = {'extend_existing': True}

    user_id = Column('fld_user_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)
    user_lname = Column('fld_user_lname', String(256), default='Last Name')
    user_fname = Column('fld_user_fname', String(256), default='First Name')
    user_email = Column('fld_user_email', String(256), default='EMail')
    user_phone = Column('fld_user_phone', String(256), default='867.5309')
    user_group_id = Column('fld_user_group', String(256), default='0')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKUser data model
        attributes.

        :return: (user_id, user_lname, user_fname, user_email, user_phone,
                  user_group_id)
        :rtype: tuple
        """

        _values = (self.user_id, self.user_lname, self.user_fname,
                   self.user_email, self.user_phone, self.user_group_id)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKUser data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKUser {0:d} attributes.".\
            format(self.user_id)

        try:
            self.user_lname = str(attributes[0])
            self.user_fname = str(attributes[1])
            self.user_email = str(attributes[2])
            self.user_phone = str(attributes[3])
            self.user_group_id = str(attributes[4])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKUser.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKUser attributes."

        return _error_code, _msg
