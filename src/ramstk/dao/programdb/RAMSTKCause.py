# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKCause.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCause Table Module."""

import gettext

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.

from ramstk.Utilities import none_to_default, OutOfRangeError
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE

_ = gettext.gettext


class RAMSTKCause(RAMSTK_BASE):
    """
    Class to represent the table ramstk_cause in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mechanism.
    This table shared a One-to-Many relationship with ramstk_control.
    This table shared a One-to-Many relationship with ramstk_action.
    """

    __tablename__ = 'ramstk_cause'
    __table_args__ = {'extend_existing': True}

    mode_id = Column(
        'fld_mode_id',
        Integer,
        ForeignKey('ramstk_mode.fld_mode_id'),
        nullable=False)
    mechanism_id = Column(
        'fld_mechanism_id',
        Integer,
        ForeignKey('ramstk_mechanism.fld_mechanism_id'),
        nullable=False)
    cause_id = Column(
        'fld_cause_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    rpn = Column('fld_rpn', Integer, default=0)
    rpn_detection = Column('fld_rpn_detection', Integer, default=0)
    rpn_detection_new = Column('fld_rpn_detection_new', Integer, default=0)
    rpn_new = Column('fld_rpn_new', Integer, default=0)
    rpn_occurrence = Column('fld_rpn_occurrence', Integer, default=0)
    rpn_occurrence_new = Column('fld_rpn_occurrence_new', Integer, default=0)

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
            'rpn_occurrence_new': self.rpn_occurrence_new
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKCause data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKCause {0:d} attributes.". \
               format(self.cause_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.rpn = int(none_to_default(attributes['rpn'], 0))
            self.rpn_detection = int(
                none_to_default(attributes['rpn_detection'], 0))
            self.rpn_detection_new = int(
                none_to_default(attributes['rpn_detection_new'], 0))
            self.rpn_new = int(none_to_default(attributes['rpn_new'], 0))
            self.rpn_occurrence = int(
                none_to_default(attributes['rpn_occurrence'], 0))
            self.rpn_occurrence_new = int(
                none_to_default(attributes['rpn_occurrence_new'], 0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKCause.set_attributes().".format(_err)

        return _error_code, _msg

    def calculate_rpn(self, severity, severity_new):
        """
        Calculate the Risk Priority Number (RPN) for the Cause.

            RPN = S * O * D

        :param int cause_id: the ID of the Cause to calculate the RPN.
        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Cause is associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = ("RAMSTK SUCCESS: Calculating failure cause {0:d} "
                "RPN.").format(self.cause_id)

        if not 0 < severity < 11:
            _error_code = 2020
            raise OutOfRangeError(
                _(u"RPN severity is outside the range "
                  u"[1, 10] for Cause ID: {0:d}.").format(self.cause_id))
        if not 0 < self.rpn_occurrence < 11:
            _error_code = 2020
            raise OutOfRangeError(
                _(u"RPN occurrence is outside the range "
                  u"[1, 10] for Cause ID: {0:d}.").format(self.cause_id))
        if not 0 < self.rpn_detection < 11:
            _error_code = 2020
            raise OutOfRangeError(
                _(u"RPN detection is outside the range "
                  u"[1, 10] for Cause ID: {0:d}.").format(self.cause_id))
        if not 0 < severity_new < 11:
            _error_code = 2020
            raise OutOfRangeError(
                _(u"RPN new severity is outside the range "
                  u"[1, 10] for Cause ID: {0:d}.").format(self.cause_id))
        if not 0 < self.rpn_occurrence_new < 11:
            _error_code = 2020
            raise OutOfRangeError(
                _(u"RPN new occurrence is outside the range "
                  u"[1, 10] for Cause ID: {0:d}.").format(self.cause_id))
        if not 0 < self.rpn_detection_new < 11:
            _error_code = 2020
            raise OutOfRangeError(
                _(u"RPN new detection is outside the range "
                  u"[1, 10] for Cause ID: {0:d}.").format(self.cause_id))

        self.rpn = int(severity) \
            * int(self.rpn_occurrence) \
            * int(self.rpn_detection)
        self.rpn_new = int(severity_new) \
            * int(self.rpn_occurrence_new) \
            * int(self.rpn_detection_new)

        if self.rpn < 1:
            _error_code = 2030
            _msg = ("Failure cause RPN has a value less than 1 for Cause "
                    "ID: {0:d}").format(self.cause_id)
            raise OutOfRangeError(
                _(u"Failure cause RPN has a value less than 1 for Cause ID: "
                  u"{0:d}.").format(self.cause_id))
        if self.rpn_new > 1000:
            _error_code = 2030
            _msg = ("Failure cause RPN has a value greater than 1000 for "
                    "Cause ID: {0:d}.").format(self.cause_id)
            raise OutOfRangeError(
                _(u"Failure cause RPN has a value greater than 1000 for Cause "
                  u"ID: {0:d}.").format(self.cause_id))

        return _error_code, _msg
