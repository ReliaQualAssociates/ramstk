# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKControl.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKControl Table Module."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKControl(RAMSTK_BASE):
    """
    Class to represent the table ramstk_control in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_cause.
    """

    __tablename__ = 'ramstk_control'
    __table_args__ = {'extend_existing': True}

    cause_id = Column(
        'fld_cause_id',
        Integer,
        ForeignKey('ramstk_cause.fld_cause_id'),
        nullable=False)
    control_id = Column(
        'fld_control_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    type_id = Column('fld_type_id', String(512), default='')

    # Define the relationships to other tables in the RAMSTK Program database.
    cause = relationship('RAMSTKCause', back_populates='control')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = True
    is_action = False

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKControl data model attributes.

        :return: {cause_id, control_id, description, type_id} pairs.
        :rtype: dict
        """
        _attributes = {
            'cause_id': self.cause_id,
            'control_id': self.control_id,
            'description': self.description,
            'type_id': self.type_id
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKControl data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKControl {0:d} attributes.". \
               format(self.control_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.type_id = str(none_to_default(attributes['type_id'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKControl.set_attributes().".format(_err)

        return _error_code, _msg
