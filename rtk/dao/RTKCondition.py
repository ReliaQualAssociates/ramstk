#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCondition.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKCondition Package.
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


class RTKCondition(Base):
    """
    Class to represent the table rtk_condition in the RTK Common database.
    """

    __tablename__ = 'rtk_condition'
    __table_args__ = {'extend_existing': True}

    condition_id = Column('fld_condition_id', Integer, primary_key=True,
                          autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Condition Decription')
    type = Column('fld_type', String(256), default='')

    def get_attributes(self):
        """
        Condition to retrieve the current values of the RTKCondition data model
        attributes.

        :return: (condition_id, description, type)
        :rtype: tuple
        """

        _values = (self.condition_id, self.description, self.type)

        return _values

    def set_attributes(self, attributes):
        """
        Condition to set the current values of the RTKCondition data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCondition {0:d} attributes.". \
            format(self.condition_id)

        try:
            self.description = str(attributes[0])
            self.type = str(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCondition.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCondition attributes."

        return _error_code, _msg
