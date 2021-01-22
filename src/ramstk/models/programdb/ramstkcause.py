# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKCause.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCause Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKCause(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_cause in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mechanism.
    This table shared a One-to-Many relationship with ramstk_control.
    This table shared a One-to-Many relationship with ramstk_action.
    """

    __defaults__ = {
        'description': '',
        'rpn': 0,
        'rpn_detection': 10,
        'rpn_detection_new': 10,
        'rpn_new': 0,
        'rpn_occurrence': 10,
        'rpn_occurrence_new': 10
    }
    __tablename__ = 'ramstk_cause'
    __table_args__ = (ForeignKeyConstraint(
        [
            'fld_revision_id', 'fld_hardware_id', 'fld_mode_id',
            'fld_mechanism_id'
        ],
        [
            'ramstk_mechanism.fld_revision_id',
            'ramstk_mechanism.fld_hardware_id', 'ramstk_mechanism.fld_mode_id',
            'ramstk_mechanism.fld_mechanism_id'
        ],
    ), {
        'extend_existing': True
    })

    revision_id = Column('fld_revision_id',
                         Integer,
                         primary_key=True,
                         nullable=False)
    hardware_id = Column('fld_hardware_id',
                         Integer,
                         primary_key=True,
                         default=-1,
                         nullable=False)
    mode_id = Column('fld_mode_id', Integer, primary_key=True, nullable=False)
    mechanism_id = Column('fld_mechanism_id',
                          Integer,
                          primary_key=True,
                          nullable=False)
    cause_id = Column('fld_cause_id',
                      Integer,
                      primary_key=True,
                      autoincrement=True,
                      nullable=False,
                      unique=True)

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
    # mode = relationship('RAMSTKMode', back_populates='cause')
    mechanism = relationship(  # type: ignore
        'RAMSTKMechanism', back_populates='cause')
    control = relationship(  # type: ignore
        'RAMSTKControl',
        back_populates='cause',
        cascade='delete, delete-orphan')
    action = relationship(  # type: ignore
        'RAMSTKAction',
        back_populates='cause',
        cascade='delete, delete-orphan')

    is_mode = False
    is_mechanism = False
    is_cause = True
    is_control = False
    is_action = False

    def get_attributes(self):
        """Retrieve current values of the RAMSTKCause data model attributes.

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
            'rpn_occurrence_new': self.rpn_occurrence_new
        }

        return _attributes
