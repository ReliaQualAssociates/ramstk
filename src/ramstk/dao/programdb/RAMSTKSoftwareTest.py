# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKSoftwareTest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RAMSTKSoftwareTest Table
===============================================================================
"""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import error_handler, none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKSoftwareTest(RAMSTK_BASE):
    """
    Class to represent the table ramstk_software_test in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_software.
    """

    __tablename__ = 'ramstk_software_test'
    __table_args__ = {'extend_existing': True}

    software_id = Column(
        'fld_software_id',
        Integer,
        ForeignKey('ramstk_software.fld_software_id'),
        nullable=False)
    technique_id = Column(
        'fld_technique_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    recommended = Column('fld_recommended', Integer, default=0)
    used = Column('fld_used', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    software = relationship('RAMSTKSoftware', back_populates='software_test')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RAMSTKSoftwareTest
        data model attributes.

        :return: (software_id, technique_id, recommended, used)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.technique_id, self.recommended,
                       self.used)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RAMSTKSoftwareTest data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKSoftwareTest {0:d} " \
               "attributes.".format(self.software_id)

        try:
            self.recommended = int(none_to_default(attributes[0], 0))
            self.used = int(none_to_default(attributes[1], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKSoftwareTest.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKSoftwareTest attributes."

        return _error_code, _msg
