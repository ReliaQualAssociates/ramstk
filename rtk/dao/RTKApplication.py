# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKApplication.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKApplication Table
===============================================================================
"""

from sqlalchemy import Column, Float, Integer, String  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKApplication(RTK_BASE):
    """
    Class to represent the table rtk_application in the RTK Common database.
    """

    __tablename__ = 'rtk_application'
    __table_args__ = {'extend_existing': True}

    application_id = Column(
        'fld_application_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Application Description')
    fault_density = Column('fld_fault_density', Float, default=1.0)
    transformation_ratio = Column(
        'fld_transformation_ratio', Float, default=1.0)

    def get_attributes(self):
        """
        Application to retrieve the current values of the RTKApplication data
        model attributes.

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
            self.description = str(
                none_to_default(attributes[0], 'Application Description'))
            self.fault_density = float(none_to_default(attributes[1], 1.0))
            self.transformation_ratio = float(
                none_to_default(attributes[2], 1.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKApplication.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKApplication attributes."

        return _error_code, _msg
