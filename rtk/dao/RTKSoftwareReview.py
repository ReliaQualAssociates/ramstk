#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftwareReview.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKSoftwareReview Package.
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKSoftwareReview(Base):
    """
    Class to represent the table rtk_software_review in the RTK Program
    database.

    :cvar str type: the type of review the question(s) are applicable to.
                    Types are SRR, PDR, CDR, and TRR.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_review'

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
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftwareReview.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftwareReview attributes."

        return _error_code, _msg
