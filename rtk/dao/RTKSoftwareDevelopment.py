# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftwareDevelopment.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKSoftwareDevelopment Table
===============================================================================
"""

from sqlalchemy import Column, ForeignKey, Integer  
from sqlalchemy.orm import relationship  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKSoftwareDevelopment(RTK_BASE):
    """
    Class to represent the table rtk_software_development in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_development'
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
            self.answer = int(none_to_default(attributes[0], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftwareDevelopment.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftwareDevelopment attributes."

        return _error_code, _msg
