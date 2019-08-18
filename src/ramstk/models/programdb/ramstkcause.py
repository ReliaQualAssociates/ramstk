# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKCause.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCause Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKCause(RAMSTK_BASE, RAMSTKBaseTable):
    """
    Class to represent the table ramstk_cause in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mechanism.
    This table shared a One-to-Many relationship with ramstk_control.
    This table shared a One-to-Many relationship with ramstk_action.
    """

    __defaults__ = {
        'description': '',
        'rpn': 0,
        'rpn_detection': 0,
        'rpn_detection_new': 0,
        'rpn_new': 0,
        'rpn_occurrence': 0,
        'rpn_occurrence_new': 0
    }
    __tablename__ = 'ramstk_cause'
    __table_args__ = {'extend_existing': True}

    mode_id = Column(
        'fld_mode_id',
        Integer,
        ForeignKey('ramstk_mode.fld_mode_id'),
        nullable=False,
    )
    mechanism_id = Column(
        'fld_mechanism_id',
        Integer,
        ForeignKey('ramstk_mechanism.fld_mechanism_id'),
        nullable=False,
    )
    cause_id = Column(
        'fld_cause_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column('fld_description',
                         String(512),
                         default=__defaults__['description'])
    rpn = Column('fld_rpn', Integer, default=__defaults__['rpn'])
    rpn_detection = Column('fld_rpn_detection',
                           Integer,
                           default=__defaults__['rpn_detection'])
    rpn_detection_new = Column('fld_rpn_detection_new',
                               Integer,
                               default=__defaults__['rpn_detection_new'])
    rpn_new = Column('fld_rpn_new', Integer, default=__defaults__['rpn_new'])
    rpn_occurrence = Column('fld_rpn_occurrence',
                            Integer,
                            default=__defaults__['rpn_occurrence'])
    rpn_occurrence_new = Column('fld_rpn_occurrence_new',
                                Integer,
                                default=__defaults__['rpn_occurrence_new'])

    # Define the relationships to other tables in the RAMSTK Program database.
    mode = relationship('RAMSTKMode', back_populates='cause')
    mechanism = relationship('RAMSTKMechanism', back_populates='cause')
    control = relationship('RAMSTKControl', back_populates='cause')
    action = relationship('RAMSTKAction', back_populates='cause')

    is_mode = False
    is_mechanism = False
    is_cause = True
    is_control = False
    is_action = False

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKCause data model attributes.

        :return: {mode_id, mechanism_id, cause_id, description, rpn_occurrence,
                  rpn_detection, rpn, rpn_occurrence_new, rpn_detection_new,
                  rpn_new}
        :rtype: tuple
        """
        _attributes = {
            'mode_id': self.mode_id,
            'mechanism_id': self.mechanism_id,
            'cause_id': self.cause_id,
            'description': self.description,
            'rpn': self.rpn,
            'rpn_detection': self.rpn_detection,
            'rpn_detection_new': self.rpn_detection_new,
            'rpn_new': self.rpn_new,
            'rpn_occurrence': self.rpn_occurrence,
            'rpn_occurrence_new': self.rpn_occurrence_new,
        }

        return _attributes
