# -*- coding: utf-8 -*-
#
#       ramstk.dao.programdb.RAMSTKMechanism.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMechanism Table Module."""

import gettext

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default, OutOfRangeError
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Doyle "weibullguy" Rowland'

_ = gettext.gettext


class RAMSTKMechanism(RAMSTK_BASE):
    """
    Class to represent table ramstk_mechanism in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mode.
    This table shares a One-to-Many relationship with ramstk_cause.
    This table shares a One-to-Many relationship with ramstk_op_load.
    """

    __tablename__ = 'ramstk_mechanism'
    __table_args__ = {'extend_existing': True}

    mode_id = Column(
        'fld_mode_id',
        Integer,
        ForeignKey('ramstk_mode.fld_mode_id'),
        nullable=False)
    mechanism_id = Column(
        'fld_mechanism_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    pof_include = Column('fld_pof_include', Integer, default=1)
    rpn = Column('fld_rpn', Integer, default=0)
    rpn_detection = Column('fld_rpn_detection', Integer, default=0)
    rpn_detection_new = Column('fld_rpn_detection_new', Integer, default=0)
    rpn_new = Column('fld_rpn_new', Integer, default=0)
    rpn_occurrence = Column('fld_rpn_occurrence', Integer, default=0)
    rpn_occurrence_new = Column('fld_rpn_occurrence_new', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    mode = relationship('RAMSTKMode', back_populates='mechanism')
    cause = relationship(
        'RAMSTKCause', back_populates='mechanism', cascade='all,delete')
    op_load = relationship(
        'RAMSTKOpLoad', back_populates='mechanism', cascade='all,delete')

    is_mode = False
    is_mechanism = True
    is_cause = False
    is_control = False
    is_action = False
    is_opload = False
    is_opstress = False
    is_testmethod = False

    def get_attributes(self):
        """
        Retrieve the current values of the Mechanism data model attributes.

        :return: {mode_id, mechanism_id, description, pof_include, rpn,
                  rpn_detection, rpn_detection_new, rpn_new, rpn_occurrence,
                  rpn_occurrence_new} pairs
        :rtype: dict
        """
        _attributes = {
            'mode_id': self.mode_id,
            'mechanism_id': self.mechanism_id,
            'description': self.description,
            'pof_include': self.pof_include,
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
        Set the current values of the Mechanism data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKMechanism {0:d} attributes.". \
               format(self.mechanism_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.pof_include = int(
                none_to_default(attributes['pof_include'], 1))
            self.rpn = int(none_to_default(attributes['rpn'], 0))
            self.rpn_detection = int(
                none_to_default(attributes['rpn_detection'], 1))
            self.rpn_detection_new = int(
                none_to_default(attributes['rpn_detection_new'], 1))
            self.rpn_new = int(none_to_default(attributes['rpn_new'], 0))
            self.rpn_occurrence = int(
                none_to_default(attributes['rpn_occurrence'], 1))
            self.rpn_occurrence_new = int(
                none_to_default(attributes['rpn_occurrence_new'], 1))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKMechanism.set_attributes().".format(str(_err))

        return _error_code, _msg

    def calculate_rpn(self, severity, severity_new):
        """
        Calculate the Risk Priority Number (RPN) for the Mechanism.

            RPN = S * O * D

        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Mechanism is associated
                             with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Calculating failure mechanism {0:d} RPN.'.\
            format(self.mechanism_id)

        if not 0 < severity < 11:
            _error_code = 2020
            _msg = _("RPN severity is outside the range [1, 10].")
            raise OutOfRangeError(_msg)
        if not 0 < self.rpn_occurrence < 11:
            _error_code = 2020
            _msg = _("RPN occurrence is outside the range [1, 10].")
            raise OutOfRangeError(_msg)
        if not 0 < self.rpn_detection < 11:
            _error_code = 2020
            _msg = _("RPN detection is outside the range [1, 10].")
            raise OutOfRangeError(_msg)
        if not 0 < severity_new < 11:
            _error_code = 2020
            _msg = _("RPN new severity is outside the range [1, 10].")
            raise OutOfRangeError(_msg)
        if not 0 < self.rpn_occurrence_new < 11:
            _error_code = 2020
            _msg = _("RPN new occurrence is outside the range [1, 10].")
            raise OutOfRangeError(_msg)
        if not 0 < self.rpn_detection_new < 11:
            _error_code = 2020
            _msg = _("RPN new detection is outside the range [1, 10].")
            raise OutOfRangeError(_msg)

        self.rpn = int(severity) \
            * int(self.rpn_occurrence) \
            * int(self.rpn_detection)
        self.rpn_new = int(severity_new) \
            * int(self.rpn_occurrence_new) \
            * int(self.rpn_detection_new)

        if self.rpn < 1:
            _error_code = 2020
            _msg = 'Failure mechanism RPN has a value less than 1.'
            raise OutOfRangeError(
                _("Failure mechanism RPN has a value less "
                  "than 1."))
        if self.rpn_new > 1000:
            _error_code = 2020
            _msg = 'Failure mechanism RPN has a value greater than 1000.'
            raise OutOfRangeError(
                _("Failure mechanism RPN has a value "
                  "greater than 1000."))

        return _error_code, _msg
