# * coding: utf8 *
#
#       ramstk.dao.commondb.RAMSTKCondition.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007  2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCondition Table Module."""

from sqlalchemy import Column, Integer, String

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKCondition(RAMSTK_BASE):
    """Class to represent the table ramstk_condition in RAMSTK Common database."""

    __tablename__ = 'ramstk_condition'
    __table_args__ = {'extend_existing': True}

    condition_id = Column(
        'fld_condition_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Condition Decription')
    cond_type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKCondition data model attributes.

        :return: {condition_id, description, condition_type} pairs
        :rtype: dict
        """
        _attributes = {
            'condition_id': self.condition_id,
            'description': self.description,
            'condition_type': self.cond_type
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKCondition data model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKCondition {0:d} attributes.". \
            format(self.condition_id)

        try:
            self.description = str(
                none_to_default(attributes['description'],
                                'Condition Description'))
            self.cond_type = str(
                none_to_default(attributes['condition_type'], 'unknown'))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKCondition.set_attributes().".format(str(_err))

        return _error_code, _msg
