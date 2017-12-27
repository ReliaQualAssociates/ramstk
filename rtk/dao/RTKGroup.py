# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKGroup.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKGroup Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKGroup(RTK_BASE):
    """
    Class to represent the table rtk_group in the RTK Common database.

    This table shares a Many-to-One relationship with rtk_user.
    """

    __tablename__ = 'rtk_group'
    __table_args__ = {'extend_existing': True}

    group_id = Column(
        'fld_group_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Group Description')
    group_type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKGroup data model
        attributes.

        :return: (workgroup_id, description, group_type)
        :rtype: tuple
        """

        _values = (self.group_id, self.description, self.group_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKGroup data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKGroup {0:d} attributes.".\
            format(self.group_id)

        try:
            self.description = str(
                none_to_default(attributes[0], 'Group Description'))
            self.group_type = str(none_to_default(attributes[1], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKGroup.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKGroup attributes."

        return _error_code, _msg
