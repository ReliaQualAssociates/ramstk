#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftwareTest.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKSoftwareTest Package.
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


class RTKSoftwareTest(Base):
    """
    Class to represent the table rtk_software_test in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_test'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    technique_id = Column('fld_technique_id', Integer, primary_key=True,
                          autoincrement=True, nullable=False)

    recommended = Column('fld_recommended', Integer, default=0)
    used = Column('fld_used', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='software_test')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSoftwareTest
        data model attributes.

        :return: (software_id, technique_id, recommended, used)
        :rtype: tuple
        """

        _attributes = (self.software_id, self.technique_id, self.recommended,
                       self.used)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKSoftwareTest data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSoftwareTest {0:d} " \
               "attributes.".format(self.software_id)

        try:
            self.recommended = int(attributes[0])
            self.used = int(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftwareTest.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftwareTest attributes."

        return _error_code, _msg
