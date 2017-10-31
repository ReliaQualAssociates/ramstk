# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKAction.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKAction Table
===============================================================================
"""

from datetime import date, timedelta

# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKAction(RTK_BASE):
    """
    Class to represent the table rtk_action in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_action'
    __table_args__ = {'extend_existing': True}

    mode_id = Column('fld_mode_id', Integer,
                     ForeignKey('rtk_mode.fld_mode_id'), nullable=False)
    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    action_id = Column('fld_action_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    action_recommended = Column('fld_action_recommended', BLOB, default='')
    action_category = Column('fld_action_category', Integer, default=0)
    action_owner = Column('fld_action_owner', String(512), default=0)
    action_due_date = Column('fld_action_due_date', Date,
                             default=date.today() + timedelta(days=30))
    action_status = Column('fld_action_status', String(512), default=0)
    action_taken = Column('fld_action_taken', BLOB, default='')
    action_approved = Column('fld_action_approved', Integer, default=0)
    action_approve_date = Column('fld_action_approve_date', Date,
                                 default=date.today() + timedelta(days=30))
    action_closed = Column('fld_action_closed', Integer, default=0)
    action_close_date = Column('fld_action_close_date', Date,
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
        Method to retrieve the current values of the RTKAction data model
        attributes.

        :return: (mode_id, cause_id, action_id, action_recommended,
                  action_category, action_owner, action_due_date,
                  action_status, action_taken, action_approved,
                  action_approved_date, action_closed, action_closed_date)
        :rtype: tuple
        """

        _values = (self.mode_id, self.cause_id, self.action_id,
                   self.action_recommended, self.action_category,
                   self.action_owner, self.action_due_date,
                   self.action_status, self.action_taken,
                   self.action_approved, self.action_approve_date,
                   self.action_closed, self.action_close_date)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the RTKAction data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKAction {0:d} attributes.".\
            format(self.action_id)
        _date = date.today() + timedelta(days=30)

        try:
            self.action_recommended = str(none_to_default(attributes[0], ''))
            self.action_category = int(none_to_default(attributes[1], 0))
            self.action_owner = str(none_to_default(attributes[2], 0))
            self.action_due_date = none_to_default(attributes[3], _date)
            self.action_status = str(none_to_default(attributes[4], 0))
            self.action_taken = str(none_to_default(attributes[5], ''))
            self.action_approved = int(none_to_default(attributes[6], 0))
            self.action_approve_date = none_to_default(attributes[7], _date)
            self.action_closed = int(none_to_default(attributes[8], 0))
            self.action_close_date = none_to_default(attributes[9], _date)
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKAction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKAction attributes."

        return _error_code, _msg
