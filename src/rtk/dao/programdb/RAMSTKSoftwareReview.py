# -*- coding: utf-8 -*-
#
#       rtk.dao.RAMSTKSoftwareReview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RAMSTKSoftwareReview Table
===============================================================================
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from rtk.Utilities import error_handler, none_to_default
from rtk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKSoftwareReview(RAMSTK_BASE):
    """
    Class to represent the table rtk_software_review in the RAMSTK Program
    database.

    :cvar str type: the type of review the question(s) are applicable to.
                    Types are SRR, PDR, CDR, and TRR.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_review'
    __table_args__ = {'extend_existing': True}

    software_id = Column(
        'fld_software_id',
        Integer,
        ForeignKey('rtk_software.fld_software_id'),
        nullable=False)
    question_id = Column(
        'fld_question_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    answer = Column('fld_answer', Integer, default=0)
    value = Column('fld_value', Integer, default=0)
    review_type = Column('fld_type', String(256), default='')

    # Define the relationships to other tables in the RAMSTK Program database.
    software = relationship('RAMSTKSoftware', back_populates='review')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RAMSTKSoftwareReview
        data model attributes.

        :return: (software_id, question_id, answer, value, review_type)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.question_id, self.answer,
                       self.value, self.review_type)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RAMSTKSoftwareReview data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKSoftwareReview {0:d} " \
               "attributes.".format(self.software_id)

        try:
            self.answer = int(none_to_default(attributes[0], 0))
            self.value = int(none_to_default(attributes[1], 0))
            self.review_type = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKSoftwareReview.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKSoftwareReview attributes."

        return _error_code, _msg
