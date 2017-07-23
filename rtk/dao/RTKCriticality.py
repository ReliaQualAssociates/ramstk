#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCriticality.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKCriticality Table
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
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKCriticality(Base):
    """
    Class to represent the table rtk_criticality in the RTK Common database.
    """

    __tablename__ = 'rtk_criticality'
    __table_args__ = {'extend_existing': True}

    criticality_id = Column('fld_criticality_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    name = Column('fld_name', String(256), default='Criticality Name')
    description = Column('fld_description', String(512),
                         default='Criticality Description')
    category = Column('fld_category', String(256), default='')
    value = Column('fld_value', Integer, default=0)

    def get_attributes(self):
        """
        Criticality to retrieve the current values of the RTKCriticality data
        model attributes.

        :return: (criticality_id, name, description, category, value)
        :rtype: tuple
        """

        _values = (self.criticality_id, self.name, self.description,
                   self.category, self.value)

        return _values

    def set_attributes(self, attributes):
        """
        Criticality to set the current values of the RTKCriticality data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCriticality {0:d} attributes.". \
            format(self.criticality_id)

        try:
            self.name = str(attributes[0])
            self.description = str(attributes[1])
            self.category = str(attributes[2])
            self.value = int(attributes[3])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCriticality.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCriticality attributes."

        return _error_code, _msg
