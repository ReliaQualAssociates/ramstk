#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKLevel.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKLevel Package.
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


class RTKLevel(Base):
    """
    Class to represent the table rtk_level in the RTK Common database.
    """

    __tablename__ = 'rtk_level'
    __table_args__ = {'extend_existing': True}

    level_id = Column('fld_level_id', Integer, primary_key=True,
                    autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Level Description')
    type = Column('fld_type', String(256), default='')
    value = Column('fld_value', Integer, default=0)

    def get_attributes(self):
        """
        Level to retrieve the current values of the RTKLevel data model
        attributes.

        :return: (level_id, description, type, value)
        :rtype: tuple
        """

        _values = (self.level_id, self.description, self.type, self.value)

        return _values

    def set_attributes(self, attributes):
        """
        Level to set the current values of the RTKLevel data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKLevel {0:d} attributes.". \
            format(self.level_id)

        try:
            self.description = str(attributes[0])
            self.type = str(attributes[1])
            self.value = int(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKLevel.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKLevel attributes."

        return _error_code, _msg
