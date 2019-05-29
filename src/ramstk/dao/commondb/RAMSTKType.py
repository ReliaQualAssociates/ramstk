# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKType.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKType Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKType(RAMSTK_BASE):
    """Class to represent the table ramstk_type in the RAMSTK Common database."""

    __tablename__ = 'ramstk_type'
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
        Retrieve the current values of the RAMSTKType data model attributes.

        :return: {type_id, description, type_type} pairs.
        :rtype: dict
        """
        _attributes = {
            'type_id': self.type_id,
            'code': self.code,
            'description': self.description,
            'type_type': self.type_type
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKType data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKType {0:d} attributes.". \
            format(self.type_id)

        try:
            self.code = str(none_to_default(attributes['code'], ''))
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.type_type = str(none_to_default(attributes['type_type'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(_err,
                                                      self.__class__.__name__)

        return _error_code, _msg
