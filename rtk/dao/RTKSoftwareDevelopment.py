#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftwareDevelopment.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKSoftwareDevelopment Package.
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer
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


class RTKSoftwareDevelopment(Base):
    """
    Class to represent the table rtk_software_development in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_development'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='development')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSoftwareDevelopment
        data model attributes.

        :return: (software_id, question_id, answer)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.question_id, self.answer)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKSoftwareDevelopment data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSoftwareDevelopment {0:d} " \
               "attributes.".format(self.software_id)

        try:
            self.answer = int(attributes[0])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftwareDevelopment.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftwareDevelopment attributes."

        return _error_code, _msg
