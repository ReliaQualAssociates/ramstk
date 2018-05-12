# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKAction.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKAction Table Module."""

from datetime import date, timedelta


from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKAction(RTK_BASE):
    """
    Class to represent the table rtk_action in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_action'
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
    action_id = Column(
        'fld_action_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    action_recommended = Column('fld_action_recommended', BLOB, default='')
    action_category = Column('fld_action_category', String(512), default='')
    action_owner = Column('fld_action_owner', String(512), default='')
    action_due_date = Column(
        'fld_action_due_date', Date, default=date.today() + timedelta(days=30))
    action_status = Column('fld_action_status', String(512), default='')
    action_taken = Column('fld_action_taken', BLOB, default='')
    action_approved = Column('fld_action_approved', Integer, default=0)
    action_approve_date = Column(
        'fld_action_approve_date',
        Date,
        default=date.today() + timedelta(days=30))
    action_closed = Column('fld_action_closed', Integer, default=0)
    action_close_date = Column(
        'fld_action_close_date',
        Date,
        default=date.today() + timedelta(days=30))

    # Define the relationships to other tables in the RTK Program database.
    # The first relationship is for functional FMEAs and the second is for
    # hardware FMEAs.
    mode = relationship('RTKMode', back_populates='action')
    cause = relationship('RTKCause', back_populates='action')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = False
    is_action = True

    def get_attributes(self):
        """
        Retrieve the current values of the RTKAction data model attributes.

        :return: {mode_id, cause_id, action_id, action_recommended,
                  action_category, action_owner, action_due_date,
                  action_status, action_taken, action_approved,
                  action_approved_date, action_closed,
                  action_closed_date} pairs.
        :rtype: dict
        """
        _attributes = {
            'mode_id': self.mode_id,
            'cause_id': self.cause_id,
            'action_id': self.action_id,
            'action_recommended': self.action_recommended,
            'action_category': self.action_category,
            'action_owner': self.action_owner,
            'action_due_date': self.action_due_date,
            'action_status': self.action_status,
            'action_taken': self.action_taken,
            'action_approved': self.action_approved,
            'action_approve_date': self.action_approve_date,
            'action_closed': self.action_closed,
            'action_close_date': self.action_close_date
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKAction data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKAction {0:d} attributes.".\
            format(self.action_id)
        _date = date.today() + timedelta(days=30)

        try:
            self.action_recommended = str(
                none_to_default(attributes['action_recommended'], ''))
            self.action_category = str(
                none_to_default(attributes['action_category'], ''))
            self.action_owner = str(
                none_to_default(attributes['action_owner'], 0))
            self.action_due_date = none_to_default(
                attributes['action_due_date'], _date)
            self.action_status = str(
                none_to_default(attributes['action_status'], 0))
            self.action_taken = str(
                none_to_default(attributes['action_taken'], ''))
            self.action_approved = int(
                none_to_default(attributes['action_approved'], 0))
            self.action_approve_date = none_to_default(
                attributes['action_approve_date'], _date)
            self.action_closed = int(
                none_to_default(attributes['action_closed'], 0))
            self.action_close_date = none_to_default(
                attributes['action_close_date'], _date)
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKAction.set_attributes().".format(_err)

        return _error_code, _msg
