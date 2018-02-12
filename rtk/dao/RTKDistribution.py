# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKDistribution.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKDistribution Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKDistribution(RTK_BASE):
    """
    Class to represent the table rtk_distribution in the RTK Common database.
    """

    __tablename__ = 'rtk_distribution'
    __table_args__ = {'extend_existing': True}

    distribution_id = Column(
        'fld_distribution_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column(
        'fld_description', String(512), default='Distribution Description')
    dist_type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKDistribution data model
        attributes.

        :return: (phase_id, description, dist_type)
        :rtype: tuple
        """

        _values = (self.distribution_id, self.description, self.dist_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKDistribution data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKDistribution {0:d} attributes.". \
            format(self.distribution_id)

        try:
            self.description = str(
                none_to_default(attributes[0], 'Distribution Description'))
            self.dist_type = str(none_to_default(attributes[1], 'unknown'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKDistribution.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKDistribution attributes."

        return _error_code, _msg
