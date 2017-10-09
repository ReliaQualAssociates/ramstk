# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKUser.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKUser Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String        # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


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
            self.user_lname = str(none_to_default(attributes[0], 'Last Name'))
            self.user_fname = str(none_to_default(attributes[1], 'First Name'))
            self.user_email = str(none_to_default(attributes[2], 'EMail'))
            self.user_phone = str(none_to_default(attributes[3], '867.5309'))
            self.user_group_id = str(none_to_default(attributes[4], '0'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKUser.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKUser attributes."

        return _error_code, _msg
