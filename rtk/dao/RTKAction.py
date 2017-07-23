#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKAction.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKAction Package.
"""

from datetime import date, timedelta

# Import the database models.
from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKAction(Base):
    """
    Class to represent the table rtk_action in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_action'
    __table_args__ = {'extend_existing': True}

    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    action_id = Column('fld_action_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    action_recommended = Column('fld_action_recommended', BLOB, default='')
    action_category = Column('fld_action_category', Integer, default=0)
    action_owner = Column('fld_action_owner', Integer, default=0)
    action_due_date = Column('fld_action_due_date', Date,
                             default=date.today() + timedelta(days=30))
    action_status_id = Column('fld_action_status', Integer, default=0)
    action_taken = Column('fld_action_taken', BLOB, default='')
    action_approved = Column('fld_action_approved', Integer, default=0)
    action_approve_date = Column('fld_action_approve_date', Date,
                                 default=date.today() + timedelta(days=30))
    action_closed = Column('fld_action_closed', Integer, default=0)
    action_close_date = Column('fld_action_close_date', Date,
                               default=date.today() + timedelta(days=30))

    # Define the relationships to other tables in the RTK Program database.
    cause = relationship('RTKCause', back_populates='action')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKAction data model
        attributes.

        :return: (cause_id, action_id, action_recommended, action_category,
                  action_owner, action_due_date, action_status, action_taken,
                  action_approved, action_approved_date, action_closed,
                  action_closed_date)
        :rtype: tuple
        """

        _values = (self.cause_id, self.action_id, self.action_recommended,
                   self.action_category, self.action_owner,
                   self.action_due_date, self.action_status_id,
                   self.action_taken, self.action_approved,
                   self.action_approve_date, self.action_closed,
                   self.action_close_date)

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

        try:
            self.action_recommended = str(attributes[0])
            self.action_category = int(attributes[1])
            self.action_owner = int(attributes[2])
            self.action_due_date = attributes[3]
            self.action_status_id = int(attributes[4])
            self.action_taken = str(attributes[5])
            self.action_approved = int(attributes[6])
            self.action_approve_date = attributes[7]
            self.action_closed = int(attributes[8])
            self.action_close_date = attributes[9]
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKAction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKAction attributes."

        return _error_code, _msg
