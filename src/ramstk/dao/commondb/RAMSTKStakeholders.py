# -*- coding: utf-8 -*-
#
#       ramstk.dao.commondb.RAMSTKStakeholders.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStakeholders Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKStakeholders(RAMSTK_BASE):
    """Class to represent the table ramstk_stakeholders in the RAMSTK Common database."""

    __tablename__ = 'ramstk_stakeholders'
    __table_args__ = {'extend_existing': True}

    stakeholders_id = Column(
        'fld_stakeholders_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    stakeholder = Column('fld_stakeholder', String(512), default='Stakeholder')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKStakeholders data model attributes.

        :return: {stakeholders_id, stakeholder} pairs.
        :rtype: dict
        """
        _attributes = {
            'stakeholders_id': self.stakeholders_id,
            'stakeholder': self.stakeholder
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKStakeholders data model attributes.

        :param dict attributes: dict containing the key:values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKStakeholders {0:d} attributes.". \
            format(self.stakeholders_id)

        try:
            self.stakeholder = str(
                none_to_default(attributes['stakeholder'], 'Stakeholder'))
        except KeyError as _err:
            _error_code = 40
            _msg = ("RAMSTK ERROR: Missing attribute {0:s} in attribute "
                    "dictionary passed to "
                    "{1:s}.set_attributes().").format(str(_err),
                                                      self.__class__.__name__)

        return _error_code, _msg
