# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKRequirement.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKRequirement Table Module."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable
from ramstk.utilities import none_to_default


class RAMSTKRequirement(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_requirement table in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {
        'derived': 0,
        'description': '',
        'figure_number': '',
        'owner': 0,
        'page_number': '',
        'parent_id': 0,
        'priority': 0,
        'requirement_code': '',
        'specification': '',
        'requirement_type': 0,
        'validated': 0,
        'validated_date': date.today(),
        'q_clarity_0': 0,
        'q_clarity_1': 0,
        'q_clarity_2': 0,
        'q_clarity_3': 0,
        'q_clarity_4': 0,
        'q_clarity_5': 0,
        'q_clarity_6': 0,
        'q_clarity_7': 0,
        'q_clarity_8': 0,
        'q_complete_0': 0,
        'q_complete_1': 0,
        'q_complete_2': 0,
        'q_complete_3': 0,
        'q_complete_4': 0,
        'q_complete_5': 0,
        'q_complete_6': 0,
        'q_complete_7': 0,
        'q_complete_8': 0,
        'q_complete_9': 0,
        'q_consistent_0': 0,
        'q_consistent_1': 0,
        'q_consistent_2': 0,
        'q_consistent_3': 0,
        'q_consistent_4': 0,
        'q_consistent_5': 0,
        'q_consistent_6': 0,
        'q_consistent_7': 0,
        'q_consistent_8': 0,
        'q_verifiable_0': 0,
        'q_verifiable_1': 0,
        'q_verifiable_2': 0,
        'q_verifiable_3': 0,
        'q_verifiable_4': 0,
        'q_verifiable_5': 0
    }
    __tablename__ = 'ramstk_requirement'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id',
                         Integer,
                         ForeignKey('ramstk_revision.fld_revision_id'),
                         nullable=False)
    requirement_id = Column('fld_requirement_id',
                            Integer,
                            primary_key=True,
                            autoincrement=True,
                            nullable=False)

    derived = Column('fld_derived', Integer, default=__defaults__['derived'])
    description = Column('fld_description',
                         String,
                         default=__defaults__['description'])
    figure_number = Column('fld_figure_number',
                           String(256),
                           default=__defaults__['figure_number'])
    owner = Column('fld_owner', Integer, default=__defaults__['owner'])
    page_number = Column('fld_page_number',
                         String(256),
                         default=__defaults__['page_number'])
    parent_id = Column('fld_parent_id',
                       Integer,
                       default=__defaults__['parent_id'])
    priority = Column('fld_priority',
                      Integer,
                      default=__defaults__['priority'])
    requirement_code = Column('fld_requirement_code',
                              String(256),
                              default=__defaults__['requirement_code'])
    specification = Column('fld_specification',
                           String(256),
                           default=__defaults__['specification'])
    requirement_type = Column('fld_requirement_type',
                              Integer,
                              default=__defaults__['requirement_type'])
    validated = Column('fld_validated',
                       Integer,
                       default=__defaults__['validated'])
    validated_date = Column('fld_validated_date',
                            Date,
                            default=__defaults__['validated_date'])

    # Clarity of requirement questions.
    q_clarity_0 = Column('fld_clarity_0',
                         Integer,
                         default=__defaults__['q_clarity_0'])
    q_clarity_1 = Column('fld_clarity_1',
                         Integer,
                         default=__defaults__['q_clarity_1'])
    q_clarity_2 = Column('fld_clarity_2',
                         Integer,
                         default=__defaults__['q_clarity_2'])
    q_clarity_3 = Column('fld_clarity_3',
                         Integer,
                         default=__defaults__['q_clarity_3'])
    q_clarity_4 = Column('fld_clarity_4',
                         Integer,
                         default=__defaults__['q_clarity_4'])
    q_clarity_5 = Column('fld_clarity_5',
                         Integer,
                         default=__defaults__['q_clarity_5'])
    q_clarity_6 = Column('fld_clarity_6',
                         Integer,
                         default=__defaults__['q_clarity_6'])
    q_clarity_7 = Column('fld_clarity_7',
                         Integer,
                         default=__defaults__['q_clarity_7'])
    q_clarity_8 = Column('fld_clarity_8',
                         Integer,
                         default=__defaults__['q_clarity_8'])

    # Completeness of requirement questions.
    q_complete_0 = Column('fld_complete_0',
                          Integer,
                          default=__defaults__['q_complete_0'])
    q_complete_1 = Column('fld_complete_1',
                          Integer,
                          default=__defaults__['q_complete_1'])
    q_complete_2 = Column('fld_complete_2',
                          Integer,
                          default=__defaults__['q_complete_2'])
    q_complete_3 = Column('fld_complete_3',
                          Integer,
                          default=__defaults__['q_complete_3'])
    q_complete_4 = Column('fld_complete_4',
                          Integer,
                          default=__defaults__['q_complete_4'])
    q_complete_5 = Column('fld_complete_5',
                          Integer,
                          default=__defaults__['q_complete_5'])
    q_complete_6 = Column('fld_complete_6',
                          Integer,
                          default=__defaults__['q_complete_6'])
    q_complete_7 = Column('fld_complete_7',
                          Integer,
                          default=__defaults__['q_complete_7'])
    q_complete_8 = Column('fld_complete_8',
                          Integer,
                          default=__defaults__['q_complete_8'])
    q_complete_9 = Column('fld_complete_9',
                          Integer,
                          default=__defaults__['q_complete_9'])

    # Consitency of requirement questions.
    q_consistent_0 = Column('fld_consistent_0',
                            Integer,
                            default=__defaults__['q_consistent_0'])
    q_consistent_1 = Column('fld_consistent_1',
                            Integer,
                            default=__defaults__['q_consistent_1'])
    q_consistent_2 = Column('fld_consistent_2',
                            Integer,
                            default=__defaults__['q_consistent_2'])
    q_consistent_3 = Column('fld_consistent_3',
                            Integer,
                            default=__defaults__['q_consistent_3'])
    q_consistent_4 = Column('fld_consistent_4',
                            Integer,
                            default=__defaults__['q_consistent_4'])
    q_consistent_5 = Column('fld_consistent_5',
                            Integer,
                            default=__defaults__['q_consistent_5'])
    q_consistent_6 = Column('fld_consistent_6',
                            Integer,
                            default=__defaults__['q_consistent_6'])
    q_consistent_7 = Column('fld_consistent_7',
                            Integer,
                            default=__defaults__['q_consistent_7'])
    q_consistent_8 = Column('fld_consistent_8',
                            Integer,
                            default=__defaults__['q_consistent_8'])

    # Verifiablity of requirement questions.
    q_verifiable_0 = Column('fld_verifiable_0',
                            Integer,
                            default=__defaults__['q_verifiable_0'])
    q_verifiable_1 = Column('fld_verifiable_1',
                            Integer,
                            default=__defaults__['q_verifiable_1'])
    q_verifiable_2 = Column('fld_verifiable_2',
                            Integer,
                            default=__defaults__['q_verifiable_2'])
    q_verifiable_3 = Column('fld_verifiable_3',
                            Integer,
                            default=__defaults__['q_verifiable_3'])
    q_verifiable_4 = Column('fld_verifiable_4',
                            Integer,
                            default=__defaults__['q_verifiable_4'])
    q_verifiable_5 = Column('fld_verifiable_5',
                            Integer,
                            default=__defaults__['q_verifiable_5'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision: relationship = relationship(
        'RAMSTKRevision',
        back_populates='requirement',
    )

    def get_attributes(self):
        """Retrieve current values of the Requirement data model attributes.

        :return: {revision_id, requirement_id, derived, description,
                  figure_number, owner, page_number, parent_id, priority,
                  requirement_code, specification, requirement_type, validated,
                  validated_date, q_clarity_0, q_clarity_1, q_clarity_2,
                  q_clarity_3, q_clarity_4, q_clarity_5, q_clarity_6,
                  q_clarity_7, q_clarity_8, q_complete_0, q_complete_1,
                  q_complete_2, q_complete_3, q_complete_4, q_complete_5,
                  q_complete_6, q_complete_7, q_complete_8, q_complete_9,
                  q_consistent_0, q_consistent_1, q_consistent_2,
                  q_consistent_3, q_consistent_4, q_consistent_5,
                  q_consistent_6, q_consistent_7, q_consistent_8,
                  q_verifiable_0, q_verifiable_1, q_verifiable_2,
                  q_verifiable_3, q_verifiable_4, q_verifiable_5} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'requirement_id': self.requirement_id,
            'derived': self.derived,
            'description': self.description,
            'figure_number': self.figure_number,
            'owner': self.owner,
            'page_number': self.page_number,
            'parent_id': self.parent_id,
            'priority': self.priority,
            'requirement_code': self.requirement_code,
            'specification': self.specification,
            'requirement_type': self.requirement_type,
            'validated': self.validated,
            'validated_date': self.validated_date,
            'q_clarity_0': self.q_clarity_0,
            'q_clarity_1': self.q_clarity_1,
            'q_clarity_2': self.q_clarity_2,
            'q_clarity_3': self.q_clarity_3,
            'q_clarity_4': self.q_clarity_4,
            'q_clarity_5': self.q_clarity_5,
            'q_clarity_6': self.q_clarity_6,
            'q_clarity_7': self.q_clarity_7,
            'q_clarity_8': self.q_clarity_8,
            'q_complete_0': self.q_complete_0,
            'q_complete_1': self.q_complete_1,
            'q_complete_2': self.q_complete_2,
            'q_complete_3': self.q_complete_3,
            'q_complete_4': self.q_complete_4,
            'q_complete_5': self.q_complete_5,
            'q_complete_6': self.q_complete_6,
            'q_complete_7': self.q_complete_7,
            'q_complete_8': self.q_complete_8,
            'q_complete_9': self.q_complete_9,
            'q_consistent_0': self.q_consistent_0,
            'q_consistent_1': self.q_consistent_1,
            'q_consistent_2': self.q_consistent_2,
            'q_consistent_3': self.q_consistent_3,
            'q_consistent_4': self.q_consistent_4,
            'q_consistent_5': self.q_consistent_5,
            'q_consistent_6': self.q_consistent_6,
            'q_consistent_7': self.q_consistent_7,
            'q_consistent_8': self.q_consistent_8,
            'q_verifiable_0': self.q_verifiable_0,
            'q_verifiable_1': self.q_verifiable_1,
            'q_verifiable_2': self.q_verifiable_2,
            'q_verifiable_3': self.q_verifiable_3,
            'q_verifiable_4': self.q_verifiable_4,
            'q_verifiable_5': self.q_verifiable_5
        }

        return _attributes

    def create_code(self, prefix: str) -> None:
        """Create Requirement code based on the requirement type and it's ID.

        :param prefix: the prefix to use for the Requirement code.
        :return: None
        :rtype: None
        """
        # Pad the suffix (Requirement ID) with zeros so the suffix is four
        # characters wide and then create the code.
        _zeds = 4 - len(str(self.requirement_id))
        _pad = '0' * _zeds
        _code = '{0:s}-{1:s}{2:d}'.format(prefix, _pad, self.requirement_id)

        self.requirement_code = str(none_to_default(_code, ''))
