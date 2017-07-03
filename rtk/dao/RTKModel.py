#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKModel.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKModel Package.
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


class RTKModel(Base):
    """
    Class to represent the table rtk_model in the RTK Common database.
    """

    __tablename__ = 'rtk_model'

    model_id = Column('fld_model_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Model Description')
    type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKModel data model
        attributes.

        :return: (model_id, description, type)
        :rtype: tuple
        """

        _values = (self.model_id, self.description, self.type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKModel data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKModel {0:d} attributes.". \
            format(self.model_id)

        try:
            self.description = str(attributes[0])
            self.type = str(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKModel.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKModel attributes."

        return _error_code, _msg
