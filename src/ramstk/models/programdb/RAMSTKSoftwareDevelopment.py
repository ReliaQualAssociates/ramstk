# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKSoftwareDevelopment.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RAMSTKSoftwareDevelopment Table
===============================================================================
"""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import error_handler, none_to_default


class RAMSTKSoftwareDevelopment(RAMSTK_BASE):
    """
    Class to represent the table ramstk_software_development in the RAMSTK Program
    database.

    This table shares a Many-to-One relationship with ramstk_software.
    """

    __tablename__ = 'ramstk_software_development'
    __table_args__ = {'extend_existing': True}

    software_id = Column(
        'fld_software_id',
        Integer,
        ForeignKey('ramstk_software.fld_software_id'),
        nullable=False,
    )
    question_id = Column(
        'fld_question_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    answer = Column('fld_answer', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    software = relationship('RAMSTKSoftware', back_populates='development')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RAMSTKSoftwareDevelopment
        data model attributes.

        :return: (software_id, question_id, answer)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.question_id, self.answer)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RAMSTKSoftwareDevelopment data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKSoftwareDevelopment {0:d} " \
               "attributes.".format(self.software_id)

        try:
            self.answer = int(none_to_default(attributes[0], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKSoftwareDevelopment.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKSoftwareDevelopment attributes."

        return _error_code, _msg
