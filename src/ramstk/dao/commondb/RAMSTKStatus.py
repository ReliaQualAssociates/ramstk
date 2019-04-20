# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKStatus.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStatus Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKStatus(RAMSTK_BASE):
    """Class to represent the table ramstk_status in the RAMSTK Common database."""

    __tablename__ = 'ramstk_status'
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
        Retrieve the current values of the RAMSTKStatus data model attributes.

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
        Set the current values of the RAMSTKStatus data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKStatus {0:d} attributes.". \
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
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(str(_err),
                                                      self.__class__.__name__)

        return _error_code, _msg
