# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKStatus.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKStatus Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKStatus(RTK_BASE):
    """Class to represent the table rtk_status in the RTK Common database."""

    __tablename__ = 'rtk_status'
    __table_args__ = {'extend_existing': True}

    status_id = Column(
        'fld_status_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(256), default='Status Name')
    description = Column(
        'fld_description', String(512), default='Status Decription')
    status_type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKStatus data model attributes.

        :return: {status_id, name, description, status_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'status_id': self.status_id,
            'name': self.name,
            'description': self.description,
            'status_type': self.status_type
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKStatus data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKStatus {0:d} attributes.". \
            format(self.status_id)

        try:
            self.name = str(none_to_default(attributes['name'], 'Status Name'))
            self.description = str(
                none_to_default(attributes['description'],
                                'Status Description'))
            self.status_type = str(
                none_to_default(attributes['status_type'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
