# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKHazards.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKHazard Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String        # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKHazards(RTK_BASE):
    """
    Class to represent the table rtk_hazard in the RTK Common database.
    """

    __tablename__ = 'rtk_hazards'
    __table_args__ = {'extend_existing': True}

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
            self.category = str(none_to_default(attributes[0],
                                                'Hazard Category'))
            self.subcategory = str(none_to_default(attributes[1],
                                                   'Hazard Subcategory'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKHazard.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKHazard attributes."

        return _error_code, _msg
