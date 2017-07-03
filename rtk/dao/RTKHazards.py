#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKHazards.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKHazard Package.
"""

from sqlalchemy import Column, Integer, String

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


class RTKHazards(Base):
    """
    Class to represent the table rtk_hazard in the RTK Common database.
    """

    __tablename__ = 'rtk_hazards'

    hazard_id = Column('fld_hazard_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    category = Column('fld_category', String(512),
                      default='Hazard Category')
    subcategory = Column('fld_subcategory', String(512),
                         default='Hazard Subcategory')

    def get_attributes(self):
        """
        Hazard to retrieve the current values of the RTKHazard data model
        attributes.

        :return: (hazard_id, description, fault_density,
                  transformation_ratio)
        :rtype: tuple
        """

        _values = (self.hazard_id, self.category, self.subcategory)

        return _values

    def set_attributes(self, attributes):
        """
        Hazard to set the current values of the RTKHazard data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKHazard {0:d} attributes.". \
            format(self.hazard_id)

        try:
            self.category = str(attributes[0])
            self.subcategory = str(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKHazard.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKHazard attributes."

        return _error_code, _msg
