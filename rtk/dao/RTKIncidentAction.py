#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKIncidentAction.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKIncidentAction Table
==============================
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


class RTKIncidentAction(Base):
    """
    Class to represent the table rtk_incident_action in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_incident.
    """

    __tablename__ = 'rtk_incident_action'
    __table_args__ = {'extend_existing': True}

    incident_id = Column('fld_incident_id', Integer,
                         ForeignKey('rtk_incident.fld_incident_id'),
                         nullable=False)
    action_id = Column('fld_action_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    action_owner = Column('fld_action_owner', Integer, default=0)
    action_prescribed = Column('fld_action_prescribed', BLOB, default='')
    action_taken = Column('fld_action_taken', BLOB, default='')
    approved = Column('fld_approved', Integer, default=0)
    approved_by = Column('fld_approved_by', Integer, default=0)
    approved_date = Column('fld_approved_date', Date,
                           default=date.today() + timedelta(days=30))
    closed = Column('fld_closed', Integer, default=0)
    closed_by = Column('fld_closed_by', Integer, default=0)
    closed_date = Column('fld_closed_date', Date,
                         default=date.today() + timedelta(days=30))
    due_date = Column('fld_due_date', Date,
                      default=date.today() + timedelta(days=30))
    status_id = Column('fld_status_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    incident = relationship('RTKIncident', back_populates='incident_action')

    def get_attributes(self):
        """
        Retrieves the current values of the RTKIncidentAction data model
        attributes.

        :return: (incident_id, action_id, action_id, action_owner,
                  action_prescribed, action_taken, approved, approved_by,
                  approved_date, closed, closed_by, closed_date, due_date,
                  status_id)
        :rtype: tuple
        """

        _values = (self.incident_id, self.action_id, self.action_owner,
                   self.action_prescribed, self.action_taken, self.approved,
                   self.approved_by, self.approved_date, self.closed,
                   self.closed_by, self.closed_date, self.due_date,
                   self.status_id)

        return _values

    def set_attributes(self, values):
        """
        Method to set the RTKIncidentAction data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKIncidentAction {0:d} attributes.". \
               format(self.action_id)

        try:
            self.action_owner = int(values[0])
            self.action_prescribed = str(values[1])
            self.action_taken = str(values[2])
            self.approved = int(values[3])
            self.approved_by = int(values[4])
            self.approved_date = values[5]
            self.closed = int(values[6])
            self.closed_by = int(values[7])
            self.closed_date = values[8]
            self.due_date = values[9]
            self.status_id = int(values[10])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKIncidentAction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKIncidentAction attributes."

        return _error_code, _msg

