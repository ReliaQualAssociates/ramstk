# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftwareReview.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKSoftwareReview Table
===============================================================================
"""

from sqlalchemy import Column, ForeignKey, \
                       Integer, String              # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


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
    review_type = Column('fld_type', String(256), default='')

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='review')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSoftwareReview
        data model attributes.

        :return: (software_id, question_id, answer, value, review_type)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.question_id, self.answer,
                       self.value, self.review_type)

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
            self.answer = int(none_to_default(attributes[0], 0))
            self.value = int(none_to_default(attributes[1], 0))
            self.review_type = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftwareReview.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftwareReview attributes."

        return _error_code, _msg
