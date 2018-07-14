# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKGroup.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKGroup Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


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
        Retrieve the current values of the RTKGroup data model attributes.

        :return: {workgroup_id, description, group_type} pairs
        :rtype: dict
        """
        _attributes = {
            'group_id': self.group_id,
            'description': self.description,
            'group_type': self.group_type
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKGroup data model attributes.

        :param dict attributes: dict containing the pair:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKGroup {0:d} attributes.".\
            format(self.group_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Group Description'))
            self.group_type = str(
                none_to_default(attributes['group_type'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
