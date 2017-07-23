#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKLoadHistory.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKLoadHistory Package.
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


class RTKLoadHistory(Base):
    """
    Class to represent the table rtk_load_history in the RTK Common database.
    """

    __tablename__ = 'rtk_load_history'
    __table_args__ = {'extend_existing': True}

    history_id = Column('fld_load_history_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Load History Description')

    def get_attributes(self):
        """
        LoadHistory to retrieve the current values of the RTKLoadHistory data
        model attributes.

        :return: (load_history_id, description)
        :rtype: tuple
        """

        _values = (self.history_id, self.description)

        return _values

    def set_attributes(self, attributes):
        """
        LoadHistory to set the current values of the RTKLoadHistory data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKLoadHistory {0:d} attributes.". \
            format(self.history_id)

        try:
            self.description = str(attributes[0])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKLoadHistory.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKLoadHistory attributes."

        return _error_code, _msg
