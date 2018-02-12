# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRequirement.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKRequirement Table Module."""

from datetime import date

from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  

# Import other RTK modules.
from rtk.Utilities import none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKRequirement(RTK_BASE):
    """
    Class to represent the rtk_requirement table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_requirement'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('rtk_revision.fld_revision_id'),
        nullable=False)
    requirement_id = Column(
        'fld_requirement_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    derived = Column('fld_derived', Integer, default=0)
    description = Column('fld_description', BLOB, default='')
    figure_number = Column('fld_figure_number', String(256), default='')
    owner = Column('fld_owner', String(256), default='')
    page_number = Column('fld_page_number', String(256), default='')
    parent_id = Column('fld_parent_id', Integer, default=0)
    priority = Column('fld_priority', Integer, default=0)
    requirement_code = Column('fld_requirement_code', String(256), default='')
    specification = Column('fld_specification', String(256), default='')
    requirement_type = Column('fld_requirement_type', String(256), default='')
    validated = Column('fld_validated', Integer, default=0)
    validated_date = Column('fld_validated_date', Date, default=date.today())

    # Clarity of requirement questions.
    q_clarity_0 = Column('fld_clarity_0', Integer, default=0)
    q_clarity_1 = Column('fld_clarity_1', Integer, default=0)
    q_clarity_2 = Column('fld_clarity_2', Integer, default=0)
    q_clarity_3 = Column('fld_clarity_3', Integer, default=0)
    q_clarity_4 = Column('fld_clarity_4', Integer, default=0)
    q_clarity_5 = Column('fld_clarity_5', Integer, default=0)
    q_clarity_6 = Column('fld_clarity_6', Integer, default=0)
    q_clarity_7 = Column('fld_clarity_7', Integer, default=0)
    q_clarity_8 = Column('fld_clarity_8', Integer, default=0)

    # Completeness of requirement questions.
    q_complete_0 = Column('fld_complete_0', Integer, default=0)
    q_complete_1 = Column('fld_complete_1', Integer, default=0)
    q_complete_2 = Column('fld_complete_2', Integer, default=0)
    q_complete_3 = Column('fld_complete_3', Integer, default=0)
    q_complete_4 = Column('fld_complete_4', Integer, default=0)
    q_complete_5 = Column('fld_complete_5', Integer, default=0)
    q_complete_6 = Column('fld_complete_6', Integer, default=0)
    q_complete_7 = Column('fld_complete_7', Integer, default=0)
    q_complete_8 = Column('fld_complete_8', Integer, default=0)
    q_complete_9 = Column('fld_complete_9', Integer, default=0)

    # Consitency of requirement questions.
    q_consistent_0 = Column('fld_consistent_0', Integer, default=0)
    q_consistent_1 = Column('fld_consistent_1', Integer, default=0)
    q_consistent_2 = Column('fld_consistent_2', Integer, default=0)
    q_consistent_3 = Column('fld_consistent_3', Integer, default=0)
    q_consistent_4 = Column('fld_consistent_4', Integer, default=0)
    q_consistent_5 = Column('fld_consistent_5', Integer, default=0)
    q_consistent_6 = Column('fld_consistent_6', Integer, default=0)
    q_consistent_7 = Column('fld_consistent_7', Integer, default=0)
    q_consistent_8 = Column('fld_consistent_8', Integer, default=0)

    # Verifiablity of requirement questions.
    q_verifiable_0 = Column('fld_verifiable_0', Integer, default=0)
    q_verifiable_1 = Column('fld_verifiable_1', Integer, default=0)
    q_verifiable_2 = Column('fld_verifiable_2', Integer, default=0)
    q_verifiable_3 = Column('fld_verifiable_3', Integer, default=0)
    q_verifiable_4 = Column('fld_verifiable_4', Integer, default=0)
    q_verifiable_5 = Column('fld_verifiable_5', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='requirement')

    def get_attributes(self):
        """
        Retrieve the current values of the Requirement data model attributes.

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

    def set_attributes(self, attributes):
        """
        Set the current values of teh Requirement data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKRequirement {0:d} attributes.". \
               format(self.requirement_id)

        try:
            self.derived = int(none_to_default(attributes['derived'], 0))
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.figure_number = str(
                none_to_default(attributes['figure_number'], ''))
            self.owner = str(none_to_default(attributes['owner'], ''))
            self.page_number = str(
                none_to_default(attributes['page_number'], ''))
            self.parent_id = int(none_to_default(attributes['parent_id'], 0))
            self.priority = int(none_to_default(attributes['priority'], 0))
            self.requirement_code = str(
                none_to_default(attributes['requirement_code'], ''))
            self.specification = str(
                none_to_default(attributes['specification'], ''))
            self.requirement_type = str(
                none_to_default(attributes['requirement_type'], ''))
            self.validated = int(none_to_default(attributes['validated'], 0))
            self.validated_date = none_to_default(attributes['validated_date'],
                                                  date.today())
            self.q_clarity_0 = int(
                none_to_default(attributes['q_clarity_0'], 0))
            self.q_clarity_1 = int(
                none_to_default(attributes['q_clarity_1'], 0))
            self.q_clarity_2 = int(
                none_to_default(attributes['q_clarity_2'], 0))
            self.q_clarity_3 = int(
                none_to_default(attributes['q_clarity_3'], 0))
            self.q_clarity_4 = int(
                none_to_default(attributes['q_clarity_4'], 0))
            self.q_clarity_5 = int(
                none_to_default(attributes['q_clarity_5'], 0))
            self.q_clarity_6 = int(
                none_to_default(attributes['q_clarity_6'], 0))
            self.q_clarity_7 = int(
                none_to_default(attributes['q_clarity_7'], 0))
            self.q_clarity_8 = int(
                none_to_default(attributes['q_clarity_8'], 0))
            self.q_complete_0 = int(
                none_to_default(attributes['q_complete_0'], 0))
            self.q_complete_1 = int(
                none_to_default(attributes['q_complete_1'], 0))
            self.q_complete_2 = int(
                none_to_default(attributes['q_complete_2'], 0))
            self.q_complete_3 = int(
                none_to_default(attributes['q_complete_3'], 0))
            self.q_complete_4 = int(
                none_to_default(attributes['q_complete_4'], 0))
            self.q_complete_5 = int(
                none_to_default(attributes['q_complete_5'], 0))
            self.q_complete_6 = int(
                none_to_default(attributes['q_complete_6'], 0))
            self.q_complete_7 = int(
                none_to_default(attributes['q_complete_7'], 0))
            self.q_complete_8 = int(
                none_to_default(attributes['q_complete_8'], 0))
            self.q_complete_9 = int(
                none_to_default(attributes['q_complete_9'], 0))
            self.q_consistent_0 = int(
                none_to_default(attributes['q_consistent_0'], 0))
            self.q_consistent_1 = int(
                none_to_default(attributes['q_consistent_1'], 0))
            self.q_consistent_2 = int(
                none_to_default(attributes['q_consistent_2'], 0))
            self.q_consistent_3 = int(
                none_to_default(attributes['q_consistent_3'], 0))
            self.q_consistent_4 = int(
                none_to_default(attributes['q_consistent_4'], 0))
            self.q_consistent_5 = int(
                none_to_default(attributes['q_consistent_5'], 0))
            self.q_consistent_6 = int(
                none_to_default(attributes['q_consistent_6'], 0))
            self.q_consistent_7 = int(
                none_to_default(attributes['q_consistent_7'], 0))
            self.q_consistent_8 = int(
                none_to_default(attributes['q_consistent_8'], 0))
            self.q_verifiable_0 = int(
                none_to_default(attributes['q_verifiable_0'], 0))
            self.q_verifiable_1 = int(
                none_to_default(attributes['q_verifiable_1'], 0))
            self.q_verifiable_2 = int(
                none_to_default(attributes['q_verifiable_2'], 0))
            self.q_verifiable_3 = int(
                none_to_default(attributes['q_verifiable_3'], 0))
            self.q_verifiable_4 = int(
                none_to_default(attributes['q_verifiable_4'], 0))
            self.q_verifiable_5 = int(
                none_to_default(attributes['q_verifiable_5'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKMechanism.set_attributes().".format(_err)

        return _error_code, _msg

    def create_code(self, prefix):
        """
        Create the Requirement code based on the requirement type and it's ID.

        :param str prefix: the prefix to use for the Requirement code.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Pad the suffix (Requirement ID) with zeros so the suffix is four
        # characters wide and then create the code.
        _zeds = 4 - len(str(self.requirement_id))
        _pad = '0' * _zeds
        _code = '{0:s}-{1:s}{2:d}'.format(prefix, _pad, self.requirement_id)

        self.requirement_code = str(none_to_default(_code, ''))

        return _return
