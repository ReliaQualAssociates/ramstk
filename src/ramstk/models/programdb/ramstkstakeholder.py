# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.RAMSTKStakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStakeholder Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKStakeholder(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_stakeholder table in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {
        'customer_rank': 1,
        'description': 'Stakeholder Input',
        'group': '',
        'improvement': 0.0,
        'overall_weight': 0.0,
        'planned_rank': 1,
        'priority': 1,
        'requirement_id': 0,
        'stakeholder': '',
        'user_float_1': 1.0,
        'user_float_2': 1.0,
        'user_float_3': 1.0,
        'user_float_4': 1.0,
        'user_float_5': 1.0
    }
    __tablename__ = 'ramstk_stakeholder'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    stakeholder_id = Column(
        'fld_stakeholder_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    customer_rank = Column('fld_customer_rank',
                           Integer,
                           default=__defaults__['customer_rank'])
    description = Column('fld_description',
                         String,
                         default=__defaults__['description'])
    group = Column('fld_group', String(128), default=__defaults__['group'])
    improvement = Column('fld_improvement',
                         Float,
                         default=__defaults__['improvement'])
    overall_weight = Column('fld_overall_weight',
                            Float,
                            default=__defaults__['overall_weight'])
    planned_rank = Column('fld_planned_rank',
                          Integer,
                          default=__defaults__['planned_rank'])
    priority = Column('fld_priority',
                      Integer,
                      default=__defaults__['priority'])
    requirement_id = Column('fld_requirement_id',
                            Integer,
                            default=__defaults__['requirement_id'])
    stakeholder = Column('fld_stakeholder',
                         String(128),
                         default=__defaults__['stakeholder'])
    user_float_1 = Column('fld_user_float_1',
                          Float,
                          default=__defaults__['user_float_1'])
    user_float_2 = Column('fld_user_float_2',
                          Float,
                          default=__defaults__['user_float_2'])
    user_float_3 = Column('fld_user_float_3',
                          Float,
                          default=__defaults__['user_float_3'])
    user_float_4 = Column('fld_user_float_4',
                          Float,
                          default=__defaults__['user_float_4'])
    user_float_5 = Column('fld_user_float_5',
                          Float,
                          default=__defaults__['user_float_5'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision: relationship = relationship(
        'RAMSTKRevision',
        back_populates='stakeholder',
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKStakeholder data model attributes.

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
            'user_float_5': self.user_float_5,
        }

        return _attributes
