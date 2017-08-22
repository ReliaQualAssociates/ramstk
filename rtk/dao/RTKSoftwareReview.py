#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftwareReview.py is part of The RTK Project
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
The RTKSoftwareReview Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKSoftwareReview(RTK_BASE):
    """
    Class to represent the table rtk_software_review in the RTK Program
    database.

    :cvar str type: the type of review the question(s) are applicable to.
                    Types are SRR, PDR, CDR, and TRR.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_review'
    __table_args__ = {'extend_existing': True}

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)
    value = Column('fld_value', Integer, default=0)
    type = Column('fld_type', String(256), default='')

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='review')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSoftwareReview
        data model attributes.

        :return: (software_id, question_id, answer, value, type)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.question_id, self.answer,
                       self.value, self.type)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKSoftwareReview data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSoftwareReview {0:d} " \
               "attributes.".format(self.software_id)

        try:
            self.answer = int(attributes[0])
            self.value = int(attributes[1])
            self.type = str(attributes[2])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftwareReview.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftwareReview attributes."

        return _error_code, _msg
