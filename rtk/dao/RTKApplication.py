#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKApplication.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKApplication Package.
"""

from sqlalchemy import Column, Float, Integer, String

# Import other RTK modules.
try:
    import Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKApplication(Base):
    """
    Class to represent the table rtk_application in the RTK Common database.
    """

    __tablename__ = 'rtk_application'

    application_id = Column('fld_application_id', Integer, primary_key=True,
                    autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Application Description')
    fault_density = Column('fld_fault_density', Float, default=1.0)
    transformation_ratio = Column('fld_transformation_ratio', Float,
                                  default=1.0)

    def get_attributes(self):
        """
        Application to retrieve the current values of the RTKApplication data model
        attributes.

        :return: (application_id, description, fault_density,
                  transformation_ratio)
        :rtype: tuple
        """

        _values = (self.application_id, self.description, self.fault_density,
                   self.transformation_ratio)

        return _values

    def set_attributes(self, attributes):
        """
        Application to set the current values of the RTKApplication data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKApplication {0:d} attributes.". \
            format(self.application_id)

        try:
            self.description = str(attributes[0])
            self.fault_density = float(attributes[1])
            self.transformation_ratio = float(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKApplication.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKApplication attributes."

        return _error_code, _msg
