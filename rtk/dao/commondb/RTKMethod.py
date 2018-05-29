# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKMethod.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKMethod Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKMethod(RTK_BASE):
    """Class to represent the table rtk_method in the RTK Common database."""

    __tablename__ = 'rtk_method'
    __table_args__ = {'extend_existing': True}

    method_id = Column(
        'fld_method_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    name = Column('fld_name', String(256), default='Method Name')
    description = Column(
        'fld_description', String(512), default='Method Description')
    method_type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKMethod data model attributes.

        :return: {method_id, name, description, method_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'method_id': self.method_id,
            'name': self.name,
            'description': self.description,
            'method_type': self.method_type
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKMethod data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMethod {0:d} attributes.". \
            format(self.method_id)

        try:
            self.name = str(none_to_default(attributes['name'], 'Method Name'))
            self.description = str(
                none_to_default(attributes['description'],
                                'Method Description'))
            self.method_type = str(
                none_to_default(attributes['method_type'], 'unknown'))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
