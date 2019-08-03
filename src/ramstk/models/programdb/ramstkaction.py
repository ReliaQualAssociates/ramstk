# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKAction.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKAction Table Module."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKAction(RAMSTK_BASE, RAMSTKBaseTable):
    """
    Class to represent table ramstk_action in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_cause.
    """

    __defaults__ = {
        'action_recommended': b'',
        'action_category': '',
        'action_owner': '',
        'action_due_date': date.today() + timedelta(days=30),
        'action_status': '',
        'action_taken': b'',
        'action_approved': 0,
        'action_approve_date': date.today() + timedelta(days=30),
        'action_closed': 0,
        'action_close_date': date.today() + timedelta(days=30)
    }
    __tablename__ = 'ramstk_action'
    __table_args__ = {'extend_existing': True}

    cause_id = Column(
        'fld_cause_id',
        Integer,
        ForeignKey('ramstk_cause.fld_cause_id'),
        nullable=False,
    )
    action_id = Column(
        'fld_action_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    action_recommended = Column('fld_action_recommended',
                                BLOB,
                                default=__defaults__['action_recommended'])
    action_category = Column('fld_action_category',
                             String(512),
                             default=__defaults__['action_category'])
    action_owner = Column('fld_action_owner',
                          String(512),
                          default=__defaults__['action_owner'])
    action_due_date = Column('fld_action_due_date',
                             Date,
                             default=__defaults__['action_due_date'])
    action_status = Column('fld_action_status',
                           String(512),
                           default=__defaults__['action_status'])
    action_taken = Column('fld_action_taken',
                          BLOB,
                          default=__defaults__['action_taken'])
    action_approved = Column('fld_action_approved',
                             Integer,
                             default=__defaults__['action_approved'])
    action_approve_date = Column('fld_action_approve_date',
                                 Date,
                                 default=__defaults__['action_approve_date'])
    action_closed = Column('fld_action_closed',
                           Integer,
                           default=__defaults__['action_closed'])
    action_close_date = Column('fld_action_close_date',
                               Date,
                               default=__defaults__['action_close_date'])

    # Define the relationships to other tables in the RAMSTK Program database.
    cause = relationship('RAMSTKCause', back_populates='action')

    is_mode = False
    is_mechanism = False
    is_cause = False
    is_control = False
    is_action = True

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKAction data model attributes.

        :return: {cause_id, action_id, action_recommended,
                  action_category, action_owner, action_due_date,
                  action_status, action_taken, action_approved,
                  action_approved_date, action_closed,
                  action_closed_date} pairs.
        :rtype: dict
        """
        _attributes = {
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
            'action_close_date': self.action_close_date,
        }

        return _attributes
