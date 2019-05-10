# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKStakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStakeholder Table Module."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKStakeholder(RAMSTK_BASE):
    """
    Class to represent ramstk_stakeholder table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __tablename__ = 'ramstk_stakeholder'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    stakeholder_id = Column(
        'fld_stakeholder_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    customer_rank = Column('fld_customer_rank', Integer, default=1)
    description = Column('fld_description', BLOB, default=b'Stakeholder Input')
    group = Column('fld_group', String(128), default='')
    improvement = Column('fld_improvement', Float, default=0.0)
    overall_weight = Column('fld_overall_weight', Float, default=0.0)
    planned_rank = Column('fld_planned_rank', Integer, default=1)
    priority = Column('fld_priority', Integer, default=1)
    requirement_id = Column('fld_requirement_id', Integer, default=0)
    stakeholder = Column('fld_stakeholder', String(128), default='')
    user_float_1 = Column('fld_user_float_1', Float, default=1.0)
    user_float_2 = Column('fld_user_float_2', Float, default=1.0)
    user_float_3 = Column('fld_user_float_3', Float, default=1.0)
    user_float_4 = Column('fld_user_float_4', Float, default=1.0)
    user_float_5 = Column('fld_user_float_5', Float, default=1.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='stakeholder')

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKStakeholder data model attributes.

        :return: {revision_id, stakeholder_id, customer_rank, description,
                  group, improvement, overall_weight, planned_rank, priority,
                  requirement_id, stakeholder, user_float_1, user_float_2,
                  user_float_3, user_float_4, user_float_5} pairs.
        :rtype: tuple
        """
        _attributes = {
            'revision_id': self.revision_id,
            'stakeholder_id': self.stakeholder_id,
            'customer_rank': self.customer_rank,
            'description': self.description,
            'group': self.group,
            'improvement': self.improvement,
            'overall_weight': self.overall_weight,
            'planned_rank': self.planned_rank,
            'priority': self.priority,
            'requirement_id': self.requirement_id,
            'stakeholder': self.stakeholder,
            'user_float_1': self.user_float_1,
            'user_float_2': self.user_float_2,
            'user_float_3': self.user_float_3,
            'user_float_4': self.user_float_4,
            'user_float_5': self.user_float_5
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKStakeholder data model attributes.

        :param dict attributes: dict of values to assign to the instance
                                attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKStakeholder {0:d} attributes.". \
               format(self.stakeholder_id)

        try:
            self.customer_rank = int(
                none_to_default(float(attributes['customer_rank']), 1))
            try:
                self.description = none_to_default(
                    attributes['description'].encode('utf-8'), b'')
            except AttributeError:
                self.description = none_to_default(attributes['description'],
                                                   b'')
            self.group = str(none_to_default(attributes['group'], ''))
            self.improvement = float(
                none_to_default(attributes['improvement'], 0.0))
            self.overall_weight = float(
                none_to_default(attributes['overall_weight'], 0.0))
            self.planned_rank = int(
                none_to_default(float(attributes['planned_rank']), 1))
            self.priority = int(
                none_to_default(float(attributes['priority']), 1))
            self.requirement_id = int(
                none_to_default(attributes['requirement_id'], 0))
            self.stakeholder = str(
                none_to_default(attributes['stakeholder'], ''))
            self.user_float_1 = float(
                none_to_default(attributes['user_float_1'], 0.0))
            self.user_float_2 = float(
                none_to_default(attributes['user_float_2'], 0.0))
            self.user_float_3 = float(
                none_to_default(attributes['user_float_3'], 0.0))
            self.user_float_4 = float(
                none_to_default(attributes['user_float_4'], 0.0))
            self.user_float_5 = float(
                none_to_default(attributes['user_float_5'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKStakeholder.set_attributes().".format(str(_err))

        return _error_code, _msg
