#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMeasurement.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKMeasurement Table
==============================
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
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKMeasurement(RTK_BASE):
    """
    Class to represent the table rtk_measurement in the RTK Common database.
    """

    __tablename__ = 'rtk_measurement'
    __table_args__ = {'extend_existing': True}

    measurement_id = Column('fld_measurement_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Failure Mode Decription')

    def get_attributes(self):
        """
        Measurement to retrieve the current values of the RTKMeasurement data
        model attributes.

        :return: (measurement_id, description)
        :rtype: tuple
        """

        _values = (self.measurement_id, self.description)

        return _values

    def set_attributes(self, attributes):
        """
        Measurement to set the current values of the RTKMeasurement data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMeasurement {0:d} attributes.". \
            format(self.measurement_id)

        try:
            self.description = str(attributes[0])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMeasurement.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMeasurement attributes."

        return _error_code, _msg
