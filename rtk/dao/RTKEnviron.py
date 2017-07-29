#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKEnviron.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKEnviron Table
==============================
"""

from sqlalchemy import Column, Float, Integer, String

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
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKEnviron(RTK_BASE):
    """
    Class to represent the table rtk_environ in the RTK Common database.
    """

    __tablename__ = 'rtk_environ'
    __table_args__ = {'extend_existing': True}

    environ_id = Column('fld_environ_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    code = Column('fld_code', String(256), default='Environ Code')
    description = Column('fld_description', String(512),
                         default='Environ Description')
    type = Column('fld_type', Integer, default='unknown')
    pi_e = Column('fld_pi_e', Float, default=1.0)
    do = Column('fld_do', Float, default=1.0)

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKEnviron data model
        attributes.

        :return: (environs_id, code, description, type, pi_e, do)
        :rtype: tuple
        """

        _values = (self.environ_id, self.code, self.description, self.type,
                   self.pi_e, self.do)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKEnviron data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKEnviron {0:d} attributes.". \
            format(self.environ_id)

        try:
            self.code = str(attributes[0])
            self.description = str(attributes[1])
            self.type = str(attributes[2])
            self.pi_e = float(attributes[3])
            self.do = float(attributes[4])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKEnviron.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKEnviron attributes."

        return _error_code, _msg
