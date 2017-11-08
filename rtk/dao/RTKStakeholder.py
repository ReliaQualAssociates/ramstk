# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKStakeholder.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKStakeholder Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKStakeholder(RTK_BASE):
    """
    Class to represent the rtk_stakeholder table in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_stakeholder'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('rtk_revision.fld_revision_id'),
        nullable=False)
    stakeholder_id = Column(
        'fld_stakeholder_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    customer_rank = Column('fld_customer_rank', Integer, default=1)
    description = Column('fld_description', BLOB, default='Stakeholder Input')
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
            self.customer_rank = int(none_to_default(attributes[0], 1))
            self.description = str(none_to_default(attributes[1], ''))
            self.group = str(none_to_default(attributes[2], ''))
            self.improvement = float(none_to_default(attributes[3], 0.0))
            self.overall_weight = float(none_to_default(attributes[4], 0.0))
            self.planned_rank = int(none_to_default(attributes[5], 1))
            self.priority = int(none_to_default(attributes[6], 1))
            self.requirement_id = int(none_to_default(attributes[7], 0))
            self.stakeholder = str(none_to_default(attributes[8], ''))
            self.user_float_1 = float(none_to_default(attributes[9], 0.0))
            self.user_float_2 = float(none_to_default(attributes[10], 0.0))
            self.user_float_3 = float(none_to_default(attributes[11], 0.0))
            self.user_float_4 = float(none_to_default(attributes[12], 0.0))
            self.user_float_5 = float(none_to_default(attributes[13], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKStakeholder.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKStakeholder attributes."

        return _error_code, _msg
