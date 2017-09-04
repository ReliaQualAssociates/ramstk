#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCause.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
===============================================================================
The RTKCause Table
===============================================================================
"""

import gettext

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default, OutOfRangeError
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKCause(RTK_BASE):
    """
    Class to represent the table rtk_cause in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mechanism.
    This table shared a One-to-Many relationship with rtk_control.
    This table shared a One-to-Many relationship with rtk_action.
    """

    __tablename__ = 'rtk_cause'
    __table_args__ = {'extend_existing': True}

    mechanism_id = Column('fld_mechanism_id', Integer,
                          ForeignKey('rtk_mechanism.fld_mechanism_id'),
                          nullable=False)
    cause_id = Column('fld_cause_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    rpn = Column('fld_rpn', Integer, default=0)
    rpn_detection = Column('fld_rpn_detection', Integer, default=0)
    rpn_detection_new = Column('fld_rpn_detection_new', Integer, default=0)
    rpn_new = Column('fld_rpn_new', Integer, default=0)
    rpn_occurrence = Column('fld_rpn_occurrence', Integer, default=0)
    rpn_occurrence_new = Column('fld_rpn_occurrence_new', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mechanism = relationship('RTKMechanism', back_populates='cause')
    control = relationship('RTKControl', back_populates='cause')
    action = relationship('RTKAction', back_populates='cause')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKCause data model
        attributes.

        :return: (mode_id, mechanism_id, cause_id, description, rpn_occurrence,
                  rpn_detection, rpn, rpn_occurrence_new, rpn_detection_new,
                  rpn_new)
        :rtype: tuple
        """

        _attributes = (self.mechanism_id, self.cause_id, self.description,
                       self.rpn, self.rpn_detection, self.rpn_detection_new,
                       self.rpn_new, self.rpn_occurrence,
                       self.rpn_occurrence_new)

        return _attributes

    def set_attributes(self, values):
        """
        Method to set the RTKCause data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCause {0:d} attributes.". \
               format(self.cause_id)

        try:
            self.description = str(none_to_default(values[0], ''))
            self.rpn = int(none_to_default(values[1], 0))
            self.rpn_detection = int(none_to_default(values[2], 0))
            self.rpn_detection_new = int(none_to_default(values[3], 0))
            self.rpn_new = int(none_to_default(values[4], 0))
            self.rpn_occurrence = int(none_to_default(values[5], 0))
            self.rpn_occurrence_new = int(none_to_default(values[6], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCause.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCause attributes."

        return _error_code, _msg

    def calculate_rpn(self, severity, severity_new):
        """
        Method to calculate the Risk Priority Number (RPN) for the Mechanism.

            RPN = S * O * D

        :param int cause_id: the ID of the Cause to calculate the RPN.
        :param int severity: the Severity (S) value of the FMEA end effect for
                             the failure mode this Cause is associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating failure cause {0:d} RPN.'.\
                format(self.cause_id)

        if not 0 < severity < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_occurrence < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_detection < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN detection is outside the range "
                                    u"[1, 10]."))
        if not 0 < severity_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new severity is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_occurrence_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new occurrence is outside the range "
                                    u"[1, 10]."))
        if not 0 < self.rpn_detection_new < 11:
            _error_code = 2020
            raise OutOfRangeError(_(u"RPN new detection is outside the range "
                                    u"[1, 10]."))

        self.rpn = int(severity) \
                * int(self.rpn_occurrence) \
                * int(self.rpn_detection)
        self.rpn_new = int(severity_new) \
                * int(self.rpn_occurrence_new) \
                * int(self.rpn_detection_new)

        if self.rpn < 1:
            _error_code = 2030
            _msg = 'Failure cause RPN has a value less than 1.'
            raise OutOfRangeError(_(u"Failure cause RPN has a value less "
                                    u"than 1."))
        if self.rpn_new > 1000:
            _error_code = 2030
            _msg = 'Failure cause RPN has a value greater than 1000.'
            raise OutOfRangeError(_(u"Failure cause RPN has a value "
                                    u"greater than 1000."))

        return _error_code, _msg

