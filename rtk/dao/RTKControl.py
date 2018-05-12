# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKControl.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKControl Table Module."""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKControl(RTK_BASE):
    """
    Class to represent the table rtk_control in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_control'
    __table_args__ = {'extend_existing': True}

    mode_id = Column(
        'fld_mode_id',
        Integer,
        ForeignKey('rtk_mode.fld_mode_id'),
        nullable=False)
    cause_id = Column(
        'fld_cause_id',
        Integer,
        ForeignKey('rtk_cause.fld_cause_id'),
        nullable=False)
    control_id = Column(
        'fld_control_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    type_id = Column('fld_type_id', String(512), default='')

    # Define the relationships to other tables in the RTK Program database.
    mode = relationship('RTKMode', back_populates='control')
    cause = relationship('RTKCause', back_populates='control')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = True
    is_action = False

    def get_attributes(self):
        """
        Retrieve the current values of the RTKControl data model attributes.

        :return: {mode_id, cause_id, control_id, description, type_id} pairs.
        :rtype: dict
        """
        _attributes = {
            'mode_id': self.mode_id,
            'cause_id': self.cause_id,
            'control_id': self.control_id,
            'description': self.description,
            'type_id': self.type_id
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKControl data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKControl {0:d} attributes.". \
               format(self.control_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.type_id = str(none_to_default(attributes['type_id'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKControl.set_attributes().".format(_err)

        return _error_code, _msg
