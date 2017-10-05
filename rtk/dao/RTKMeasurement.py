# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMeasurement.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKMeasurement Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String      # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKMeasurement(RTK_BASE):
    """
    Class to represent the table rtk_measurement in the RTK Common database.
    """

    __tablename__ = 'rtk_measurement'
    __table_args__ = {'extend_existing': True}

    measurement_id = Column('fld_measurement_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Measurement Decription')

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
            self.description = str(none_to_default(attributes[0],
                                                   'Measurement Description'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMeasurement.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMeasurement attributes."

        return _error_code, _msg
