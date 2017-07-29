#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKStakeholder.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKStakeholder Table
==============================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
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
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKStakeholder(RTK_BASE):
    """
    Class to represent the rtk_stakeholder table in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_stakeholder'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    stakeholder_id = Column('fld_stakeholder_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)

    customer_rank = Column('fld_customer_rank', Integer, default=1)
    description = Column('fld_description', BLOB, default='')
    group = Column('fld_group', String(128), default='')
    improvement = Column('fld_improvement', Float, default=0.0)
    overall_weight = Column('fld_overall_weight', Float, default=0.0)
    planned_rank = Column('fld_planned_rank', Integer, default=1)
    priority = Column('fld_priority', Integer, default=1)
    requirement_id = Column('fld_requirement_id', Integer, default=0)
    stakeholder = Column('fld_stakeholder', String(128), default='')
    user_float_1 = Column('fld_user_float_1', Float, default=0.0)
    user_float_2 = Column('fld_user_float_2', Float, default=0.0)
    user_float_3 = Column('fld_user_float_3', Float, default=0.0)
    user_float_4 = Column('fld_user_float_4', Float, default=0.0)
    user_float_5 = Column('fld_user_float_5', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='stakeholder')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKStakeholder data model
        attributes.


        :return: (revision_id, stakeholder_id, customer_rank, description,
                  group, improvement, overall_weight, planned_rank, priority,
                  requirement_id, stakeholder, user_float_1, user_float_2,
                  user_float_3, user_float_4, user_float_5)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.stakeholder_id,
                       self.customer_rank, self.description, self.group,
                       self.improvement, self.overall_weight,
                       self.planned_rank, self.priority, self.requirement_id,
                       self.stakeholder, self.user_float_1, self.user_float_2, 
                       self.user_float_3, self.user_float_4, self.user_float_5)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKStakeholder data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKStakeholder {0:d} attributes.". \
               format(self.stakeholder_id)

        try:
            self.customer_rank = int(attributes[0])
            self.description = str(attributes[1])
            self.group = str(attributes[2])
            self.improvement = float(attributes[3])
            self.overall_weight = float(attributes[4])
            self.planned_rank = int(attributes[5])
            self.priority = int(attributes[6])
            self.requirement_id = int(attributes[7])
            self.stakeholder = str(attributes[8])
            self.user_float_1 = float(attributes[9])
            self.user_float_2 = float(attributes[10])
            self.user_float_3 = float(attributes[11])
            self.user_float_4 = float(attributes[12])
            self.user_float_5 = float(attributes[13])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKStakeholder.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKStakeholder attributes."

        return _error_code, _msg
