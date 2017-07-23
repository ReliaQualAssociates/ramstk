#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKPhase.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKPhase Package.
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


class RTKPhase(Base):
    """
    Class to represent the table rtk_phase in the RTK Common database.
    """

    __tablename__ = 'rtk_phase'
    __table_args__ = {'extend_existing': True}

    phase_id = Column('fld_phase_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Phase Description')
    type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKPhase data model
        attributes.

        :return: (phase_id, description, type)
        :rtype: tuple
        """

        _values = (self.phase_id, self.description, self.type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKPhase data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKPhase {0:d} attributes.". \
            format(self.phase_id)

        try:
            self.description = str(attributes[0])
            self.type = str(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKPhase.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKPhase attributes."

        return _error_code, _msg
