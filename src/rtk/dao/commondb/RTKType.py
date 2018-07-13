# -*- coding: utf-8 -*-
#
#       rtk.dao.commondb.RTKType.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKType Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKType(RTK_BASE):
    """Class to represent the table rtk_type in the RTK Common database."""

    __tablename__ = 'rtk_type'
    __table_args__ = {'extend_existing': True}

    type_id = Column(
        'fld_type_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    code = Column('fld_code', String(256), default='Type Code')
    description = Column(
        'fld_description', String(512), default='Type Description')
    type_type = Column('fld_type', String(256), default='unknown')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKType data model attributes.

        :return: {type_id, description, type_type} pairs.
        :rtype: dict
        """
        _attributes = {'type_id':self.type_id, 'code':self.code, 'description':self.description, 'type_type':self.type_type}

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKType data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKType {0:d} attributes.". \
            format(self.type_id)

        try:
            self.code = str(none_to_default(attributes['code'], ''))
            self.description = str(none_to_default(attributes['description'], ''))
            self.type_type = str(none_to_default(attributes['type_type'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
